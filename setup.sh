#!/bin/bash

pip install -r requirements.txt
chmod +x cloudphoto
CURRENT_DIR=$(pwd)
echo "export PATH=\"$CURRENT_DIR:\$PATH\"" >> ~/.bashrc