#!/bin/bash


install_docker() {
    echo "[TASK 1] Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh >/dev/null 2>&1
    usermod -aG docker vagrant
}

install_dependencies() {
    echo "[TASK 2] Installing Make and dependencies..."
    apt-get update >/dev/null 2>&1
    apt-get install -y make >/dev/null 2>&1
}

install_dependencies
install_docker

echo "[TASK 3] Provisioning Complete!"
