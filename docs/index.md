---
title: "LND Cloud Platform Guide"
description: "Professional technical documentation for deploying Lightning Network Daemon on AWS, GCP, and Azure"
tags: [home, lnd, lightning-network, aws, gcp, azure]
cloud: all
level: 100
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "Lightning Network Daemon Documentation"
  - "Google Cloud Workforce Identity Federation Documentation"
  - "AWS IAM Identity Center Documentation"
  - "Microsoft Entra ID Documentation"
---

# LND Cloud Platform Guide

> **Professional technical documentation** for deploying and operating Lightning Network Daemon (LND) on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. Each guide follows a standardized format: **Abstract → Introduction → Architecture → Implementation → Operations → Validation → Cost Analysis → Security → Troubleshooting → References**, enabling consistent cross-cloud comparison and professional reference.

---

## Documentation Structure — Category-First, Then Cloud

### 📁 01-cloud-architecture — Cloud Architecture (Per-Cloud)
**Start here for understanding each cloud's native architecture**
- [01-cloud-overview.md](01-cloud-architecture/01-cloud-overview.md) — Cloud basics, service models, global infrastructure, HA
- [02-prerequisites.md](01-cloud-architecture/02-prerequisites.md) — **Free trial details** (AWS/GCP/Azure), required knowledge, CLI setup
- [03-service-mapping.md](01-cloud-architecture/03-service-mapping.md) — Service mapping across clouds
- [04-architecture-comparison.md](01-cloud-architecture/04-architecture-comparison.md) — CSPM, Productivity (M365 vs Workspace), Governance, Compliance

### 📁 02-networking — Networking (Category-First)
**All networking services, organized by function, then by cloud**
- [00-index.md](02-networking/00-index.md) — Reading order
- [01-backbone.md](02-networking/01-backbone.md) — Global fiber, subsea cables, network tiers, private connectivity, latency
- [02-network-security.md](02-networking/02-network-security.md) — VPN, SD-WAN, MPLS, peering, PrivateLink/PSC/Private Endpoint
- [03-network-components.md](02-networking/03-network-components.md) — Router, Switch, NAT, Shared VPC, Firewall, LB
- [04-dns.md](02-networking/04-dns.md) — Route 53, Cloud DNS, Azure DNS — private zones, hybrid DNS
- [05-load-balancing.md](02-networking/05-load-balancing.md) — L4/L7, global anycast, TLS termination, WAF integration
- [06-vpc-peering.md](02-networking/06-vpc-peering.md) — VPC peering, PrivateLink/PSC/Private Endpoint

### 📁 03-iam — Identity & Access Management (Category-First)
**IAM organized by governance level, then cloud**
- [00-index.md](03-iam/00-index.md) — Reading order
- [01-iam-at-levels.md](03-iam/01-iam-at-levels.md) — **IAM at each governance layer**: Entra ID vs Azure RBAC, Cloud Identity vs Org/Folder/Proj, Identity Center vs Account/SCP
- [02-aws.md](03-iam/02-aws.md) — AWS IAM: Core, Identity Center, SAML/OIDC, STS, IRSA
- [03-gcp.md](03-iam/03-gcp.md) — GCP IAM: Cloud Identity, WIF (workforce/workload), Service Accounts
- [04-azure.md](03-iam/04-azure.md) — Azure IAM: Entra ID vs Azure RBAC, Enterprise Apps vs App Regs, Managed Identities, Conditional Access

### 📁 04-security — Security (Category-First)
**Security services by function**
- [00-index.md](04-security/00-index.md) — Reading order
- [01-security-services.md](04-security/01-security-services.md) — DDoS, WAF, NGFW, Bastion/IAP/Azure Bastion, CSPM, vendors (Palo Alto, Fortinet, Check Point)

### 📁 05-compute — Compute (Category-First)
- [00-index.md](05-compute/00-index.md) — VM, Kubernetes, Serverless comparison

### 📁 06-storage — Storage (Category-First)
- [00-index.md](06-storage/00-index.md) — Block, Object, File, Backup/DR

### 📁 07-billing — Billing & Cost Management (Category-First)
- [00-index.md](07-billing/00-index.md) — Reading order
- [01-data-transfer-costs.md](07-billing/01-data-transfer-costs.md) — Egress/ingress, cross-zone/region, inter-cloud, bucket/log costs

### 📁 08-deployment — Deployment Architecture (Patterns & Tutorials)
- [00-index.md](08-deployment/00-index.md) — Reading order
- [01-patterns.md](08-deployment/01-patterns.md) — Standalone, HA, K8s, Serverless, Multi-cloud
- [02-aws.md](08-deployment/02-aws.md) — EC2 + EBS + NLB tutorial
- [03-gcp.md](08-deployment/03-gcp.md) — Compute Engine + PD + ILB
- [04-azure.md](08-deployment/04-azure.md) — VM + Managed Disks + LB

### 📁 09-identity-fundamentals — SAML/OIDC Fundamentals
- [00-index.md](09-identity-fundamentals/00-index.md) — Reading order
- [01-saml-oidc.md](09-identity-fundamentals/01-saml-oidc.md) — SAML 2.0/OIDC architecture, flows, certs, tokens, mapping, trust boundaries

### 📁 10-cross-cutting — Cross-Cutting Concerns
- [00-index.md](10-cross-cutting/00-index.md) — Reading order
- [01-federation-patterns.md](10-cross-cutting/01-federation-patterns.md) — Cross-cloud workforce/workload federation, Patterns A/B/C

### 📁 11-reference — Reference
- [00-index.md](11-reference/00-index.md) — Reading order
- [01-cli-cheatsheet.md](11-reference/01-cli-cheatsheet.md) — Unified AWS/GCP/Azure CLI

---

## Recommended Reading Order

| Phase | Section | Start With |
|-------|---------|------------|
| **1. Cloud Basics** | 01-cloud-architecture | 01-cloud-overview → 02-prerequisites |
| **2. Category Deep Dives** | 02-networking → 03-iam → 04-security → 05-compute → 06-storage → 07-billing | Each category's 00-index.md |
| **3. Identity Fundamentals** | 09-identity-fundamentals | 01-saml-oidc.md |
| **4. Cloud-Specific IAM** | 03-iam | 02-aws → 03-gcp → 04-azure |
| **5. Deployment** | 08-deployment | 01-patterns → tutorials |
| **6. Cross-Cutting** | 10-cross-cutting | 01-federation-patterns.md |

---

## Cross-Reference System

| Notation | Meaning | Example |
|----------|---------|---------|
| `[§XX.Y]` | Section reference | `[§02.1]` → Backbone Network |
| `[Figure N]` | Diagram reference | `[Figure 3]` → Architecture diagram |
| `[Table N]` | Table reference | `[Table 2]` → Cost comparison |
| `[Listing N]` | Code listing | `[Listing 4]` → Terraform module |

---

## License

This documentation is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).