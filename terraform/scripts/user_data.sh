#!/bin/bash
# Bootstrap script run automatically by EC2 on first boot (passed in by Terraform).
# Installs: Java 21, Jenkins LTS, Docker, Git, Python 3 (+venv), and adds 2 GB swap.
# Progress log on the server: /var/log/user-data.log
set -euxo pipefail
exec > >(tee -a /var/log/user-data.log) 2>&1
export DEBIAN_FRONTEND=noninteractive

# --- 2 GB swap so Jenkins + Docker builds fit on a small instance ---
if [ ! -f /swapfile ]; then
  fallocate -l 2G /swapfile
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
  echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

# --- Base packages ---
apt-get update -y
apt-get install -y fontconfig openjdk-21-jre-headless git curl unzip \
  python3 python3-venv python3-pip ca-certificates gnupg

# --- Docker ---
apt-get install -y docker.io
systemctl enable --now docker

# --- Jenkins LTS (official repo, 2026 signing key) ---
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key -o /etc/apt/keyrings/jenkins-keyring.asc
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
  > /etc/apt/sources.list.d/jenkins.list
apt-get update -y
apt-get install -y jenkins

# Let Jenkins (and the ubuntu user) run docker without sudo
usermod -aG docker jenkins
usermod -aG docker ubuntu

systemctl enable jenkins
systemctl restart jenkins

echo "BOOTSTRAP_COMPLETE $(date -u)" > /var/log/bootstrap-status
