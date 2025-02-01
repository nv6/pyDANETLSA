#!/bin/bash

pwd


read -p 'Did you update the pyproject.toml file? [y/N]: ' ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi
echo

read -p 'Remove dist/ [y/N]: ' ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi
rm -rv dist/

VERSION=$(sed -n 's/^version = "\([^"]*\)"/\1/p' pyproject.toml)

read -p "Detected version in setup.cfg is \"$VERSION\". Is this correct? " ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi


echo "Build..."
python3 -m build || exit 1

echo
echo "Twine..."
python3 -m twine upload --repository testpypi dist/* --verbose || exit 1

echo

echo "test install with:"
echo "
mkdir /tmp/testingground
cd /tmp/testingground
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install cryptography pyOpenSSL requests dnspython
python3 -m pip install -i https://test.pypi.org/simple/ pyDANETLSA==${VERSION}
"
