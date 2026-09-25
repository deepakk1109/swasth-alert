#!/bin/bash
yum update -y
yum install -y docker
systemctl start docker
systemctl enable docker


aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 992764023424.dkr.ecr.ap-south-1.amazonaws.com


docker run -d -p 8080:8080 992764023424.dkr.ecr.ap-south-1.amazonaws.com/swasth-alert:latest
