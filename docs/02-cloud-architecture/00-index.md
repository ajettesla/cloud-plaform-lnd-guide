---
title: "Cloud Architecture"
description: "Resource hierarchy, IAM at each governance level, security services, federation patterns, and cross-cloud comparison"
---

# Cloud Architecture — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-resource-hierarchy.md](01-resource-hierarchy.md) | **Governance backbone**: Azure (Entra Tenant → Mgmt Groups → Subscriptions → RGs), GCP (Workspace → Org → Folders → Projects), AWS (Mgmt Account → OUs → Accounts). Billing boundaries, policy inheritance (Azure Policy, Org Policies, SCPs), hard isolation |
| 2 | [02-iam-at-levels.md](02-iam-at-levels.md) | **IAM at each governance layer**: What you configure at Entra ID vs Azure RBAC vs Mgmt Group vs Subscription vs RG. GCP: Cloud Identity vs Org vs Folder vs Project IAM. AWS: IAM Identity Center vs Account IAM vs SCPs. Conditional Access, Entitlement Management, PIM |
| 3 | [03-architecture-comparison.md](03-architecture-comparison.md) | Comprehensive architecture comparison: CSPM (Defender for Cloud P2 vs Security Hub vs SCC Premium), productivity (M365 E5 vs Workspace Enterprise Plus), governance, compliance (Purview vs Cloud DLP/Vault vs Macie) |
| 4 | [04-security-networking.md](04-security-networking.md) | **Security services deep dive**: DDoS (Shield/Armor/Azure DDoS), WAF, Cloud NGFW (Network Firewall/Cloud NGFW/Azure Firewall), Bastion/IAP/Azure Bastion, VPN/SD-WAN/MPLS, PrivateLink/PSC/Private Endpoint, DNS, Load Balancing, K8s security, CSPM, third-party vendors (Palo Alto, Fortinet, Check Point) |
| 5 | [05-federation-patterns.md](05-federation-patterns.md) | Cross-cloud workforce/workload federation: Entra→GCP (SAML/OIDC), Entra→AWS (Identity Center), GCP→AWS, Azure→GCP, workload identity (Azure MI→GCP, AWS IRSA→GCP, GitHub→all), Patterns A/B/C (Central IdP, Workload Mesh, Hybrid) |

**Next**: [Deployment Architecture](../03-deployment-architecture/00-index.md) — LND deployment patterns and step-by-step tutorials