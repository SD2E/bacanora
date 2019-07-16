
.PHONY: docs

docs:
	cd docs && make html

apidocs: docs-autodoc docs

# Refresh API doc sources
docs-autodoc:
	cd docs && sphinx-apidoc -M --maxdepth 1 -H "Package Docs" -f -o source ../bacanora

docs-clean:
	cd docs && make clean

# Clean all build artifacts
clean: docs-clean
	rm -rf build *egg-info dist
	find . -d -name '*__pycache__*' -exec rm -rf {} \;
	find . -d -name '*.pytest_cache*' -exec rm -rf {} \;
	find . -d -name '*.pyc' -exec rm -rf {} \;
