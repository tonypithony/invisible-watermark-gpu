pip install twine wheel setuptools

python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*