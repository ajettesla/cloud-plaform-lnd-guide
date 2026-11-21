---
title: "Cross-Cutting Concerns"
description: "Cross-cutting concerns — federation patterns, billing, compliance, cost optimization"
---

# Cross-Cutting — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-federation-patterns.md](01-federation-patterns.md) | **Cross-cloud federation**: Workforce (Entra→GCP SAML/OIDC, Entra→AWS Identity Center, GCP→AWS, Azure→GCP), Workload (Azure MI→GCP, AWS IRSA→GCP, GitHub→all), Patterns A/B/C (Central IdP, Workload Mesh, Hybrid) |
| 2 | [02-compliance.md](02-compliance.md) | **Compliance**: GDPR, policy enforcement, CSPM comparison (Defender P2 vs Security Hub vs SCC), Purview vs Cloud DLP/Vault vs Macie, audit trails, data residency |
| 3 | [03-cost-optimization.md](03-cost-optimization.md) | **Cost optimization**: right-sizing, reserved/committed, spot/preemptible, Graviton/ARM, private connectivity, LND-specific model |

**Content to be created** — 02, 03 to be created; 01 available

**Cross-references**: IAM in [03-iam](../03-iam/00-index.md), Security in [04-security](../04-security/00-index.md), Billing in [07-billing](../07-billing/00-index.md), Cloud Architecture in [01-cloud-architecture](../01-cloud-architecture/00-index.md)
