from __future__ import annotations

import argparse
import importlib.util
import os
import unittest
from pathlib import Path
from unittest import mock


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "sync-package-manifests.py"
SPEC = importlib.util.spec_from_file_location("sync_package_manifests", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"failed to load {SCRIPT_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SyncPackageManifestsTests(unittest.TestCase):
    def test_version_from_tag_supports_common_release_forms(self) -> None:
        self.assertEqual(MODULE.version_from_tag("v0.31.0"), "0.31.0")
        self.assertEqual(MODULE.version_from_tag("refs/tags/v0.31.0"), "0.31.0")
        self.assertEqual(MODULE.version_from_tag("0.31.0"), "0.31.0")
        self.assertIsNone(MODULE.version_from_tag("nightly"))

    def test_resolve_release_metadata_uses_latest_stable_release_by_default(self) -> None:
        release_payload = {
            "tag_name": "v0.31.0",
            "draft": False,
            "prerelease": False,
            "assets": [],
        }

        with mock.patch.object(MODULE, "fetch_json", return_value=release_payload) as fetch_json:
            release, tag, version = MODULE.resolve_release_metadata("xidl/xidl", None, "token")

        fetch_json.assert_called_once_with(
            "https://api.github.com/repos/xidl/xidl/releases/latest",
            "token",
        )
        self.assertIs(release, release_payload)
        self.assertEqual(tag, "v0.31.0")
        self.assertEqual(version, "0.31.0")

    def test_main_derives_formula_and_scoop_from_release_metadata(self) -> None:
        writes: list[tuple[Path, str, bool]] = []
        args = argparse.Namespace(
            repo="xidl/xidl",
            version=None,
            tag="v0.31.0",
            check=False,
        )
        release_payload = {
            "tag_name": "v0.31.0",
            "draft": False,
            "prerelease": False,
            "assets": [],
        }

        with (
            mock.patch.dict(os.environ, {}, clear=True),
            mock.patch.object(MODULE, "parse_args", return_value=args),
            mock.patch.object(
                MODULE,
                "resolve_release_metadata",
                return_value=(release_payload, "v0.31.0", "0.31.0"),
            ),
            mock.patch.object(
                MODULE,
                "resolve_windows_assets",
                return_value={
                    "64bit": {
                        "url": "https://example.com/xidlc-x86_64-pc-windows-gnu.tar.gz",
                        "sha256": "a" * 64,
                        "target": "x86_64-pc-windows-gnu",
                        "archive": "tar.gz",
                        "autoupdate_url": "https://example.com/v$version/xidlc.tar.gz",
                        "winget_supported": False,
                    }
                },
            ),
            mock.patch.object(MODULE, "sha256_url", return_value="b" * 64) as sha256_url,
            mock.patch.object(
                MODULE,
                "write_text",
                side_effect=lambda path, content, check: writes.append((path, content, check))
                or True,
            ),
        ):
            self.assertEqual(MODULE.main(), 0)

        sha256_url.assert_called_once_with(
            "https://github.com/xidl/xidl/archive/refs/tags/v0.31.0.tar.gz",
            None,
        )

        rendered = {path: content for path, content, _ in writes}
        self.assertIn(MODULE.FORMULA_PATH, rendered)
        self.assertIn(MODULE.SCOOP_PATH, rendered)
        self.assertIn(
            'url "https://github.com/xidl/xidl/archive/refs/tags/v0.31.0.tar.gz"',
            rendered[MODULE.FORMULA_PATH],
        )
        self.assertIn('"version": "0.31.0"', rendered[MODULE.SCOOP_PATH])

    def test_resolve_release_metadata_rejects_prerelease(self) -> None:
        release_payload = {
            "tag_name": "nightly",
            "draft": False,
            "prerelease": True,
            "assets": [],
        }

        with mock.patch.object(MODULE, "fetch_json", return_value=release_payload):
            with self.assertRaises(MODULE.SyncError):
                MODULE.resolve_release_metadata("xidl/xidl", None, None)


if __name__ == "__main__":
    unittest.main()
