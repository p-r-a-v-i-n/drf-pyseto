# Releasing

1. Update version in:
   - `pyproject.toml`
   - `drf_pyseto/__init__.py`
2. Commit the version bump.
3. Tag the release and push:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

The GitHub Actions `Release` workflow will build and publish to PyPI using trusted publishing.
