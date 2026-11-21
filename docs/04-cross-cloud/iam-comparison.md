---
title: "IAM Comparison: AWS, GCP, and Azure"
description: "Side-by-side comparison of Identity and Access Management across AWS, GCP, and Azure — roles, policies, federation, workload identities, and authorization models."
tags: [comparison, iam, aws, gcp, azure, roles, policies, federation]
cloud: all
level: 300
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS IAM User Guide"
  - "Google Cloud IAM Documentation"
  - "Microsoft Entra ID Documentation"
  - "docs/01-aws/iam.md"
  - "docs/02-gcp/iam.md"
  - "docs/03-azure/iam.md"
---

# Abstract

This document provides a side-by-side comparison of Identity and Access Management (IAM) across Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. It covers resource hierarchy, identity types, role/policy models, federation patterns, workload identities, and authorization evaluation. Each cloud's detailed implementation is documented in its respective folder: [§01-aws.iam], [§02-gcp.iam], [§03-azure.iam].

# 1. Resource Hierarchy & Governance Scope

| Concept | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Top-level governance** | AWS Organizations → Root → OUs | Organization resource → Folders | Management groups → Root management group |
| **Billing/quota boundary** | AWS Account | Project | Subscription |
| **Resource grouping** | Resource Groups (logical, not mandatory) | Project (mandatory container) | Resource Group (mandatory container) |
| **Policy attachment scopes** | Account, OU (SCPs), Resource | Organization, Folder, Project, Resource | Management group, Subscription, Resource Group, Resource |
| **Inheritance** | SCPs limit max permissions (don't grant) | Allow policies inherit down hierarchy | RBAC assignments inherit down scope hierarchy |

# 2. Identity Types

| Identity Category | AWS | GCP | Azure |
|-------------------|-----|-----|-------|
| **Human (managed directory)** | IAM Identity Center users / AD users | Cloud Identity / Google Workspace users | Entra ID users |
| **Human (federated)** | IAM Identity Center + external IdP (SAML+SCIM) / Direct IAM SAML | Workforce Identity Federation (SAML/OIDC, sync-less) | Entra ID user + Enterprise App SSO |
| **Application/Service (native)** | IAM Role (assumed by compute) | Service Account (attached to compute) | Managed Identity (system/user-assigned) |
| **Application/Service (external)** | IAM Role + STS (SAML/OIDC federation) | Workload Identity Federation (OIDC) | Managed Identity + Federated Credentials / App Registration |
| **Group construct** | IAM Groups (for IAM users only) | Google Groups (Cloud Identity/Workspace) | Entra ID Groups (security, Microsoft 365) |

# 3. Role & Policy Models

## 3.1 Policy Structure

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Policy format** | JSON document | Allow policy (JSON/YAML) | Role definition (ARM template/JSON) |
| **Attachment target** | Users, Groups, Roles, Resources | Principals in allow policy bindings | Security principals at scopes |
| **Permission granularity** | Action-level (service:action) | Permission-level (service.resource.verb) | Action-level (provider/resource/action) |
| **Data-plane vs control-plane** | Separate actions (e.g., s3:GetObject vs s3:CreateBucket) | Separate permissions (storage.objects.get vs storage.buckets.create) | DataActions in role definitions |

## 3.2 Role Types

| Role Type | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Predefined/Managed** | AWS managed policies (e.g., ReadOnlyAccess) | Predefined roles (e.g., roles/viewer) | Built-in roles (e.g., Reader, Contributor) |
| **Custom** | Customer managed policies | Custom roles | Custom roles |
| **Session/assumable** | IAM Roles (trust policy + permissions) | Service Account impersonation | N/A (uses role assignments) |
| **Template for accounts** | IAM Identity Center Permission Sets | N/A | N/A |

## 3.3 Policy Evaluation Logic

| Cloud | Evaluation Order |
|-------|------------------|
| **AWS** | 1. Explicit Deny → 2. Allow (identity/resource) → 3. Permission Boundaries → 4. Session Policies → 5. SCPs |
| **GCP** | 1. Allow policies (inherited) → 2. Deny policies (if configured) → 3. Organization Policy constraints |
| **Azure** | 1. Role assignments (inherited) → 2. Azure Policy (audit/deny) → 3. Management group policies |

# 4. Federation Patterns

## 4.1 Human Workforce Federation

| Pattern | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **External IdP (Entra/Okta)** | IAM Identity Center: SAML + SCIM provisioning | Workforce Identity Federation: SAML/OIDC, sync-less | Entra ID native (Enterprise App SAML / App Reg OIDC) |
| **Google Workspace as IdP** | IAM Identity Center: SAML + SCIM | Native (Cloud Identity) | Enterprise App SAML |
| **AWS Identity Center as IdP** | Native | Workforce Identity Federation (SAML) | Enterprise App SAML |
| **Key difference** | Requires user/group provisioning (SCIM/manual) | No provisioning needed (sync-less) | Entra ID is the IdP; others federate to it |

## 4.2 Workload Federation (Cross-Cloud)

| Source → Target | AWS | GCP | Azure |
|-----------------|-----|-----|-------|
| **Azure MI →** | IAM Role + OIDC provider (sts.amazonaws.com) | Workload Identity Federation (OIDC, azp mapping) | Native (Managed Identity) |
| **AWS Role/EC2 →** | Native (instance profile) | Workload Identity Federation (AWS STS GetCallerIdentity or OIDC) | Federated Credential on App Reg (issuer: sts.amazonaws.com) |
| **GCP SA →** | IAM Role + OIDC provider (accounts.google.com) | Native (attached SA) | Federated Credential on App Reg (issuer: accounts.google.com) |
| **GitHub Actions →** | IAM Role + OIDC provider (token.actions.githubusercontent.com) | Workload Identity Federation (OIDC, sub mapping) | Federated Credential on App Reg (issuer: token.actions.githubusercontent.com) |

# 5. Workload Identity Details

## 5.1 Native Workload Identity

| Cloud | Mechanism | Credential Delivery |
|-------|-----------|---------------------|
| **AWS** | IAM Role → Instance Profile / Task Role / IRSA | IMDS (EC2), Env vars (ECS/EKS), Projected volume (EKS) |
| **GCP** | Service Account attached to compute | Metadata server (VM), Env vars (Cloud Run/GKE), Workload Identity (GKE) |
| **Azure** | Managed Identity (system/user-assigned) | IMDS (VM), Azure Identity client library |

## 5.2 Cross-Cloud Workload Identity

| Cloud | Trust Configuration | Subject Mapping |
|-------|---------------------|-----------------|
| **AWS** | IAM OIDC Provider + Role trust policy | `sts.amazonaws.com:sub` (role session name) or `token.actions.githubusercontent.com:sub` |
| **GCP** | Workload Identity Pool + Provider (OIDC) | `assertion.azp` (Azure), `assertion.arn` (AWS), `assertion.sub` (GitHub) |
| **Azure** | Federated Credential on App Registration / User-assigned MI | `system:serviceaccount:ns:sa` (K8s), `repo:org/repo:ref` (GitHub) |

# 6. Authorization Scopes & Inheritance

| Scope Level | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| **Organization/Root** | AWS Organizations (SCPs only) | Organization (allow policies, org policies) | Management Group (RBAC, Azure Policy) |
| **Folder/OU** | OU (SCPs) | Folder (allow policies, org policies) | Management Group (RBAC) |
| **Account/Project/Subscription** | Account (IAM policies, resource policies) | Project (allow policies, org policies) | Subscription (RBAC) |
| **Resource Group** | N/A (Resource Groups are logical) | N/A (Project is container) | Resource Group (RBAC) |
| **Individual Resource** | Resource-based policies (S3, KMS, SQS) | Resource-level allow policies | Resource-level RBAC |

# 7. Least-Privilege Patterns

| Pattern | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Log writer to bucket** | `s3:PutObject` on specific bucket/prefix | `storage.objects.create` on specific bucket | `Storage Blob Data Contributor` on container |
| **Read-only auditor** | `ReadOnlyAccess` managed policy | `roles/viewer` predefined role | `Reader` built-in role |
| **Cross-account access** | AssumeRole with trust policy + ExternalId | Service Account impersonation (roles/iam.workloadIdentityUser) | Azure RBAC on subscription in other tenant (via Lighthouse) |
| **CI/CD deployments** | GitHub Actions OIDC → IAM Role | GitHub Actions OIDC → WIF → SA impersonation | GitHub Actions OIDC → Federated Credential → Azure RBAC |

# 8. Audit & Compliance

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Activity logging** | CloudTrail (management + data events) | Cloud Audit Logs (admin activity, data access) | Azure Activity Log + Resource Logs |
| **Policy compliance** | AWS Config + Conformance Packs | Organization Policy + Policy Controller | Azure Policy + Initiative definitions |
| **Access analysis** | IAM Access Analyzer | Policy Analyzer (recommender) | Azure AD Access Reviews |
| **Permission boundaries** | Permission Boundaries | Deny Policies (preview) | Azure Policy (deny effect) |

# 9. Quick Reference: Service Mapping

| Function | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **Managed directory** | IAM Identity Center | Cloud Identity / Workspace | Entra ID |
| **SSO portal** | AWS Access Portal | Google Cloud Console (federated) | My Apps / Azure Portal |
| **Service accounts** | IAM Roles | Service Accounts | Managed Identities / Service Principals |
| **Workload federation** | STS AssumeRoleWithWebIdentity | Workload Identity Federation | Federated Identity Credentials |
| **Human federation** | IAM Identity Center (SAML+SCIM) | Workforce Identity Federation | Enterprise Apps (SAML) / App Regs (OIDC) |
| **Policy language** | JSON | CEL (conditions) / JSON/YAML | ARM JSON / Bicep |
| **Guardrails** | SCPs | Organization Policies | Azure Policy |
| **Access analyzer** | IAM Access Analyzer | Policy Analyzer | Azure AD Access Reviews |

# 10. Detailed Guides

- **AWS IAM**: [§01-aws.iam]
- **GCP IAM**: [§02-gcp.iam]
- **Azure IAM**: [§03-azure.iam]
- **Identity Fundamentals (SAML/OIDC)**: [§05-identity-access.idp-sp-fundamentals]
- **Cross-Cloud Federation Patterns**: [§04-cross-cloud.identity-federation-patterns]
- **Cloud Architecture Comparison**: [§04-cross-cloud.cloud-architecture-comparison]

# References

[1] AWS, "IAM User Guide," https://docs.aws.amazon.com/IAM/latest/UserGuide/
[2] Google Cloud, "IAM Documentation," https://cloud.google.com/iam/docs/
[3] Microsoft, "Microsoft Entra ID Documentation," https://learn.microsoft.com/entra/
[4] AWS, "IAM Identity Center," https://docs.aws.amazon.com/singlesignon/latest/userguide/
[5] Google Cloud, "Workforce Identity Federation," https://cloud.google.com/iam/docs/workforce-identity-federation
[6] Google Cloud, "Workload Identity Federation," https://cloud.google.com/iam/docs/workload-identity-federation
[7] Microsoft, "Managed Identities," https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/
[8] Microsoft, "Workload Identity Federation," https://learn.microsoft.com/entra/workload-id/