---
title: "CLI Cheatsheet: AWS, GCP, Azure for LND Operations"
description: "Quick reference for common cloud CLI commands used in LND deployment and operations across AWS, GCP, and Azure."
tags: [reference, cli, cheatsheet, aws, gcp, azure]
cloud: all
level: 100
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS CLI Reference"
  - "Google Cloud SDK Reference"
  - "Azure CLI Reference"
---

# Abstract

Unified command reference for cloud operations across AWS (aws), GCP (gcloud), and Azure (az). Organized by operational domain: compute, storage, networking, security, monitoring.

# 1. Authentication & Context

| Action | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Configure** | `aws configure` | `gcloud init` | `az login` |
| **Current Identity** | `aws sts get-caller-identity` | `gcloud auth list --filter=status:ACTIVE` | `az account show` |
| **List Accounts** | `aws organizations list-accounts` | `gcloud projects list` | `az account list -o table` |
| **Switch Account** | `aws configure set profile <name>` | `gcloud config set project <id>` | `az account set -s <id>` |
| **Default Region** | `aws configure set region <region>` | `gcloud config set compute/region <region>` | `az configure --defaults location=<region>` |

# 2. Compute (VMs)

## 2.1 Instance Management

| Action | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Create** | `aws ec2 run-instances --cli-input-json file://spec.json` | `gcloud compute instances create <name> --zone=<zone> --machine-type=<type> --image-family=<family> --image-project=<project>` | `az vm create -g <rg> -n <name> --image <image> --size <size> --admin-username <user> --ssh-key-values <key>` |
| **List** | `aws ec2 describe-instances --filters "Name=tag:app,Values=lnd" --query "Reservations[].Instances[].[InstanceId,State.Name,PrivateIpAddress,Tags[?Key=='Name'].Value|[0]]" -o table` | `gcloud compute instances list --filter="labels.app=lnd" --format="table(name,zone,status,networkInterfaces[0].networkIP,labels)"` | `az vm list -g <rg> --query "[?tags.app=='lnd'].{name:name, location:location, powerState:powerState, privateIp:privateIps[0]}" -o table` |
| **Get Details** | `aws ec2 describe-instances --instance-ids <id>` | `gcloud compute instances describe <name> --zone=<zone>` | `az vm show -g <rg> -n <name>` |
| **Start** | `aws ec2 start-instances --instance-ids <id>` | `gcloud compute instances start <name> --zone=<zone>` | `az vm start -g <rg> -n <name>` |
| **Stop** | `aws ec2 stop-instances --instance-ids <id>` | `gcloud compute instances stop <name> --zone=<zone>` | `az vm stop -g <rg> -n <name>` |
| **Reboot** | `aws ec2 reboot-instances --instance-ids <id>` | `gcloud compute instances reset <name> --zone=<zone>` | `az vm restart -g <rg> -n <name>` |
| **Delete** | `aws ec2 terminate-instances --instance-ids <id>` | `gcloud compute instances delete <name> --zone=<zone> --quiet` | `az vm delete -g <rg> -n <name> --yes` |

## 2.2 SSH Access

| Action | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **SSH (via bastion/SSM)** | `aws ssm start-session --target <id>` | `gcloud compute ssh <name> --zone=<zone> --tunnel-through-iap` | `az ssh vm -g <rg> -n <name>` |
| **Serial Console** | `aws ec2 get-serial-console-output --instance-id <id>` | `gcloud compute instances get-serial-port-output <name> --zone=<zone>` | `az vm boot-diagnostics get-boot-log -g <rg> -n <name>` |

# 3. Storage

## 3.1 Block Volumes

| Action | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Create** | `aws ec2 create-volume --size 100 --volume-type gp3 --iops 3000 --availability-zone <az> --encrypted --kms-key-id <key>` | `gcloud compute disks create <name> --size=100GB --type=pd-balanced --zone=<zone> --kms-key=<key>` | `az disk create -g <rg> -n <name> --size-gb 100 --sku Premium_LRS --encryption-type EncryptionAtRestWithPlatformKey` |
| **Attach** | `aws ec2 attach-volume --volume-id <vol> --instance-id <id> --device /dev/sdf` | `gcloud compute instances attach-disk <instance> --disk=<disk> --zone=<zone> --device-name=<name>` | `az vm disk attach -g <rg> --vm-name <vm> --name <disk> --sku Premium_LRS` |
| **Snapshot** | `aws ec2 create-snapshot --volume-id <vol> --description "LND backup $(date +%F)"` | `gcloud compute disks snapshot <disk> --snapshot-names=<name> --zone=<zone>` | `az snapshot create -g <rg> -n <name> --source <disk>` |

## 3.2 Object Storage

| Action | AWS S3 | GCP Cloud Storage | Azure Blob |
|--------|--------|-------------------|------------|
| **Create Bucket** | `aws s3 mb s3://<bucket> --region <region>` | `gsutil mb -l <region> gs://<bucket>` | `az storage container create -n <container> --account-name <account>` |
| **Upload** | `aws s3 cp <file> s3://<bucket>/<key>` | `gsutil cp <file> gs://<bucket>/<key>` | `az storage blob upload -f <file> -c <container> -n <blob> --account-name <account>` |
| **Sync** | `aws s3 sync <dir> s3://<bucket>/<prefix>` | `gsutil -m rsync -r <dir> gs://<bucket>/<prefix>` | `az storage blob sync -s <dir> -c <container> --account-name <account>` |
| **Lifecycle** | `aws s3api put-bucket-lifecycle-configuration --bucket <bucket> --lifecycle-configuration file://lifecycle.json` | `gsutil lifecycle set lifecycle.json gs://<bucket>` | `az storage account management-policy create --account-name <account> --policy @policy.json` |

# 4. Networking

## 4.1 VPC/VNet

| Action | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Create VPC** | `aws ec2 create-vpc --cidr-block 10.0.0.0/16` | `gcloud compute networks create <name> --subnet-mode=custom` | `az network vnet create -g <rg> -n <name> --address-prefix 10.0.0.0/16` |
| **Create Subnet** | `aws ec2 create-subnet --vpc-id <vpc> --cidr-block 10.0.1.0/24 --availability-zone <az>` | `gcloud compute networks subnets create <name> --network=<net> --range=10.0.1.0/24 --region=<region>` | `az network vnet subnet create -g <rg> --vnet-name <vnet> -n <name> --address-prefix 10.0.1.0/24` |

## 4.2 Security Groups / Firewall

| Action | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Create SG** | `aws ec2 create-security-group --group-name lnd-sg --description "LND Security Group" --vpc-id <vpc>` | `gcloud compute firewall-rules create lnd-allow --network=<net> --allow=tcp:9735,tcp:10009,tcp:8080 --source-ranges=0.0.0.0/0 --target-tags=lnd` | `az network nsg create -g <rg> -n lnd-nsg` |
| **Add Rule** | `aws ec2 authorize-security-group-ingress --group-id <sg> --protocol tcp --port 9735 --cidr 0.0.0.0/0` | `gcloud compute firewall-rules update lnd-allow --allow=tcp:9735,tcp:10009,tcp:8080` | `az network nsg rule create -g <rg> --nsg-name lnd-nsg -n allow-lnd --priority 100 --protocol Tcp --destination-port-ranges 9735 10009 8080 --access Allow` |

## 4.3 Load Balancer

| Action | AWS NLB | GCP Cloud LB | Azure LB |
|--------|---------|--------------|----------|
| **Create** | `aws elbv2 create-load-balancer --name lnd-nlb --scheme internet-facing --type network --subnet-mappings SubnetId=<subnet>,AllocationId=<eip>` | `gcloud compute address create lnd-lb-ip --region=<region>`<br>`gcloud compute target-pools create lnd-pool --region=<region>`<br>`gcloud compute forwarding-rules create lnd-rule --load-balancing-scheme=EXTERNAL --ports=9735 --target-pool=lnd-pool --address=lnd-lb-ip --region=<region>` | `az network lb create -g <rg> -n lnd-lb --sku Standard --frontend-ip-name lb-frontend --public-ip-address <pip> --backend-pool-name lb-backend` |

# 5. Security & Secrets

## 5.1 KMS

| Action | AWS KMS | GCP Cloud KMS | Azure Key Vault |
|--------|---------|---------------|-----------------|
| **Create Key** | `aws kms create-key --description "LND Master Key" --key-usage ENCRYPT_DECRYPT` | `gcloud kms keys create <name> --location=<loc> --keyring=<ring> --purpose=encryption` | `az keyvault key create --vault-name <vault> --name <name> --protection software` |
| **Encrypt** | `aws kms encrypt --key-id <id> --plaintext fileb://<file> --output text --query CiphertextBlob` | `gcloud kms encrypt --location=<loc> --keyring=<ring> --key=<key> --plaintext-file=<file> --ciphertext-file=<file>.enc` | `az keyvault key encrypt --vault-name <vault> --name <name> --algorithm RSA-OAEP --value <base64>` |
| **Decrypt** | `aws kms decrypt --ciphertext-blob fileb://<file> --output text --query Plaintext` | `gcloud kms decrypt --location=<loc> --keyring=<ring> --key=<key> --ciphertext-file=<file>.enc --plaintext-file=<file>` | `az keyvault key decrypt --vault-name <vault> --name <name> --algorithm RSA-OAEP --value <base64>` |

## 5.2 Secrets Manager

| Action | AWS Secrets Manager | GCP Secret Manager | Azure Key Vault |
|--------|---------------------|--------------------|-----------------|
| **Create** | `aws secretsmanager create-secret --name lnd/macaroon --secret-string "$(cat admin.macaroon | base64)"` | `gcloud secrets create lnd-macaroon --data-file=admin.macaroon` | `az keyvault secret set --vault-name <vault> --name lnd-macaroon --value "$(cat admin.macaroon | base64)"` |
| **Get** | `aws secretsmanager get-secret-value --secret-id lnd/macaroon --query SecretString --output text` | `gcloud secrets versions access latest --secret=lnd-macaroon` | `az keyvault secret show --vault-name <vault> --name lnd-macaroon --query value -o tsv` |

# 6. Monitoring & Logs

## 6.1 Metrics

| Action | AWS CloudWatch | GCP Cloud Monitoring | Azure Monitor |
|--------|----------------|---------------------|---------------|
| **List Metrics** | `aws cloudwatch list-metrics --namespace LND` | `gcloud monitoring metrics list --filter="metric.type=lnd_*"` | `az monitor metrics list --resource <id>` |
| **Get Statistics** | `aws cloudwatch get-metric-statistics --namespace LND --metric-name lnd_num_peers --start-time <ts> --end-time <ts> --period 300 --statistics Average` | `gcloud monitoring time-series list --filter='metric.type="lnd_num_peers" AND resource.type="gce_instance"'` | `az monitor metrics list --resource <id> --metric lnd_num_peers --interval PT5M` |

## 6.2 Logs

| Action | AWS CloudWatch Logs | GCP Cloud Logging | Azure Log Analytics |
|--------|---------------------|-------------------|---------------------|
| **Tail Logs** | `aws logs tail /aws/ec2/lnd --follow` | `gcloud logging read "resource.type=gce_instance AND labels.instance_name=lnd-*" --limit=50 --format=json` | `az monitor log-analytics query -w <workspace> --analytics-query "ContainerLog | where ContainerName == 'lnd' | limit 50"` |
| **Export to Storage** | `aws logs put-subscription-filter --log-group-name /aws/ec2/lnd --filter-name lnd-to-s3 --destination-arn <kinesis-firehose-arn>` | `gcloud logging sinks create lnd-to-gcs --destination=storage.googleapis.com/<bucket> --log-filter='resource.type="gce_instance"'` | `az monitor diagnostic-settings create --name lnd-to-blob --resource <id> --storage-account <account> --logs '[{"category":"LinuxSyslog","enabled":true}]'` |

# 7. Container / Kubernetes

## 7.1 Kubernetes

| Action | AWS EKS | GCP GKE | Azure AKS |
|--------|---------|---------|-----------|
| **Create Cluster** | `eksctl create cluster -f cluster.yaml` | `gcloud container clusters create-auto <name> --region=<region>` | `az aks create -g <rg> -n <name> --enable-managed-identity --enable-workload-identity` |
| **Get Credentials** | `aws eks update-kubeconfig --name <cluster>` | `gcloud container clusters get-credentials <name> --region=<region>` | `az aks get-credentials -g <rg> -n <name>` |
| **Delete Cluster** | `eksctl delete cluster -f cluster.yaml` | `gcloud container clusters delete <name> --region=<region> --quiet` | `az aks delete -g <rg> -n <name> --yes` |

## 7.2 Container Registry

| Action | AWS ECR | GCP Artifact Registry | Azure Container Registry |
|--------|---------|----------------------|-------------------------|
| **Create Repo** | `aws ecr create-repository --repository-name lnd` | `gcloud artifacts repositories create lnd --repository-format=docker --location=<region>` | `az acr create -g <rg> -n <registry> --sku Premium` |
| **Login** | `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com` | `gcloud auth configure-docker <region>-docker.pkg.dev` | `az acr login -n <registry>` |
| **Push** | `docker push <account>.dkr.ecr.<region>.amazonaws.com/lnd:latest` | `docker push <region>-docker.pkg.dev/<project>/lnd/lnd:latest` | `docker push <registry>.azurecr.io/lnd:latest` |

# 8. LND-Specific Operations

## 8.1 Via SSH/SSM

```bash
# All clouds: SSH into instance, then:
lncli getinfo                          # Node status
lncli listpeers                        # Peer connections
lncli listchannels                     # Active channels
lncli pendingchannels                  # Pending opens/closes
lncli feereport                        # Fee revenue
lncli closedchannels                   # Channel history
lncli describegraph                    # Network view
lncli walletbalance                    # On-chain balance
lncli channelbalance                   # Off-chain balance
lncli sendcoins --addr <addr> --amt <sat>  # On-chain send
lncli addinvoice --amt <sat> --memo "<memo>"  # Create invoice
lncli payinvoice --pay_req <invoice>   # Pay invoice
lncli connect <pubkey>@<host>:9735     # Connect peer
lncli openchannel --node_key=<pubkey> --local_amt=<sat>  # Open channel
lncli closechannel --channel_point=<txid:vout>  # Close channel
```

## 8.2 Via Kubernetes

```bash
# Exec into LND pod
kubectl exec -it lnd-0 -n lnd -- lncli getinfo

# Port-forward for local lncli
kubectl port-forward -n lnd svc/lnd 10009:10009 8080:8080
lncli --rpcserver=localhost:10009 --macaroonpath=~/.lnd/admin.macaroon --tlscertpath=~/.lnd/tls.cert getinfo

# View logs
kubectl logs -f -n lnd lnd-0

# Restart
kubectl rollout restart statefulset/lnd -n lnd
```

# 9. Terraform Commands

```bash
# Initialize
terraform init

# Format
terraform fmt -recursive

# Validate
terraform validate

# Plan
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Destroy
terraform destroy -auto-approve

# State management
terraform state list
terraform state show <resource>
terraform import <resource> <id>
terraform state mv <src> <dst>

# Workspaces
terraform workspace list
terraform workspace new <name>
terraform workspace select <name>
```

# References

[1] AWS CLI Command Reference: https://awscli.amazonaws.com/v2/documentation/
[2] Google Cloud SDK Reference: https://cloud.google.com/sdk/gcloud/reference
[3] Azure CLI Reference: https://learn.microsoft.com/cli/azure/
[4] Terraform CLI: https://developer.hashicorp.com/terraform/cli
[5] Kubernetes kubectl: https://kubernetes.io/docs/reference/kubectl/
