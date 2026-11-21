---
title: "Cloud Provider Comparison for LND Deployment"
description: "Detailed comparison of AWS, GCP, and Azure for running Lightning Network Daemon: services, pricing, limits, and operational characteristics."
tags: [comparison, aws, gcp, azure, decision-matrix]
cloud: all
level: 200
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS Service Documentation"
  - "Google Cloud Service Documentation"
  - "Azure Service Documentation"
---

# Abstract

This document provides a comprehensive comparison of Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure for deploying Lightning Network Daemon (LND). We evaluate compute, storage, networking, security, monitoring, and cost dimensions to support architecture decisions [§01.3].

# 1. Compute Comparison

## 1.1 Virtual Machines

| Feature | AWS EC2 | GCP Compute Engine | Azure Virtual Machines |
|---------|---------|-------------------|------------------------|
| **Instance Types** | 500+ (x86, ARM, GPU) | 100+ (x86, ARM, GPU) | 200+ (x86, ARM, GPU) |
| **ARM/Graviton** | Graviton2/3/4 | Tau T2A, Axion | Cobalt 100 |
| **Confidential Computing** | Nitro Enclaves | Confidential VMs | Confidential VMs |
| **Spot/Preemptible** | Spot Instances (90% off) | Spot VMs (60-91% off) | Spot VMs (90% off) |
| **Per-second Billing** | Yes (Linux) | Yes | Yes (Linux) |
| **Local NVMe** | i3, i4, im4gn | Local SSD | Lsv3, Lsv2 |
| **Dedicated Hosts** | Yes | Sole-tenant nodes | Dedicated Hosts |

## 1.2 Kubernetes

| Feature | EKS | GKE | AKS |
|---------|-----|-----|-----|
| **Control Plane** | Managed ($0.10/hr) | Free (Autopilot: $0.01/pod/hr) | Free |
| **Node Pools** | Managed/Unmanaged | Standard/Autopilot | System/User |
| **Workload Identity** | IRSA | GKE Workload Identity | Azure AD Workload Identity |
| **Autoscaling** | Karpenter, Cluster Autoscaler | GKE Autopilot, NAP | Cluster Autoscaler, NAP |
| **Private Clusters** | Yes | Yes | Yes |
| **Release Channels** | Standard, Extended | Rapid, Regular, Stable | Standard, Rapid |

## 1.3 Serverless

| Feature | AWS Lambda | GCP Cloud Run | Azure Container Apps |
|---------|------------|---------------|---------------------|
| **Max Duration** | 15 min | 60 min | 24 hr |
| **Memory** | 10 GB | 32 GB | 18 GB |
| **vCPU** | 6 | 8 | 4 |
| **Cold Start** | ~100ms | ~200ms | ~500ms |
| **VPC Support** | Yes | Yes | Yes |
| **GPU** | No | Yes (L4) | No |
| **Pricing** | Per 1ms | Per 100ms | Per second |

# 2. Storage Comparison

## 2.1 Block Storage

| Feature | AWS EBS | GCP Persistent Disk | Azure Managed Disks |
|---------|---------|---------------------|---------------------|
| **Types** | gp3, io2, io1, st1, sc1 | SSD, Balanced, Extreme, HDD | Premium SSD v2, Premium SSD, Standard SSD, Standard HDD |
| **Max Size** | 64 TiB | 64 TiB | 32 TiB |
| **Max IOPS** | 256,000 (io2) | 360,000 (Extreme) | 80,000 (Premium v2) |
| **Encryption** | AWS KMS / Custom | Google KMS / CMEK | Azure Key Vault / CMK |
| **Snapshots** | Incremental, cross-region | Incremental, multi-region | Incremental, geo-redundant |
| **Multi-attach** | io2 only | No | No |

## 2.2 Object Storage

| Feature | AWS S3 | GCP Cloud Storage | Azure Blob Storage |
|---------|--------|-------------------|-------------------|
| **Classes** | Standard, IA, Glacier, Deep Archive | Standard, Nearline, Coldline, Archive | Hot, Cool, Cold, Archive |
| **Min Duration** | 30d (IA) | 30d (Nearline) | 30d (Cool) |
| **Retrieval** | Expedited/Standard/Bulk | Standard/Expedited | Standard/High Priority |
| **Replication** | CRR, SRR | Dual-region, Turbo | GRS, GZRS, LRS |
| **Event Notifications** | S3 Event Notifications | Pub/Sub | Event Grid |

# 3. Networking Comparison

## 3.1 VPC/VNet

| Feature | AWS VPC | GCP VPC | Azure VNet |
|---------|---------|---------|------------|
| **Global** | Region-scoped | Global | Region-scoped |
| **Subnets** | AZ-scoped | Region-scoped | Region-scoped |
| **Max CIDR** | /16 | /16 | /8 |
| **Peering** | Transitive via TGW | Non-transitive | Non-transitive |
| **Transit** | Transit Gateway | Network Connectivity Center | Virtual WAN |
| **Private Access** | PrivateLink, VPC Endpoints | Private Service Connect | Private Link, Service Endpoints |

## 3.2 Load Balancing

| Feature | AWS NLB/ALB | GCP Cloud LB | Azure Load Balancer |
|---------|-------------|--------------|---------------------|
| **L4 (TCP/UDP)** | NLB | External TCP/UDP LB | Standard LB |
| **L7 (HTTP/HTTPS)** | ALB | External HTTP(S) LB | Application Gateway |
| **Global Anycast** | No (ALB regional) | Yes | No |
| **TLS Termination** | Yes | Yes | Yes |
| **Health Checks** | TCP, HTTP, HTTPS | TCP, HTTP, HTTPS, gRPC | TCP, HTTP, HTTPS |
| **Cross-zone LB** | Yes (NLB) | Yes | Yes |

# 4. Security Comparison

## 4.1 Identity & Access

| Feature | AWS IAM | GCP IAM | Azure Entra ID |
|---------|---------|---------|----------------|
| **Model** | Policy-based | Role-based (with conditions) | Role-based (with conditions) |
| **Workload Identity** | IRSA (OIDC) | Workload Identity (OIDC) | Entra Workload Identity (OIDC) |
| **Service Accounts** | IAM Roles | Service Accounts | Managed Identities |
| **Condition Keys** | Yes | Yes | Yes |
| **Permission Boundaries** | Yes | Yes (deny policies) | Yes |
| **External Identities** | SAML/OIDC | SAML/OIDC | SAML/OIDC/WS-Fed |

## 4.2 Secrets & Keys

| Feature | AWS Secrets Manager + KMS | GCP Secret Manager + Cloud KMS | Azure Key Vault + Managed HSM |
|---------|---------------------------|--------------------------------|--------------------------------|
| **Rotation** | Native (Lambda) | Native (Cloud Functions) | Native (Rotation Policies) |
| **Versioning** | Yes | Yes | Yes |
| **Cross-region** | Replication | Multi-region | Geo-replication |
| **HSM** | CloudHSM (FIPS 140-2 L3) | Cloud HSM (FIPS 140-2 L3) | Managed HSM (FIPS 140-2 L3) |
| **Cost** | $0.40/secret/mo + API calls | $0.06/secret/mo + API calls | Standard: free, Premium: $1/key/mo |

# 5. Monitoring Comparison

| Feature | AWS CloudWatch | GCP Cloud Monitoring | Azure Monitor |
|---------|----------------|---------------------|---------------|
| **Metrics** | Custom, AWS namespaces | Custom, GCP namespaces | Custom, Azure namespaces |
| **Logs** | CloudWatch Logs | Cloud Logging | Log Analytics |
| **Traces** | X-Ray | Cloud Trace | Application Insights |
| **Alerting** | CloudWatch Alarms | Alerting Policies | Alert Rules |
| **Dashboards** | CloudWatch Dashboards | Monitoring Dashboards | Workbooks |
| **SLO/SLI** | ServiceLens | SLO Monitoring | Azure Monitor SLOs |

# 6. Pricing Comparison (Estimated Monthly, us-east-1/us-central1/East US)

## 6.1 LND Node (m6i.large / n2-standard-2 / Standard_D4s_v3 + 100GB gp3/SSD/SSD)

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| Compute (730h) | $67.89 | $52.56 | $63.51 |
| Block Storage (100GB) | $8.00 | $17.00 | $15.00 |
| Snapshots (100GB) | $5.00 | $5.00 | $5.00 |
| Load Balancer | $18.00 (NLB) | $18.00 | $18.00 |
| Data Transfer (1TB) | $90.00 | $85.00 | $87.00 |
| **Total** | **$188.89** | **$177.56** | **$188.51** |

*With 1-year Reserved/Committed Use Discount: ~30% savings on compute*

## 6.2 Kubernetes Control Plane

| Service | Monthly Cost |
|---------|--------------|
| EKS | $73.00 |
| GKE Standard | $73.00 |
| GKE Autopilot | Per pod (~$10-20/pod) |
| AKS | Free |

# 7. Regional Availability

| Region | AWS | GCP | Azure |
|--------|-----|-----|-------|
| US East | us-east-1, us-east-2 | us-central1, us-east1, us-east4 | East US, East US 2 |
| US West | us-west-1, us-west-2 | us-west1, us-west2, us-west3 | West US, West US 2, West US 3 |
| EU | eu-west-1, eu-central-1, eu-north-1 | europe-west1, europe-west4, europe-north1 | North Europe, West Europe, Sweden Central |
| Asia Pacific | ap-northeast-1, ap-southeast-1, ap-southeast-2 | asia-northeast1, asia-southeast1, australia-southeast1 | Southeast Asia, East Asia, Australia East |

# 8. Decision Matrix

| Priority | Recommended | Rationale |
|----------|-------------|-----------|
| **Lowest Cost** | GCP | Sustained use discounts, competitive pricing |
| **Best K8s** | GKE | Autopilot, free control plane, best workload identity |
| **Enterprise Integration** | Azure | Entra ID, hybrid, Windows workloads |
| **Most Services** | AWS | Broadest portfolio, most regions, mature ecosystem |
| **ARM/Graviton** | AWS | Graviton4, best price/performance |
| **Confidential Computing** | All | Comparable offerings |
| **Compliance** | All | Similar certifications (SOC2, ISO, FedRAMP) |

# 9. Multi-Cloud Strategy

For HA across clouds [§10.5]:

1. **Primary**: Single cloud for simplicity
2. **Secondary**: Different cloud for disaster recovery
3. **Network**: Cloud Interconnect / ExpressRoute / Direct Connect
4. **Data**: Cross-region replication with consistent snapshots
5. **DNS**: Global load balancer with health checks (Route53, Cloud DNS, Traffic Manager)

# References

[1] AWS, "Amazon EC2 Pricing," https://aws.amazon.com/ec2/pricing/
[2] Google Cloud, "Compute Engine Pricing," https://cloud.google.com/compute/pricing
[3] Microsoft Azure, "Virtual Machines Pricing," https://azure.microsoft.com/pricing/details/virtual-machines/
[4] Cloud Provider Documentation (links in each section)
