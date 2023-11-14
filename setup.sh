#!/bin/bash

# This script assumes you have sudo access to your computer

# Install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
(echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> $HOME/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

sudo apt-get install build-essential

# Install pipx
brew install pipx
pipx ensurepath

# Install poetry for python package management
pipx install poetry

# Create poetry virtual environment
poetry install
