#!/bin/bash

pwd

read -p 'Remove dist/ [y/N]: ' ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi
rm -rv dist/

read -p 'What is the new version?: ' VERSION
echo "Is this correct [y/N]: $VERSION"

if [ "$ANSWER" != 'y' ]; then
    exit 1
fi


python3 -m build || exit 1
python3 -m twine upload --repository testpypi dist/* --verbose || exit 1

echo "Wait for processing..."
echo python3 -m pip install -i https://test.pypi.org/simple/ pyDANETLSA==${ANSWER}

