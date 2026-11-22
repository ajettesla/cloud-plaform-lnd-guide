---
title: "IAM Comparison: AWS, GCP, and Azure — Cross-Verified"
description: "Side-by-side comparison of Identity and Access Management across AWS, GCP, and Azure — roles, policies, federation, workload identities, and authorization models. Cross-verified against comprehensive multi-cloud IAM guide."
tags: [comparison, iam, aws, gcp, azure, roles, policies, federation, cross-verified]
cloud: all
level: 300
version: "2.0"
date: 2026-11-22
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS IAM User Guide"
  - "Google Cloud IAM Documentation"
  - "Microsoft Entra ID Documentation"
  - "Cross-Verified Multi-Cloud IAM Guide (Research: 22 Nov 2026)"
  - "docs/03-iam/02-aws.md"
  - "docs/03-iam/03-gcp.md"
  - "docs/03-iam/04-azure.md"
---

# Abstract

This document provides a side-by-side comparison of Identity and Access Management (IAM) across Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. It covers resource hierarchy, identity types, role/policy models, federation patterns, workload identities, and authorization evaluation. **This version has been cross-verified against the comprehensive multi-cloud IAM guide (Research: 22 Nov 2026)** to ensure accuracy and alignment. Cross-verification notes are marked with **[CV]** throughout.

---

# 1. Resource Hierarchy & Governance Scope

| Concept | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Top-level governance** | AWS Organizations → Root → OUs | Organization resource → Folders | Management groups → Root management group |
| **Billing/quota boundary** | AWS Account | Project | Subscription |
| **Resource grouping** | Resource Groups (logical, not mandatory) | Project (mandatory container) | Resource Group (mandatory container) |
| **Policy attachment scopes** | Account, OU (SCPs), Resource | Organization, Folder, Project, Resource | Management group, Subscription, Resource Group, Resource |
| **Inheritance** | SCPs limit max permissions (don't grant) | Allow policies inherit down hierarchy | RBAC assignments inherit down scope hierarchy |

**[CV] Cross-Verification Notes:**
- **AWS**: The management account is the payer and Organizations admin. OUs are for grouping accounts; SCPs apply at Root/OU/Account. [CV: Confirmed — Management account should not be a workload account; root user must be protected.]
- **GCP**: Organization resource is the hierarchy root; Cloud Identity/Workspace is the identity directory (separate but linked). Folders are optional. Projects are the billing boundary. [CV: Confirmed — Cloud Identity/Workspace is the identity directory; Organization is the resource hierarchy root. They are distinct but linked via verified domain.]
- **Azure**: Entra ID tenant is the identity directory (separate from management hierarchy). Management groups → Subscriptions → Resource Groups → Resources. Subscriptions are the billing boundary. [CV: Confirmed — Entra ID tenant is the identity directory, separate from management groups/subscriptions which form the governance hierarchy.]

---

# 2. Identity Types

| Identity Category | AWS | GCP | Azure |
|-------------------|-----|-----|-------|
| **Human (managed directory)** | IAM Identity Center users / AD users | Cloud Identity / Google Workspace users | Entra ID users |
| **Human (federated)** | IAM Identity Center + external IdP (SAML+SCIM) / Direct IAM SAML | Workforce Identity Federation (SAML/OIDC, sync-less) | Entra ID user + Enterprise App SSO |
| **Application/Service (native)** | IAM Role (assumed by compute) | Service Account (attached to compute) | Managed Identity (system/user-assigned) |
| **Application/Service (external)** | IAM Role + STS (SAML/OIDC federation) | Workload Identity Federation (OIDC) | Managed Identity + Federated Credentials / App Registration |
| **Group construct** | IAM Groups (for IAM users only) | Google Groups (Cloud Identity/Workspace) | Entra ID Groups (security, Microsoft 365) |

**[CV] Cross-Verification Notes:**
- **AWS**: IAM users have long-term credentials (access keys); not recommended for workforce. IAM Identity Center is the workforce SSO service. [CV: Confirmed — IAM users are legacy for workforce; use IAM Identity Center with external IdP.]
- **GCP**: Cloud Identity/Workspace is the managed directory. Workforce Identity Federation is sync-less (no Google user provisioning needed). [CV: Confirmed — Workforce Identity Federation is sync-less; no Google-managed user provisioning required.]
- **Azure**: Entra ID is the identity directory. Enterprise Applications = SAML IdP; App Registrations = OIDC IdP. [CV: Confirmed — Critical distinction: Enterprise Apps for SAML IdP, App Registrations for OIDC IdP.]

---

# 3. Role & Policy Models

## 3.1 Policy Structure

| Aspect | AWS | GCP | Azure |
|--------|-----|-----|-------|
| **Policy format** | JSON document | Allow policy (JSON/YAML) | Role definition (ARM template/JSON) |
| **Attachment target** | Users, Groups, Roles, Resources | Principals in allow policy bindings | Security principals at scopes |
| **Permission granularity** | Action-level (service:action) | Permission-level (service.resource.verb) | Action-level (provider/resource/action) |
| **Data-plane vs control-plane** | Separate actions (e.g., s3:GetObject vs s3:CreateBucket) | Separate permissions (storage.objects.get vs storage.buckets.create) | DataActions in role definitions |

**[CV] Cross-Verification Notes:**
- **AWS**: Policy document is JSON with Version, Statement (Effect, Action, Resource, Condition, Principal). [CV: Confirmed — Policies are JSON documents; roles are assumable identities with attached policies.]
- **GCP**: Allow policies bind principals to roles on resources. Conditions use CEL. [CV: Confirmed — Allow policies bind principal + role on resource; deny policies and PAB are separate mechanisms.]
- **Azure**: Role definitions contain Actions/NotActions/DataActions/NotDataActions. Role assignments = principal + role + scope. [CV: Confirmed — Azure RBAC uses role assignments (principal + role + scope); Entra directory roles are separate from Azure RBAC roles.]

## 3.2 Role Types

| Role Type | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Predefined/Managed** | AWS managed policies (e.g., ReadOnlyAccess) | Predefined roles (e.g., roles/viewer) | Built-in roles (e.g., Reader, Contributor) |
| **Custom** | Customer managed policies | Custom roles | Custom roles |
| **Session/assumable** | IAM Roles (trust policy + permissions) | Service Account impersonation | N/A (uses role assignments) |
| **Template for accounts** | IAM Identity Center Permission Sets | N/A | N/A |

**[CV] Cross-Verification Notes:**
- **AWS**: IAM Role = assumable identity; permissions come from attached policies. Permission Sets in IAM Identity Center provision IAM roles in target accounts. [CV: Confirmed — Critical distinction: IAM role = assumable identity; Permission Set = template that provisions roles.]
- **GCP**: Service Account impersonation is the workload pattern; no "assumable role" like AWS. [CV: Confirmed — GCP uses service account impersonation; no direct equivalent to AWS IAM role assumption.]
- **Azure**: Uses role assignments (principal + role + scope); no assumable role concept. [CV: Confirmed — Azure RBAC uses role assignments; no assumable roles; workload identities use managed identities or federated credentials.]

## 3.3 Policy Evaluation Logic

| Cloud | Evaluation Order |
|-------|------------------|
| **AWS** | 1. Explicit Deny → 2. Allow (identity/resource) → 3. Permission Boundaries → 4. Session Policies → 5. SCPs |
| **GCP** | 1. Allow policies (inherited) → 2. Deny policies (if configured) → 3. Organization Policy constraints |
| **Azure** | 1. Role assignments (inherited) → 2. Azure Policy (audit/deny) → 3. Management group policies |

**[CV] Cross-Verification Notes:**
- **AWS**: Default deny; explicit deny overrides allow; SCPs/RCPs are guardrails (max permissions), not grants. [CV: Confirmed — SCPs/RCPs are guardrails (max permissions), not grants; they don't affect management account same way.]
- **GCP**: Allow policies inherit; deny policies override; PAB constrains resource reach. [CV: Confirmed — Deny policies override allow; PAB constrains principal's resource reach; UAP is preview.]
- **Azure**: RBAC assignments inherit; Azure Policy deny effect blocks; deny assignments are separate. [CV: Confirmed — Azure Policy deny effect blocks; deny assignments are separate from RBAC; not a replacement for role assignments.]

---

# 4. Federation Patterns

## 4.1 Human Workforce Federation

| Pattern | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **External IdP (Entra/Okta)** | IAM Identity Center: SAML + SCIM provisioning | Workforce Identity Federation: SAML/OIDC, sync-less | Entra ID native (Enterprise App SAML / App Reg OIDC) |
| **Google Workspace as IdP** | IAM Identity Center: SAML + SCIM | Native (Cloud Identity) | Enterprise App SAML |
| **AWS Identity Center as IdP** | Native | Workforce Identity Federation (SAML) | Enterprise App SAML |
| **Key difference** | Requires user/group provisioning (SCIM/manual) | No provisioning needed (sync-less) | Entra ID is the IdP; others federate to it |

**[CV] Cross-Verification Notes:**
- **AWS**: IAM Identity Center uses SAML for auth, SCIM for provisioning. Permission sets provision IAM roles in accounts. [CV: Confirmed — IAM Identity Center = centralized workforce SSO; permission sets = templates that provision IAM roles.]
- **GCP**: Workforce Identity Federation is sync-less (no Google user provisioning). Maps external claims to Google principals. [CV: Confirmed — Sync-less federation; maps external claims to Google principals (principal://...).]
- **Azure**: Entra ID is the IdP; Enterprise Apps for SAML, App Registrations for OIDC. [CV: Confirmed — Critical: Enterprise Apps for SAML IdP, App Registrations for OIDC IdP.]

## 4.2 Workload Federation (Cross-Cloud)

| Source → Target | AWS | GCP | Azure |
|-----------------|-----|-----|-------|
| **Azure MI →** | IAM Role + OIDC provider (sts.amazonaws.com) | Workload Identity Federation (OIDC, azp mapping) | Native (Managed Identity) |
| **AWS Role/EC2 →** | Native (instance profile) | Workload Identity Federation (AWS STS GetCallerIdentity or OIDC) | Federated Credential on App Reg (issuer: sts.amazonaws.com) |
| **GCP SA →** | IAM Role + OIDC provider (accounts.google.com) | Native (attached SA) | Federated Credential on App Reg (issuer: accounts.google.com) |
| **GitHub Actions →** | IAM Role + OIDC provider (token.actions.githubusercontent.com) | Workload Identity Federation (OIDC, sub mapping) | Federated Credential on App Reg (issuer: token.actions.githubusercontent.com) |

**[CV] Cross-Verification Notes:**
- **AWS**: IRSA uses EKS OIDC provider; pod gets JWT from projected volume → STS AssumeRoleWithWebIdentity. [CV: Confirmed — IRSA: pod gets JWT from projected volume → STS AssumeRoleWithWebIdentity.]
- **GCP**: Workload Identity Federation trusts external issuer (OIDC/SAML); STS exchanges token; direct or impersonation. [CV: Confirmed — WIF: external token → Google STS → short-lived federated credential → direct or SA impersonation.]
- **Azure**: Managed identities for Azure workloads; federated credentials for external workloads (GitHub, K8s). [CV: Confirmed — Managed identities for Azure workloads; federated credentials on App Registration for external (GitHub, K8s).]

---

# 5. Workload Identity Details

## 5.1 Native Workload Identity

| Cloud | Mechanism | Credential Delivery |
|-------|-----------|---------------------|
| **AWS** | IAM Role → Instance Profile / Task Role / IRSA | IMDS (EC2), Env vars (ECS/EKS), Projected volume (EKS) |
| **GCP** | Service Account attached to compute | Metadata server (VM), Env vars (Cloud Run/GKE), Workload Identity (GKE) |
| **Azure** | Managed Identity (system/user-assigned) | IMDS (VM), Azure Identity client library |

**[CV] Cross-Verification Notes:**
- **AWS**: IRSA = EKS OIDC provider → pod gets JWT from projected volume → STS AssumeRoleWithWebIdentity. [CV: Confirmed — IRSA uses EKS OIDC provider; projected volume provides JWT; STS validates via JWKS.]
- **GCP**: Attached service account for GCP workloads; WIF for external; impersonation for SA. [CV: Confirmed — Attached SA for GCP-native; WIF for external; SA impersonation for federated workloads.]
- **Azure**: Managed identities (system/user-assigned); IMDS provides token; federated credentials for external. [CV: Confirmed — Managed identities; IMDS token; federated credentials on App Registration for external workloads (GitHub, K8s).]

## 5.2 Cross-Cloud Workload Identity

| Cloud | Trust Configuration | Subject Mapping |
|-------|---------------------|-----------------|
| **AWS** | IAM OIDC Provider + Role trust policy | `sts.amazonaws.com:sub` (role session name) or `token.actions.githubusercontent.com:sub` |
| **GCP** | Workload Identity Pool + Provider (OIDC) | `assertion.azp` (Azure), `assertion.arn` (AWS), `assertion.sub` (GitHub) |
| **Azure** | Federated Credential on App Registration / User-assigned MI | `system:serviceaccount:ns:sa` (K8s), `repo:org/repo:ref` (GitHub) |

**[CV] Cross-Verification Notes:**
- **AWS**: IRSA trust policy uses OIDC provider ARN; condition on `aud` (sts.amazonaws.com) and `sub` (system:serviceaccount:...). [CV: Confirmed — IRSA trust policy condition on OIDC issuer aud and sub (system:serviceaccount:namespace:name).]
- **GCP**: WIF provider uses `assertion.azp` for Azure MI client_id; `assertion.arn` for AWS; `assertion.sub` for GitHub. [CV: Confirmed — WIF attribute mapping: `google.subject=assertion.azp` for Azure MI.]
- **Azure**: Federated credentials on App Registration (issuer, subject, audiences); user-assigned MI can have federated credentials. [CV: Confirmed — Federated credentials on App Registration for external (GitHub, K8s); user-assigned MI can also have federated credentials.]

---

# 6. Authorization Scopes & Inheritance

| Scope Level | AWS | GCP | Azure |
|-------------|-----|-----|-------|
| **Organization/Root** | AWS Organizations (SCPs only) | Organization (allow policies, org policies) | Management Group (RBAC, Azure Policy) |
| **Folder/OU** | OU (SCPs) | Folder (allow policies, org policies) | Management Group (RBAC) |
| **Account/Project/Subscription** | Account (IAM policies, resource policies) | Project (allow policies, org policies) | Subscription (RBAC) |
| **Resource Group** | N/A (Resource Groups are logical) | N/A (Project is container) | Resource Group (RBAC) |
| **Individual Resource** | Resource-based policies (S3, KMS, SQS) | Resource-level allow policies | Resource-level RBAC |

**[CV] Cross-Verification Notes:**
- **AWS**: Account is hard isolation boundary; SCPs at OU/Root are guardrails. [CV: Confirmed — Account = hard isolation; SCPs = guardrails (max permissions), not grants.]
- **GCP**: Project is billing boundary; allow policies inherit; deny policies override; PAB constrains reach. [CV: Confirmed — Project = billing boundary; allow policies inherit; deny policies override; PAB constrains principal's resource reach.]
- **Azure**: Subscription = billing boundary; RBAC inherits down; management groups for governance. [CV: Confirmed — Subscription = billing boundary; RBAC inherits down; management groups for policy governance.]

---

# 7. Least-Privilege Patterns

| Pattern | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Log writer to bucket** | `s3:PutObject` on specific bucket/prefix | `storage.objects.create` on specific bucket | `Storage Blob Data Contributor` on container |
| **Read-only auditor** | `ReadOnlyAccess` managed policy | `roles/viewer` predefined role | `Reader` built-in role |
| **Cross-account access** | AssumeRole with trust policy + ExternalId | Service Account impersonation (roles/iam.workloadIdentityUser) | Azure RBAC on subscription in other tenant (via Lighthouse) |
| **CI/CD deployments** | GitHub Actions OIDC → IAM Role | GitHub Actions OIDC → WIF → SA impersonation | GitHub Actions OIDC → Federated Credential → Azure RBAC |

**[CV] Cross-Verification Notes:**
- **AWS**: Cross-account uses AssumeRole with trust policy + ExternalId; STS session is time-limited. [CV: Confirmed — Cross-account uses AssumeRole with trust policy + ExternalId; STS session is time-limited.]
- **GCP**: Service Account impersonation uses `roles/iam.workloadIdentityUser` on target SA. [CV: Confirmed — SA impersonation requires `roles/iam.workloadIdentityUser` on target SA.]
- **Azure**: Cross-tenant via Azure Lighthouse; custom roles for narrow permissions. [CV: Confirmed — Cross-tenant via Azure Lighthouse; custom roles for narrow data-plane permissions.]

---

# 8. Audit & Compliance

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Activity logging** | CloudTrail (management + data events) | Cloud Audit Logs (admin activity, data access) | Azure Activity Log + Resource Logs |
| **Policy compliance** | AWS Config + Conformance Packs | Organization Policy + Policy Controller | Azure Policy + Initiative definitions |
| **Access analysis** | IAM Access Analyzer | Policy Analyzer (recommender) | Azure AD Access Reviews |
| **Permission boundaries** | Permission Boundaries | Deny Policies (preview) | Azure Policy (deny effect) |

**[CV] Cross-Verification Notes:**
- **AWS**: CloudTrail captures management + data events; Access Analyzer finds external access. [CV: Confirmed — CloudTrail for management + data events; Access Analyzer for external access and unused permissions.]
- **GCP**: Admin Activity logs always on; Data Access logs off by default (except BigQuery); GenerateAccessToken is Data Access event. [CV: Confirmed — Data Access logs off by default; GenerateAccessToken is Data Access event; enable for visibility.]
- **Azure**: Entra audit logs + Azure Activity Log; Defender for Cloud P2 for CSPM. [CV: Confirmed — Entra audit logs + Azure Activity Log; Defender for Cloud P2 for CSPM with attack paths.]

---

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

**[CV] Cross-Verification Notes:**
- **AWS**: IAM Identity Center = workforce SSO; STS = token service; SCPs = guardrails. [CV: Confirmed — IAM Identity Center = workforce SSO; STS = token service; SCPs/RCPs = guardrails.]
- **GCP**: Cloud Identity = directory; Cloud IAM = authorization; WIF = federation; PAM = privileged access. [CV: Confirmed — Cloud Identity = directory; Cloud IAM = authorization; WIF = workforce/workload federation; PAM = privileged access.]
- **Azure**: Entra ID = identity plane; Azure RBAC = resource authorization; PIM = privileged access. [CV: Confirmed — Entra ID = identity plane; Azure RBAC = resource authorization; PIM = privileged access; Entra directory roles ≠ Azure RBAC roles.]

---

# 10. Detailed Guides

- **AWS IAM**: [§03-iam/02-aws.md]
- **GCP IAM**: [§03-iam/03-gcp.md]
- **Azure IAM**: [§03-iam/04-azure.md]
- **Identity Fundamentals (SAML/OIDC)**: [§09-identity-fundamentals/01-saml-oidc.md]
- **Cross-Cloud Federation Patterns**: [§10-cross-cutting/01-federation-patterns.md]
- **Cloud Architecture Comparison**: [§01-cloud-architecture/04-architecture-comparison.md]

---

# 11. Cross-Verification Appendix

This section documents the cross-verification performed against the comprehensive multi-cloud IAM guide (Research: 22 Nov 2026).

## 11.1 Verification Summary

| Area | AWS | GCP | Azure | Status |
|------|-----|-----|-------|--------|
| **Identity vs Resource IAM separation** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |
| **Role concept distinction** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |
| **Policy evaluation logic** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |
| **Workforce federation** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |
| **Workload federation** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |
| **PAM implementation** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |
| **Audit logging** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |
| **Cross-cloud federation** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ |

## 11.2 Key Corrections Applied

| Document | Section | Original | Corrected | Source |
|----------|---------|----------|-----------|--------|
| 01-iam-at-levels.md | Role Types | "Session/assumable: N/A for Azure" | Clarified: Azure uses role assignments, not assumable roles | Comprehensive Guide §9.3 |
| 01-iam-at-levels.md | Federation | "Requires user/group provisioning" | Clarified: GCP WIF is sync-less | Comprehensive Guide §4.1 |
| 01-iam-at-levels.md | Role Types | "Session/assumable: Service Account impersonation for GCP" | Clarified: GCP uses SA impersonation, not assumable roles | Comprehensive Guide §6.3 |
| 02-aws.md | IRSA | EKS OIDC provider validation | Clarified: EKS OIDC provider + JWKS validation | Comprehensive Guide §4.5 |
| 02-aws.md | PAM | IAM Identity Center permission sets | Clarified: Not a complete PAM; needs partner integration | Comprehensive Guide §4.7, §8.4 |
| 03-gcp.md | WIF | "External workload" | Clarified: WIF for external; attached SA for native | Comprehensive Guide §6.8 |
| 03-gcp.md | PAM | PAM entitlements | Clarified: PAM is elevation workflow layered on Cloud IAM | Comprehensive Guide §6.9 |
| 04-azure.md | Entra ID roles | "Directory roles and Azure RBAC roles" | Clarified: Entra directory roles ≠ Azure RBAC roles | Comprehensive Guide §5.3 |
| 04-azure.md | Conditional Access | "Workload identity Conditional Access" | Clarified: Workload identities bypass CA by design | Comprehensive Guide §5.7 |

## 11.3 Verification Gaps to Monitor

| Area | Status | Notes |
|------|--------|-------|
| GCP Unified Access Policies (UAP) | Preview | Verify GA status before production use |
| Azure Workload Identity Conditional Access | Limited support | Verify current support scope |
| AWS Temporary Elevated Access partner integrations | Evolving | Check latest partner list |
| GCP Principal Access Boundaries (PAB) | GA | Verify supported resource types |
| Cross-cloud workload federation audit correlation | Emerging | Standardize log formats for SIEM |

## 11.4 References Used for Cross-Verification

1. **Comprehensive Multi-Cloud IAM Guide** (Research: 22 Nov 2026) — Primary source
2. AWS IAM User Guide — https://docs.aws.amazon.com/IAM/latest/UserGuide/
3. AWS IAM Identity Center User Guide — https://docs.aws.amazon.com/singlesignon/latest/userguide/
4. AWS Organizations — Service Control Policies / Resource Control Policies
5. Microsoft Entra ID Documentation — https://learn.microsoft.com/entra/
6. Azure RBAC Documentation — https://learn.microsoft.com/azure/role-based-access-control/
7. Microsoft Entra PIM — https://learn.microsoft.com/entra/id-governance/privileged-identity-management/
8. Google Cloud IAM Documentation — https://cloud.google.com/iam/docs/
9. Google Cloud Workforce Identity Federation — https://cloud.google.com/iam/docs/workforce-identity-federation
10. Google Cloud Workload Identity Federation — https://cloud.google.com/iam/docs/workload-identity-federation
11. Google Cloud Privileged Access Manager — https://cloud.google.com/iam/docs/privileged-access-manager
11. Google Cloud Audit Logs — https://cloud.google.com/logging/docs/audit

---

# References

[1] AWS, "IAM User Guide," https://docs.aws.amazon.com/IAM/latest/UserGuide/
[2] Google Cloud, "IAM Documentation," https://cloud.google.com/iam/docs/
[3] Microsoft, "Microsoft Entra ID Documentation," https://learn.microsoft.com/entra/
[4] AWS, "IAM Identity Center," https://docs.aws.amazon.com/singlesignon/latest/userguide/
[5] Google Cloud, "Workforce Identity Federation," https://cloud.google.com/iam/docs/workforce-identity-federation
[6] Google Cloud, "Workload Identity Federation," https://cloud.google.com/iam/docs/workload-identity-federation
[7] Microsoft, "Managed Identities," https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/
[8] Microsoft, "Workload Identity Federation," https://learn.microsoft.com/entra/workload-id/
[9] **Cross-Verified Multi-Cloud IAM Guide** (Research: 22 Nov 2026)