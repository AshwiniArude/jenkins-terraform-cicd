#!/bin/bash
# Run on the EC2 server:  bash verify_server.sh
# Prints the status of everything Terraform's bootstrap script installed.

line() { printf '%*s\n' 60 '' | tr ' ' '-'; }

line; echo " SERVER VERIFICATION - $(hostname) - $(date)"; line
echo "Bootstrap : $(cat /var/log/bootstrap-status 2>/dev/null || echo 'still running - check: sudo tail -f /var/log/user-data.log')"
echo "OS        : $(lsb_release -ds 2>/dev/null)"
echo "Java      : $(java -version 2>&1 | head -1)"
echo "Jenkins   : $(jenkins --version 2>/dev/null || echo 'not installed yet') ($(systemctl is-active jenkins))"
echo "Docker    : $(docker --version 2>/dev/null) ($(systemctl is-active docker))"
echo "Git       : $(git --version)"
echo "Python    : $(python3 --version)"
echo "Jenkins in docker group: $(id -nG jenkins 2>/dev/null | grep -qw docker && echo yes || echo NO)"
line
echo "Memory:"; free -h
line
echo "Running containers:"; docker ps 2>/dev/null || sudo docker ps
line
