---
title: "Prerequisites for LND Cloud Deployment"
description: "Required knowledge, tools, cloud accounts, and access permissions before deploying LND on AWS, GCP, or Azure."
tags: [prerequisites, setup, accounts, cli, permissions]
cloud: all
level: 100
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS CLI Documentation"
  - "Google Cloud SDK Documentation"
  - "Azure CLI Documentation"
  - "Terraform Documentation"
---

# Abstract

This guide outlines all prerequisites for following the LND Cloud Platform Guide tutorials and implementation guides. Covers required knowledge, cloud account setup, CLI tools, Terraform, and permissions needed for each cloud provider.

# 1. Required Knowledge

## 1.1 Bitcoin & Lightning Fundamentals

- **Bitcoin basics**: Blocks, transactions, UTXO model, confirmations
- **Lightning Network**: Payment channels, HTLCs, routing, gossip protocol
- **LND architecture**: Components [§10.1], RPC interfaces, macaroon authentication
- **Channel operations**: Opening, closing, splicing, rebalancing

## 1.2 Cloud Computing Basics

- **IaaS concepts**: VMs, storage, networking, load balancing
- **Identity & Access**: IAM/RBAC, service accounts, roles, policies
- **Networking**: VPC/VNet, subnets, security groups, DNS, VPN
- **Storage**: Block vs object vs file, encryption, snapshots, replication

## 1.3 Infrastructure as Code

- **Terraform**: Resources, modules, state, variables, outputs
- **GitOps**: Declarative infrastructure, pull-based deployment
- **CI/CD**: Pipeline concepts, artifact promotion, approval gates

# 2. Cloud Account Setup

## 2.1 AWS

### 2.1.1 Account Requirements

- AWS account with billing enabled
- IAM user/role with `AdministratorAccess` or equivalent custom policy
- MFA enabled on root and IAM users
- Default region configured (recommended: `us-east-1`, `us-west-2`, `eu-west-1`)

### 2.1.2 Required Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "elasticloadbalancing:*",
        "ec2:Describe*",
        "iam:*",
        "kms:*",
        "secretsmanager:*",
        "logs:*",
        "cloudwatch:*",
        "s3:*",
        "ebs:*",
        "vpc:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### 2.1.3 CLI Setup

```bash
# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure
aws configure
# Enter: Access Key ID, Secret Access Key, Default Region, Output Format (json)

# Verify
aws sts get-caller-identity
```

## 2.2 GCP

### 2.2.1 Account Requirements

- Google Cloud project with billing enabled
- User with `Project Owner` or `Editor` + `Security Admin` roles
- 2FA enabled
- Default region/zone configured

### 2.2.2 Required Permissions

Roles needed:
- `roles/compute.admin`
- `roles/iam.securityAdmin`
- `roles/secretmanager.admin`
- `roles/cloudkms.admin`
- `roles/logging.admin`
- `roles/monitoring.admin`
- `roles/storage.admin`

### 2.2.3 CLI Setup

```bash
# Install gcloud
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Initialize
gcloud init
# Select project, configure default region/zone

# Verify
gcloud auth list
gcloud config get-value project
```

## 2.3 Azure

### 2.3.1 Account Requirements

- Azure subscription with billing enabled
- User with `Owner` or `Contributor` + `User Access Administrator` roles
- MFA enabled via Entra ID
- Default location configured

### 2.3.2 Required Permissions

Roles needed:
- `Virtual Machine Contributor`
- `Network Contributor`
- `Storage Account Contributor`
- `Key Vault Administrator`
- `Monitoring Contributor`
- `Log Analytics Contributor`

### 2.3.3 CLI Setup

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login
# Select subscription
az account set --subscription <subscription-id>

# Verify
az account show
```

# 3. Required Tools

## 3.1 Terraform (Required)

```bash
# Install Terraform >= 1.9
wget https://releases.hashicorp.com/terraform/1.9.0/terraform_1.9.0_linux_amd64.zip
unzip terraform_1.9.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify
terraform version
# Should output: Terraform v1.9.0+
```

## 3.2 Git

```bash
# Install git
sudo apt-get update && sudo apt-get install -y git

# Configure
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 3.3 SSH Keys

```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "your.email@example.com" -f ~/.ssh/lnd-cloud

# For AWS: Import public key
aws ec2 import-key-pair --key-name lnd-cloud --public-key-material fileb://~/.ssh/lnd-cloud.pub

# For GCP: Add to project metadata
gcloud compute project-info add-metadata --metadata=ssh-keys="ubuntu:$(cat ~/.ssh/lnd-cloud.pub)"

# For Azure: Will be passed during VM creation
```

## 3.4 Optional Tools

| Tool | Purpose | Install |
|------|---------|---------|
| `kubectl` | Kubernetes management | Cloud SDK or standalone |
| `helm` | K8s package manager | `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 \| bash` |
| `jq` | JSON processing | `sudo apt-get install jq` |
| `yq` | YAML processing | `pip install yq` |
| `pre-commit` | Git hooks | `pip install pre-commit` |

# 4. Repository Setup

```bash
# Clone this guide
git clone https://github.com/ajettesla/cloud-plaform-lnd-guide
cd cloud-plaform-lnd-guide

# Install pre-commit hooks
pre-commit install

# Install Python dependencies
pip install -r requirements.txt

# Verify MkDocs builds
mkdocs build --strict
```

# 5. Verification Checklist

Before proceeding to tutorials [§12]:

- [ ] Cloud CLI authenticated and default region set
- [ ] Terraform >= 1.9 installed
- [ ] SSH key generated and registered with cloud provider
- [ ] Git configured with user identity
- [ ] Repository cloned and pre-commit hooks installed
- [ ] MkDocs builds without errors (`mkdocs build --strict`)
- [ ] Understanding of Bitcoin/LN fundamentals
- [ ] Basic Terraform knowledge (resources, modules, state)

# References

[1] AWS, "AWS CLI Command Reference," https://awscli.amazonaws.com/v2/documentation/
[2] Google Cloud, "gcloud CLI Reference," https://cloud.google.com/sdk/gcloud/reference
[3] Microsoft, "Azure CLI Reference," https://learn.microsoft.com/cli/azure/
[4] HashiCorp, "Terraform Documentation," https://developer.hashicorp.com/terraform/docs
[5] Lightning Network Daemon, "Installation Guide," https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md
