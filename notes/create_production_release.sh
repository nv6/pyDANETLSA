#!/bin/bash

pwd


read -p 'Did you update the setup.cfg file? [y/N]: ' ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi
echo

read -p 'Remove dist/ [y/N]: ' ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi
rm -rv dist/

VERSION=$(sed -n 's/^version *= *//p' setup.cfg)
read -p "Detected version in setup.cfg is \"$VERSION\". Is this correct? " ANSWER
if [ "$ANSWER" != 'y' ]; then
    exit 1
fi


echo "Build..."
python3 -m build || exit 1

echo
echo "Twine..."
python3 -m twine upload --repository pypi dist/* --verbose || exit 1
echo

echo "test install with:"
echo "
mkdir /tmp/testingground
cd /tmp/testingground
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -i https://pypi.org/simple/ pyDANETLSA==${ANSWER}
"
