---
title: "Deployment Architecture"
description: "LND deployment patterns and step-by-step tutorials for each cloud platform"
---

# Deployment Architecture — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-patterns.md](01-patterns.md) | **LND deployment patterns**: Standalone VM, Active-Passive HA, Active-Active Multi-Node, Kubernetes Native (EKS/GKE/AKS), Serverless/Event-Driven, Hybrid/Multi-Cloud. Decision matrix, trade-offs, cross-references to cloud architecture |
| 2 | [02-aws-tutorial.md](02-aws-tutorial.md) | **Step-by-step AWS**: EC2 + EBS + NLB deployment. Prerequisites, Terraform variables, verification, monitoring, backup, channel opening, cleanup, troubleshooting |
| 3 | [03-gcp-tutorial.md](03-gcp-tutorial.md) | **Step-by-step GCP**: Compute Engine + Persistent Disk + ILB deployment. Architecture, validation checklist |
| 4 | [04-azure-tutorial.md](04-azure-tutorial.md) | **Step-by-step Azure**: VM + Managed Disks + Load Balancer deployment. Architecture, validation checklist |

**Prerequisites**: Complete [Cloud Fundamentals](../01-cloud-fundamentals/00-index.md) and [Cloud Architecture](../02-cloud-architecture/00-index.md) first

**Next**: [Identity Fundamentals](../04-identity-fundamentals/00-index.md) — SAML/OIDC deep dive for federation setup