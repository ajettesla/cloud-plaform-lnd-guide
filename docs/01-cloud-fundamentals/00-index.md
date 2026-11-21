---
title: "Cloud Fundamentals"
description: "Start here: Cloud basics, prerequisites, service comparison, global networking, and data transfer costs"
---

# Cloud Fundamentals — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-overview.md](01-overview.md) | What is cloud, service models (IaaS/PaaS/SaaS), deployment models, shared responsibility, global infrastructure (regions, AZs, edge), high availability principles |
| 2 | [02-prerequisites.md](02-prerequisites.md) | Required knowledge (Bitcoin/LN, cloud basics, IaC), **free trial details for AWS/GCP/Azure** (including GCP ₹3000 card hold, no Admin Console), CLI setup, Terraform, SSH keys, verification checklist |
| 3 | [03-service-comparison.md](03-service-comparison.md) | Side-by-side service mapping: compute, storage, networking, security, monitoring, Kubernetes, pricing estimates |
| 4 | [04-backbone-network.md](04-backbone-network.md) | Global fiber ownership (AWS/GCP/Azure subsea cables), network tiers (Premium vs Standard), private connectivity (Direct Connect, Cloud Interconnect, ExpressRoute), latency measurements, LND implications |
| 5 | [05-data-transfer-costs.md](05-data-transfer-costs.md) | **Egress/ingress pricing**, cross-zone (AWS charges, GCP/Azure free), cross-region, inter-cloud, object storage classes, log costs, block storage, LND node cost model |

**Next**: [Cloud Architecture](../02-cloud-architecture/00-index.md) — Governance hierarchy, IAM at each level, security services, federation patterns