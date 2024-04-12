rm -r dist
python3 -m build --sdist
python3 -m build --wheel

twine upload --repository testpypi dist/*