#!/bin/bash

# Install dependencies
apt-get update
apt-get install -y wget gnupg unzip python3-pip

# Download and install Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
apt-get update
apt-get install -y google-chrome-stable

# Install Python packages
pip3 install selenium undetected-chromedriver

echo "Setup complete."

