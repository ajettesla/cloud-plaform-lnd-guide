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

## Documentation Structure — Follow This Order

### Phase 1: Cloud Fundamentals
**[01-cloud-fundamentals/00-index.md](01-cloud-fundamentals/00-index.md)**
1. [01-overview.md](01-cloud-fundamentals/01-overview.md) — Cloud basics, service models, global infrastructure, HA
2. [02-prerequisites.md](01-cloud-fundamentals/02-prerequisites.md) — **Free trial details**, required knowledge, CLI setup, verification
3. [03-service-comparison.md](01-cloud-fundamentals/03-service-comparison.md) — Service mapping across clouds
4. [04-backbone-network.md](01-cloud-fundamentals/04-backbone-network.md) — Global fiber, latency, private connectivity
5. [05-data-transfer-costs.md](01-cloud-fundamentals/05-data-transfer-costs.md) — Egress/ingress, bucket/log costs, LND cost model

### Phase 2: Cloud Architecture (Governance, IAM, Security)
**[02-cloud-architecture/00-index.md](02-cloud-architecture/00-index.md)**
1. [01-resource-hierarchy.md](02-cloud-architecture/01-resource-hierarchy.md) — Governance backbone: Azure (Entra→Mgmt Groups→Subs→RGs), GCP (Workspace→Org→Folders→Projects), AWS (Mgmt Account→OUs→Accounts)
2. [02-iam-at-levels.md](02-cloud-architecture/02-iam-at-levels.md) — **IAM at each level**: Entra ID vs Azure RBAC, Cloud Identity vs Org/Folder/Project IAM, IAM Identity Center vs Account IAM vs SCPs. Conditional Access, PIM, Entitlement Management
3. [03-architecture-comparison.md](02-cloud-architecture/03-architecture-comparison.md) — CSPM (Defender P2 vs Security Hub vs SCC), Productivity (M365 E5 vs Workspace), Governance, Compliance (Purview vs Cloud DLP/Vault vs Macie)
4. [04-security-networking.md](02-cloud-architecture/04-security-networking.md) — DDoS, WAF, Cloud NGFW, Bastion/IAP/Azure Bastion, VPN/SD-WAN/MPLS, PrivateLink/PSC/Private Endpoint, DNS, Load Balancing, K8s security, CSPM, vendors (Palo Alto, Fortinet, Check Point)
5. [05-federation-patterns.md](02-cloud-architecture/05-federation-patterns.md) — Cross-cloud workforce/workload federation, Patterns A/B/C

### Phase 3: Identity Fundamentals (SAML/OIDC)
**[04-identity-fundamentals/00-index.md](04-identity-fundamentals/00-index.md)**
1. [01-saml-oidc-fundamentals.md](04-identity-fundamentals/01-saml-oidc-fundamentals.md) — SAML 2.0/OIDC architecture, three URLs, flows, certs, tokens, mapping, trust boundaries

### Phase 4: Cloud Platform Guides (Cloud-Specific IAM)
**[05-cloud-platform-guides/00-index.md](05-cloud-platform-guides/00-index.md)**
1. [01-aws-iam.md](05-cloud-platform-guides/01-aws-iam.md) — IAM Core, Identity Center, SAML/OIDC, STS, IRSA, AWS as IdP
2. [02-gcp-iam.md](05-cloud-platform-guides/02-gcp-iam.md) — Cloud Identity, WIF (workforce/workload), Service Accounts
3. [03-azure-iam.md](05-cloud-platform-guides/03-azure-iam.md) — Entra ID vs Azure RBAC, Enterprise Apps vs App Regs, Managed Identities, Conditional Access, PIM

### Phase 5: Deployment Architecture (Patterns & Tutorials)
**[03-deployment-architecture/00-index.md](03-deployment-architecture/00-index.md)**
1. [01-patterns.md](03-deployment-architecture/01-patterns.md) — LND patterns: Standalone, HA, K8s, Serverless, Multi-Cloud
2. [02-aws-tutorial.md](03-deployment-architecture/02-aws-tutorial.md) — EC2 + EBS + NLB step-by-step
3. [03-gcp-tutorial.md](03-deployment-architecture/03-gcp-tutorial.md) — Compute Engine + PD + ILB
4. [04-azure-tutorial.md](03-deployment-architecture/04-azure-tutorial.md) — VM + Managed Disks + LB

### Phase 6: Reference
**[07-reference/00-index.md](07-reference/00-index.md)**
1. [01-cli-cheatsheet.md](07-reference/01-cli-cheatsheet.md) — Unified AWS/GCP/Azure CLI

---

## Quick Start

```bash
# Clone and serve locally
git clone https://github.com/ajettesla/cloud-plaform-lnd-guide
cd cloud-plaform-lnd-guide
# No Python dependencies needed — pure markdown documentation
```

## Cross-Reference System

| Notation | Meaning | Example |
|----------|---------|---------|
| `[§XX.Y]` | Section reference | `[§02.1]` → Resource Hierarchy |
| `[Figure N]` | Diagram reference | `[Figure 3]` → Architecture diagram |
| `[Table N]` | Table reference | `[Table 2]` → Cost comparison |
| `[Listing N]` | Code listing | `[Listing 4]` → Terraform module |

---

## License

This documentation is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).