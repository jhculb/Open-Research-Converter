#!/bin/bash
sudo apt-get update && sudo apt-get upgrade -y
REQUIRED_PKG="poetry"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
    sudo apt-get install curl
    curl -sSL https://install.python-poetry.org | python3 -
fi
echo "Adding to path"
export PATH="$HOME/.local/bin:$PATH"
echo "Configuring poetry"
poetry self update
poetry completions bash >> ~/.bash_completion
poetry init
poetry add $( cat dev_requirements.txt ) --group dev
poetry add $( cat test_requirements.txt ) --group test
poetry run pre-commit install