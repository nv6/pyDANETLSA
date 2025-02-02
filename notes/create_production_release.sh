#!/bin/bash

VERSION=$(sed -n 's/^version = "\([^"]*\)"/\1/p' pyproject.toml)


read -p "Detected version in setup.cfg is \"$VERSION\". Is this correct? " ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi


echo "Removing dist..."
rm -rf dist build *.egg-info

echo "Building..."
python3 -m build || exit 1


echo "Inspecting:"
echo "---"
tar tzf dist/pydanetlsa-${VERSION}.tar.gz
echo "---"


read -p "Upload to PRODUCTION pypi? [y/N] " ANSWER
if [ "$ANSWER" = 'y' ]; then
    echo
    echo "Twine..."
    python3 -m twine upload --repository pypi dist/* --verbose || exit 1
    echo
fi

