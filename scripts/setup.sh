#!/bin/bash

# 1. Detect the Operating System
OS="$(uname -s)"
echo "Detected OS: $OS"

install_windows() {
    echo "Installing on Windows..."
    
    if command -v winget &> /dev/null; then
        echo "Winget found. Installing tools..."
        
        winget install -e --id Docker.DockerDesktop
        
        winget install -e --id GnuWin32.Make
        
        winget install -e --id Python.Python.3
        
        echo "Installation commands sent. You may need to restart your terminal."
    else
        echo "Error: 'winget' not found. Please update Windows App Installer from the Microsoft Store."
        exit 1
    fi
}

install_mac() {
    echo "Installing on macOS..."
    
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    echo "Updating Homebrew..."
    brew update
    
    brew install --cask docker
    brew install make
    brew install python
}

install_linux() {
    echo "Installing on Linux (Ubuntu/Debian)..."
    
    sudo apt-get update
    
    sudo apt-get install -y make docker.io docker-compose-v2 python3 python3-pip python3-venv
    
    sudo usermod -aG docker $USER
    echo "You must log out and log back in for Docker permissions to take effect."
}

# 2. Execute the correct function based on OS
case "$OS" in
    Linux*)     install_linux;;
    Darwin*)    install_mac;;
    CYGWIN*|MINGW*|MSYS*) install_windows;;
    *)          echo "Unknown Operating System: $OS"; exit 1 ;;
esac

echo "Installation attempt complete."
echo "Please restart your terminal/computer to ensure tools are available in your PATH."