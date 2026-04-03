# xidl-packaging

This repository owns package manager distribution metadata for `xidlc`.

It is intentionally separate from [`xidl/xidl`](https://github.com/xidl/xidl):

- `xidl/xidl` builds and publishes CLI release assets.
- `xidl-packaging` watches the latest stable GitHub Release and refreshes downstream package manager manifests.

## Managed outputs

- `Formula/xidlc.rb`
- `packaging/scoop/xidlc.json`
- `packaging/winget/manifests/x/xidl/xidlc/`

## Automation

`.github/workflows/sync-xidlc-package-manifests.yml` runs every day and can also
be triggered manually.

- Scheduled runs sync the latest stable release from `xidl/xidl`.
- Manual runs can backfill a specific release with `release_tag`.

Only published stable releases are synced. Drafts, prereleases, and `nightly`
are ignored.

## Local usage

Sync the latest stable release:

```bash
python3 scripts/sync-package-manifests.py
```

Sync a specific release tag:

```bash
python3 scripts/sync-package-manifests.py --tag v0.32.0
```

Run local checks:

```bash
python3 -m py_compile scripts/sync-package-manifests.py scripts/tests/test_sync_package_manifests.py
python3 -m unittest discover -s scripts/tests
```
