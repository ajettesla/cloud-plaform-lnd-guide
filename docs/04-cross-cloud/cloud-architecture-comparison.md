# Azure, Google Cloud, and AWS
## A practical comparison of resource hierarchy, identity, federation, IAM, and log-pipeline services

Prepared as a learning reference for a reader familiar with Microsoft Azure who is learning Google Cloud and wants AWS included as a third comparison. This document consolidates the concepts discussed so far and adds the closest AWS counterparts.

Research date: 21 November 2026  |  Evidence standard: official Microsoft, Google Cloud, and AWS documentation. Product behavior can change; verify the cited vendor pages before production implementation.

> **How to read the comparisons.** “Closest equivalent” means similar purpose, not identical implementation. Every cloud has different resource boundaries, identity models, policy evaluation, and service behavior. Where there is no direct equivalent, the table says so instead of forcing a one-to-one mapping.

# Contents

- 1. Executive comparison and the right mental model
- 2. Cloud resource hierarchy: tenant, organization, subscription, project, account, resource group
- 3. Identity plane: Entra ID, Cloud Identity / Google Workspace, AWS IAM Identity Center
- 4. Human federation: SAML and OIDC across the three clouds
- 5. SAML certificates, OIDC tokens, and trust validation
- 6. Workload identities and cross-cloud access
- 7. IAM and authorization: scopes, roles, policies, and inheritance
- 8. Services for a future security-log collection pipeline
- 9. Security design checklist and practical learning sequence
- 10. Glossary and official references

# 1. Executive comparison and the right mental model

The cleanest mental model is to separate three planes:

| Plane | Question it answers | Azure | Google Cloud | AWS |
| --- | --- | --- | --- | --- |
| Resource / governance plane | Where do cloud resources live, and how are they grouped and governed? | Management groups → subscriptions → resource groups → resources | Organization → folders → projects → resources | AWS Organizations → root → OUs → accounts → resources |
| Identity plane | Who or what is requesting access, and how do they authenticate? | Microsoft Entra ID: users, groups, app registrations, service principals, managed identities | Cloud Identity / Google Workspace for managed users; Workforce and Workload Identity Federation for external principals; service accounts for workloads | IAM users and roles; IAM Identity Center for workforce SSO and account access; external IdPs can be connected |
| Authorization plane | What can the authenticated principal do, and at what scope? | Azure RBAC role assignments at management group, subscription, resource group, or resource | Cloud IAM allow policies at organization, folder, project, and supported resource scopes | IAM identity/resource policies, role trust policies, permission sets, and Organizations guardrails such as SCPs |

> **Core rule.** Authentication is not authorization. An employee can successfully authenticate with Entra ID, Okta, Google, or another IdP and still have no permission to view a project, subscription, or AWS account. The destination cloud must separately authorize the resulting principal.

The most important differences to retain:

- Google Cloud Organization is a resource-hierarchy root; Cloud Identity / Google Workspace is the managed identity directory associated with that organization. They are related but not the same object. [1][2]
- An Azure subscription, a Google Cloud project, and an AWS account are useful high-level comparisons, but they do not have identical billing, isolation, governance, or service semantics. [1][3][5]
- Google Workforce Identity Federation is for people. Google Workload Identity Federation is for applications and compute workloads. [7][8]
- AWS IAM Identity Center with an external IdP uses SAML for sign-in and SCIM or manual provisioning to make users and groups available for assignments. Direct Google Workforce Identity Federation is designed to avoid synchronizing external workforce accounts into Google-managed identities. [7][11][12]

# 2. Cloud resource hierarchy

## 2.1 Azure: Entra tenant and Azure resource hierarchy

```text
Microsoft Entra ID tenant (directory)
└── Tenant root management group
    └── Management groups (optional, nested)
        └── Subscriptions
            └── Resource groups
                └── Resources (VMs, VNets, storage accounts, etc.)
```

The Entra tenant is the identity directory. Azure management groups sit above subscriptions and provide a governance scope. Azure RBAC supports role assignments at management group, subscription, resource group, and individual resource scopes; assignments at higher scopes are inherited by lower scopes. A subscription contains resource groups, and a resource group is a lifecycle and management container for Azure resources. [3][4]

## 2.2 Google Cloud: identity directory versus Organization resource

```text
Cloud Identity / Google Workspace account (managed identity directory)
                 │ associated with
                 ▼
Google Cloud Organization (resource-hierarchy root)
└── Folders (optional; can be nested)
    └── Projects
        └── Resources (VMs, VPC networks, Cloud Storage buckets, etc.)
```

Cloud Identity / Google Workspace manages the company’s Google identities. The Google Cloud Organization resource is the top node in the Google Cloud resource hierarchy. A managed Google identity account is a prerequisite for the Organization resource, and a Google Workspace or Cloud Identity account is associated with one Organization resource. Do not call the Organization itself the Google equivalent of the Entra directory. [1][2]

Folders are optional governance/grouping containers. Projects are the basic Google Cloud container for resources, APIs, billing association, collaborators, and permissions. IAM allow policies and organization policies can be applied at organization, folder, and project levels and inherited by descendant resources where supported. [1][6]

## 2.3 AWS: AWS Organizations and accounts

```text
AWS Organizations
└── Organization root (governance container; not an account root user)
    ├── Management account (administers the organization)
    └── Organizational units (OUs; can be nested)
        └── Member AWS accounts
            └── Resources (EC2, S3, VPC, CloudWatch, etc.)
```

AWS Organizations centrally groups AWS accounts under an organization root and optional nested organizational units (OUs). An organization has a management account and member accounts. Accounts are the primary security and administrative boundaries for many AWS designs; account-level separation is commonly used for production, development, security, logging, and shared services. Service control policies (SCPs) can set the maximum available permissions for principals in member accounts, but an SCP does not itself grant permissions. [5][22]

> **Avoid a terminology trap.** AWS Organizations “root” is the top container in the organization tree. It is not the same as the AWS account root user, which is the special identity for an individual AWS account. The organization management account is also distinct from member accounts.

## 2.4 Three-cloud hierarchy mapping

| Azure | Google Cloud | AWS | How close is it? |
| --- | --- | --- | --- |
| Microsoft Entra ID tenant | Cloud Identity / Google Workspace account | No direct equivalent: AWS IAM Identity Center has an identity store; AWS Organizations is a separate resource/account governance service | Approximate identity-directory comparison only. Do not map an AWS Organization to Entra ID. |
| Tenant root management group / management groups | Organization resource / folders | Organization root / OUs | Similar governance grouping and policy attachment purposes, but inheritance and policy mechanics differ. |
| Subscription | Project | AWS account | Closest practical container comparison. All are meaningful governance/cost/resource scopes, but account/project/subscription boundaries differ. |
| Resource group | No direct structural equivalent | No direct structural equivalent; AWS Resource Groups are logical groupings, not a universal parent container. [47] | Azure Resource Groups are a distinctive layer. Do not treat a GCP folder or AWS OU as an exact equivalent. |
| Azure resource | Google Cloud resource | AWS resource | Direct conceptual equivalent: deployed service object. |

Design takeaway: use folders in Google Cloud and OUs in AWS to group projects/accounts for policy and delegation; use projects/accounts/subscriptions to create clear workload, environment, ownership, and cost boundaries. These are architecture choices, not automatic equivalents. [1][3][5]

# 3. Identity plane: who manages the people and applications?

## 3.1 Microsoft Entra ID

Microsoft Entra ID is Microsoft’s identity and access management service. It contains users and groups and supports application identities. An app registration defines an application object in a tenant; an enterprise application is the tenant-local service principal representation used to manage that application’s access and configuration. For a SAML gallery/custom enterprise application flow, the common administrative path is Enterprise applications → application → Single sign-on → SAML. App registrations are commonly used when developers register OAuth 2.0 / OIDC applications and APIs. The distinction is useful, but application objects and service principals are linked parts of the same Entra application model. [16][17]

## 3.2 Google Cloud Identity and Google Workspace

Google Workspace and Cloud Identity provide managed Google identities, users, groups, and administrative controls. Google Cloud Organization is a separate resource hierarchy object associated with that managed identity account. Google Cloud IAM then grants users, groups, service accounts, and federated principals access to cloud resources. [1][2]

## 3.3 AWS IAM and IAM Identity Center

AWS IAM controls access to AWS services and resources through users, groups, roles, and policies. IAM Identity Center is AWS’s workforce access service for single sign-on to AWS accounts and applications. It can use its own identity store, Active Directory, or an external IdP. When an external IdP is used, IAM Identity Center uses SAML 2.0 for authentication and SCIM or manual provisioning to make users/groups available for account and application assignments. [11][12][13][23]

| Identity question | Azure | Google Cloud | AWS |
| --- | --- | --- | --- |
| Managed employee directory | Microsoft Entra ID | Cloud Identity / Google Workspace | IAM Identity Center identity store, AD, or external IdP connected to IAM Identity Center |
| Application identity | App registration / service principal | Service account (for Google Cloud workload identity); federated principal for external identity | IAM role (commonly assumed by workload or federated user); IAM user exists but should not be the default for workloads |
| Compute identity | System-assigned or user-assigned managed identity | Attached service account; Workload Identity Federation for external workloads | IAM role delivered to compute through instance profile, task role, pod identity/IRSA, or other service integration |
| Human SSO to cloud resources | Entra sign-in plus Azure RBAC | Google account sign-in or Workforce Identity Federation plus Google Cloud IAM | IAM Identity Center plus permission sets, or direct IAM SAML federation |

# 4. Human federation: SAML and OIDC across the three clouds

## 4.1 What federation means

Federation creates a trust relationship between an identity provider (IdP) and a relying/service provider. The IdP authenticates the person and issues a signed protocol response or token. The destination cloud validates the issuer, signature, intended audience, validity, and required claims, then maps the identity to a principal. The destination cloud still makes the authorization decision. [7][8][14][15]

## 4.2 Google Workforce Identity Federation

Google Workforce Identity Federation (Workforce Identity Federation or WIF) lets employees, partners, and contractors use an external IdP to sign in to supported Google Cloud services. Google supports external IdPs that implement SAML 2.0 or OIDC, including Entra ID, Okta, AD FS, and generic compatible providers. A workforce identity pool groups external identities; a provider defines the trust relationship to an IdP. [7][8][9][10]

A key distinction is federation versus synchronization: Google Workforce Identity Federation does not create or synchronize a matching Google-managed user account for every external workforce user. It maps the external identity to a federated principal and uses Google Cloud IAM allow policies to authorize that principal. [7]

```text
External employee (Entra / Okta / other IdP)
    │ SAML assertion or OIDC token
    ▼
Google Workforce Identity Pool + Provider
    │ validate issuer/signature/audience; map claims
    ▼
Google Security Token Service (STS)
    │ short-lived federated credential
    ▼
Google Cloud IAM allow policy
    ▼
Authorized Google Cloud resource
```

Typical IAM principal identifiers include `principal://.../subject/...` for an individual and `principalSet://.../group/...` for a mapped group. The exact member string depends on the pool, provider, and mapped attributes. Do not paste a normal Google `user:` email principal when the identity is actually an external workforce principal. [7][8]

## 4.3 Microsoft Entra as the IdP for Google Cloud

The Google-documented Entra SAML route uses an Entra Enterprise Application configured for SAML. The Google workforce provider is configured using Entra IdP metadata. The metadata contains the IdP issuer, SSO endpoint, and public signing certificate. Google’s federation configuration also needs the Google SP Entity ID/audience and ACS/Reply URL configured at the IdP. After authentication, claims are mapped in Google—for example, a stable Entra object identifier can become `google.subject`, and group claims can be mapped to `google.groups`. The exact attribute URI and emitted group format must be verified against the actual Entra assertion. [9][16]

For Entra OIDC, use the Google provider-specific guide and the generic Google Workforce Identity Federation OIDC provider instructions. Do not reuse SAML metadata fields as OIDC configuration: OIDC uses issuer, client ID, redirect URI/authorization flow, token claims, and provider signing keys (JWKS). [8][9]

## 4.4 Okta and other third-party IdPs

Okta is an identity provider (IdP) and access-management platform, not a Google Cloud-specific identity type. Google publishes an Okta-specific Workforce Identity Federation guide for SAML and OIDC. If an IdP is not listed in the Google console vendor list, Google documents a generic provider path for compatible SAML 2.0 or OIDC IdPs. The generic route still requires correct issuer, endpoint/metadata, signing-key trust, attribute mapping, conditions, and IAM bindings. [8][10]

The same generic concept applies to other compatible IdPs such as Ping Identity, OneLogin, AD FS, or a self-managed standards-compliant provider; do not assume a vendor-specific wizard exists for every provider. Use the provider’s official metadata/discovery documentation and validate the actual assertion or token. [8]

## 4.5 AWS workforce SSO with an external IdP

AWS offers three related but distinct approaches:

- AWS IAM Identity Center with an external IdP: connect the external IdP using SAML 2.0 for authentication and configure SCIM or manual provisioning so users and groups exist in IAM Identity Center. Then assign users/groups to AWS accounts and applications using permission sets. AWS explicitly notes that SAML does not provide a way for IAM Identity Center to query the IdP for users and groups. [11][12][13]
- Direct IAM SAML federation: configure an IAM SAML identity provider and an IAM role trust policy, then exchange the SAML response using AWS STS `AssumeRoleWithSAML`. This can provide temporary AWS credentials without creating a dedicated IAM user for every employee. It is a different pattern from IAM Identity Center permission sets. [14][24]
- IAM OIDC federation: register a trusted OIDC provider in IAM, create an IAM role whose trust policy accepts tokens from that issuer under specified conditions, and use AWS STS `AssumeRoleWithWebIdentity` to obtain temporary credentials. This is commonly used for web identity and CI/CD/workload cases; it is not the same as the external-IdP SAML configuration for IAM Identity Center. [15][39]

> **Important AWS difference.** AWS IAM Identity Center external-IdP sign-in is not a pure “SAML assertion creates an ephemeral principal with no directory record” pattern. IAM Identity Center requires the relevant users/groups to be provisioned into its identity store before assigning them to accounts/applications. Google Workforce Identity Federation is designed to federate external workforce identities without synchronizing Google user accounts. [7][11][12]

## 4.6 Comparison: human sign-in

| Scenario | Azure / Entra | Google Cloud | AWS |
| --- | --- | --- | --- |
| Company’s IdP is Entra ID; user signs in to each cloud | Entra authenticates the user; application/service integration and cloud RBAC apply | Workforce Identity Federation with SAML or OIDC; external principal receives Google IAM access | Connect Entra to IAM Identity Center using SAML + SCIM/manual provisioning, then assign permission sets; or use direct IAM SAML federation |
| Company’s IdP is Okta | Entra can federate with/consume external identity patterns depending on app architecture; Okta may also directly serve as IdP to apps | Google has a provider-specific Okta Workforce Identity Federation guide | AWS IAM Identity Center lists Okta as an external IdP with SAML and SCIM setup guidance |
| Company’s IdP is Google Workspace | Can be configured as an external IdP for supported Entra/application scenarios; validate product-specific support | Google Workspace / Cloud Identity is the managed Google identity system; this is distinct from Workforce Identity Federation into Google itself | AWS documents Google Workspace as an external IdP for IAM Identity Center using SAML and SCIM. [46] |
| Generic third-party SAML/OIDC IdP | Depends on the Entra application/federation scenario and supported protocols | Generic Workforce Identity Federation provider is supported for compatible SAML/OIDC IdPs | IAM Identity Center external IdP workflow is SAML + provisioning; IAM roles also support separate direct SAML/OIDC federation mechanisms |

# 5. SAML certificates, OIDC tokens, and trust validation

## 5.1 SAML in practical terms

SAML 2.0 commonly carries a signed XML assertion through a browser-based single sign-on exchange. The key configuration values are:

| SAML field | Purpose |
| --- | --- |
| IdP Entity ID / Issuer | Identifies the identity provider issuing the assertion. |
| IdP SSO URL | Where the service provider sends the browser to authenticate at the IdP. |
| SP Entity ID / Audience | Identifies the intended service provider; the IdP places/checks this audience in the assertion. |
| ACS / Reply URL | The service provider endpoint that receives the SAML response. |
| Signing certificate | Public certificate used by the service provider to verify the signed response/assertion. |
| Claims / attributes | Identity and group information that the service provider maps to its principal model. |
| RelayState | State/navigation information carried through a SAML flow; it is not the ACS endpoint. |

The IdP keeps its private signing key and signs the SAML response or assertion. The service provider uses the trusted public certificate to verify the signature and integrity of the signed content. A signature does not encrypt the XML; signing and encryption are different security properties. Entra’s SAML configuration lets an administrator choose whether to sign the response, assertion, or both. [16][42]

## 5.2 OIDC in practical terms

OpenID Connect is an identity layer built on OAuth 2.0. OIDC adds user authentication and the ID Token to OAuth’s authorization flows. In a common authorization-code flow, the browser is redirected to the IdP, the user authenticates, and an authorization code is returned to the client’s redirect URI; the code is exchanged for tokens. The ID Token is a signed JWT with claims such as issuer (`iss`), subject (`sub`), audience (`aud`), expiry (`exp`), and often nonce. [40][41]

| OIDC item | Purpose |
| --- | --- |
| Issuer (`iss`) | The identity provider identifier. Must match the configured trusted issuer. |
| Client ID / audience (`aud`) | Identifies the client/application for which the token was issued; Google WIF requires a client ID that matches the token audience. |
| Redirect URI | The registered client callback that receives the authorization response/code. |
| Discovery document | Publishes provider metadata such as authorization/token endpoints and JWKS URI. |
| JWKS | JSON Web Key Set containing public keys used to verify signed ID Tokens. |
| `state` | Binds the authorization response to the initiating browser session and helps prevent request forgery. |
| `nonce` | Binds an ID Token to the authentication request and helps detect token replay/substitution. |
| PKCE | Binds authorization-code redemption to the client instance that initiated the flow, especially important for public clients. |

Google Workforce Identity Federation supports OIDC authorization-code flow and implicit flow; Google describes authorization-code flow as the more secure of those WIF OIDC flow choices because tokens are returned to Google through a separate backend exchange rather than being returned in the browser URL. Do not turn that into the claim “OIDC is always more secure than SAML.” A correctly implemented SAML or OIDC integration can be secure; security depends on the selected flow, strict validation, token protection, key management, MFA, session handling, and least-privilege authorization. [7][8][40][41]

## 5.3 Certificates versus JWKS: relate it to the SSH analogy carefully

| SAML | OIDC |
| --- | --- |
| IdP publishes an X.509 signing certificate (public key material), often through SAML metadata. | IdP publishes public signing keys through a JWKS URI discovered from OIDC metadata, or keys are configured by another supported provider method. |
| IdP signs XML response/assertion with private signing key. | IdP signs an ID Token (JWT) with a private signing key. |
| SP validates XML signature against trusted certificate and checks issuer, audience, recipient, destination, and time conditions. | Relying party validates JWT signature with JWKS and checks issuer, audience, expiry, and relevant claims. |
| Certificate rollover must be coordinated with metadata/trust configuration. | JWKS key rotation is commonly published by the IdP; verifier must refresh or use valid published keys. |

Your SSH analogy is useful only at the public/private-key level: a verifier trusts public key material and checks a signature made with the corresponding private key. The purpose is different. SSH public-key authentication proves control of a login key; SAML/OIDC signing proves that an IdP issued the signed identity statement and that the signed data was not changed. It does not by itself prove that every claim is factually correct. [16][42][8]

# 6. Workload identities and cross-cloud access

## 6.1 People versus workloads

| Question | Google term | Azure term | AWS term |
| --- | --- | --- | --- |
| How does an employee sign in? | Workforce Identity Federation / Google user account | Microsoft Entra user and enterprise application SSO | IAM Identity Center user + permission set / IAM federated role |
| How does software authenticate? | Service account or Workload Identity Federation | Managed identity or service principal/app registration with federated credentials | IAM role assumed by the service; instance profile/task role/pod identity supplies it to compute |
| Which Google feature is for an Azure/AWS machine calling Google APIs? | Workload Identity Federation | Source of external identity: managed identity / service principal token | Source of external identity: IAM role/temporary credentials or outbound OIDC token |

Do not use Workforce Identity Federation for automated workloads. Google explicitly distinguishes workforce pools from workload pools and says workload federation is the intended approach for applications and machines. [7][8]

## 6.2 Azure workload identities

Azure Managed Identities provide an identity to code running on supported Azure resources without requiring the developer to manage credentials in application code. System-assigned identities share the lifecycle of the Azure resource; user-assigned identities are independent resources that can be associated with multiple resources. Microsoft Entra also supports workload identity federation for an app registration or user-assigned managed identity to trust an external OIDC issuer and specific issuer/subject/audience claims, avoiding a client secret in supported scenarios. [18][43]

## 6.3 Google workload identities

A Google Cloud service account is a special account typically used by an application or compute workload, not a person. A workload running on Google Cloud commonly uses an attached service account. An external workload can use Workload Identity Federation to exchange credentials from AWS, Azure, GitHub, GitLab, or another supported IdP for short-lived Google credentials. Google recommends avoiding downloaded service-account keys when a more secure keyless option is available. [19][20][7]

Google Workload Identity Federation supports two access patterns: direct resource access, where a federated principal receives IAM roles directly on a resource; and service account impersonation, where the federated principal is allowed to act as a Google service account and that service account receives the resource permissions. Not every Google API has identical support, so choose based on the service/API requirements. [20][7]

## 6.4 AWS workload identities

An AWS IAM role is an assumable identity that provides temporary security credentials for a session; unlike an IAM user, it is not normally associated with long-lived user credentials. EC2 applications can receive a role through an instance profile. Other compute services have their own role-attachment integrations. AWS STS also supports SAML and OIDC federation flows that return temporary AWS credentials after trust-policy validation. [14][15][24][38][39]

## 6.5 Cross-cloud examples

```text
Azure VM / Azure workload
  Managed Identity → Entra token
       ↓
Google Workload Identity Federation provider trusts Entra app/tenant
       ↓
Google STS exchanges external token
       ↓
Direct GCP IAM access OR impersonate a Google service account
       ↓
Cloud Storage / Pub/Sub / other authorized Google API
```

Google’s Azure VM guide describes this keyless pattern: the Azure VM obtains a token using managed identity, and the Google workload identity pool/provider trusts the corresponding Entra application configuration. [20]

```text
AWS EC2 / AWS workload
  IAM role via instance profile → temporary AWS credentials
       ↓
Google Workload Identity Federation trusts AWS account/role
       ↓
Google verifies AWS identity (including GetCallerIdentity in the documented AWS IAM credential path)
       ↓
Direct GCP IAM access OR impersonate a Google service account
       ↓
Cloud Storage / Pub/Sub / other authorized Google API
```

Google documents an AWS IAM credentials federation mechanism in which AWS temporary credentials are verified through AWS GetCallerIdentity. Google also documents AWS outbound identity federation, in which AWS can issue OIDC JWTs. These are different AWS-to-Google workload trust methods; choose and configure one deliberately. [20]

# 7. IAM and authorization: scopes, roles, and policies

## 7.1 Azure RBAC

Azure RBAC uses role assignments that bind a security principal to a role at a scope. Common scopes are management group, subscription, resource group, and resource. Higher-level assignments inherit to lower scopes. Azure role definitions can include management-plane actions and data-plane DataActions; for example, control-plane access to a storage account is not the same thing as permission to read blob data. [4][25][44]

## 7.2 Google Cloud IAM

Google Cloud IAM grants roles to principals through allow-policy bindings. A role is a set of permissions. Policies can be applied at organization, folder, project, and supported resource levels; parent bindings are inherited by child resources. A principal can be a Google user, group, service account, or federated principal. Google service accounts are both principals (they can receive roles) and resources (other principals can be allowed to use or administer them). [6][19]

## 7.3 AWS IAM and Organizations guardrails

AWS permissions are defined by JSON policy documents. Identity-based policies attach to users, groups, or roles; resource-based policies attach to supported resources such as S3 buckets. Cross-account access commonly requires a trust relationship and permission policies. AWS policy evaluation includes explicit-deny precedence, and additional policy types such as permissions boundaries, session policies, SCPs, and resource control policies can affect the final result. [23][24]

IAM Identity Center permission sets are templates for the access users/groups receive in AWS accounts. When assigned, IAM Identity Center provisions corresponding IAM roles in the target account and attaches the policies in the permission set. This is a workforce access management layer above the underlying account IAM role/policy model. [13]

| Concept | Azure | Google Cloud | AWS |
| --- | --- | --- | --- |
| Role definition | Azure role definition: actions and data actions | IAM role: collection of permissions | IAM policy document attached to identity/resource; permission set can package policies for account access |
| Role assignment/binding | Principal + role + scope | Principal + role binding in an allow policy on a resource | Policy attached to user/group/role/resource; role trust policy controls who can assume a role |
| Inheritance / organization guardrail | RBAC scope hierarchy; Azure Policy provides governance controls | Allow-policy inheritance; Organization Policy provides constraints | SCPs/RCPs and OU/account organization controls; SCPs limit maximum available permissions, they do not grant |
| Storage data access | Often requires a data-plane role such as Storage Blob Data Reader/Contributor | Requires relevant Cloud Storage permissions/roles on bucket/project | Identity/resource policy permissions such as s3:GetObject/PutObject; bucket policy is resource-based |

> **Least-privilege example.** A log uploader should receive only the object-create/write permission needed at the intended bucket/container, not broad project/subscription/account administrator access. Separate the identity that writes logs from the identity that reads or deletes them.

# 8. Services for a future security-log collection pipeline

The services below are not exact product equivalents; they are the closest building blocks for the same job. The goal is to understand how each cloud collects, routes, stores, schedules, and processes logs.

## 8.1 Storage

| Purpose | Azure | Google Cloud | AWS | Important difference |
| --- | --- | --- | --- | --- |
| Object storage for exported files | Azure Blob Storage in a Storage Account; data organized in containers and blobs | Cloud Storage bucket in a project; data stored as objects | Amazon S3 bucket in an AWS account; data stored as objects | The container hierarchy and IAM model differ; Azure Storage Account is itself a resource with containers, while GCS/S3 bucket placement is tied to a project/account. |
| Typical log landing zone | Storage account / blob container | GCS bucket / object prefix | S3 bucket / object prefix | A folder-like prefix is not necessarily a true filesystem folder. |

Official service overviews: Cloud Storage [30], Azure Blob Storage [31], Amazon S3 [32].

## 8.2 Audit and platform log collection

| Cloud | Log source / service | How to route or export | Cautions |
| --- | --- | --- | --- |
| Azure | Azure Activity Log and resource logs collected through Azure Monitor | Diagnostic settings can send selected logs/metrics to Log Analytics, Storage Accounts, or Event Hubs. | Resource logs are not collected by default for many resources; configure diagnostic settings per resource. Destination and region/network constraints apply. [26] |
| Google Cloud | Cloud Audit Logs and other Cloud Logging entries | Cloud Logging log sinks route matching entries to log buckets, Cloud Storage, BigQuery, or Pub/Sub. | A sink routes future incoming entries; it does not retroactively export older entries. Historical log copy/export is a separate operation. [27] |
| AWS | AWS CloudTrail records account/API activity; CloudWatch Logs stores application/service logs | CloudTrail trails can deliver to S3 and optionally CloudWatch Logs; CloudWatch Logs subscription filters can stream matching events to Kinesis Data Streams, Lambda, or Data Firehose. | CloudTrail records control-plane activity; it is not a substitute for every application or operating-system log source. [28][29] |

## 8.3 Messaging and event transport

| Need | Azure | Google Cloud | AWS | Do not confuse |
| --- | --- | --- | --- | --- |
| Streaming/event ingestion | Event Hubs | Pub/Sub | Kinesis Data Streams | These are the closest high-throughput stream concepts; delivery, ordering, retention, and consumer models differ. |
| Application messaging / queue | Service Bus queues/topics | Pub/Sub (topic/subscription model) or Cloud Tasks for task delivery | SQS queues + SNS topics | A message queue, publish/subscribe bus, and event router solve overlapping but different patterns. |
| Event routing / notifications | Event Grid | Eventarc / Pub/Sub depending on event source and consumer | EventBridge | Choose based on event source, filtering, delivery contract, and target integrations. |

Treat these as purpose-based comparisons, not one-to-one products: Azure documentation distinguishes Event Hubs for streaming, Service Bus for enterprise messaging, and Event Grid for event routing; Google distinguishes Pub/Sub from Cloud Tasks and Eventarc; AWS distinguishes Kinesis Data Streams from SQS, SNS, and EventBridge. Choose the service by delivery model, ordering, retention, filtering, retries, and consumer pattern—not by product name alone. [48][49][50][51][52][53][54][55]

Google Cloud Logging can route logs to Pub/Sub for downstream integrations. Azure Monitor diagnostic settings can stream logs to Event Hubs. CloudWatch Logs subscription filters can deliver log events to Kinesis, Lambda, or Firehose. [26][27][29]

## 8.4 Scheduling and invoking compute

| Need | Azure | Google Cloud | AWS |
| --- | --- | --- | --- |
| Run a task on a schedule | Azure Functions Timer Trigger (or Logic Apps recurrence for workflow-oriented orchestration) | Cloud Scheduler | Amazon EventBridge Scheduler |
| Call a private HTTP service | Azure Functions/App Service authentication and Entra-based access controls, depending on app hosting | Cloud Scheduler HTTP target with OIDC/OAuth token; Cloud Run requires an authenticated caller to have Cloud Run Invoker | EventBridge Scheduler invokes supported targets using an execution role; Lambda invocation permissions/policies must allow the call |
| Workload identity for the task | Managed identity | Attached service account | IAM role/execution role |

For Google Cloud, Cloud Scheduler can attach an OIDC token from a client service account for an HTTP target. For a Cloud Run service, grant the calling service account `roles/run.invoker` on the receiving service. The Cloud Scheduler service agent is not the application caller identity; do not use the service agent as the job’s client service account. [33][34][45]

Azure Functions Timer Trigger is a scheduler mechanism built into the Functions runtime and uses NCRONTAB-style schedules. AWS EventBridge Scheduler supports recurring cron/rate schedules and one-time invocations; it uses an execution role to call targets. [35][36]

## 8.5 “Invoker” terminology

Cloud Run Invoker is a Google Cloud IAM role (`roles/run.invoker`) on the receiving Cloud Run service. It authorizes a principal to invoke the service. It is not the same thing as the service account attached to the Cloud Run service: the attached identity is used by the running workload for outbound API calls, while the Invoker role is granted to callers for inbound requests. Similar separation exists in Azure (managed identity for outbound access versus inbound app authentication) and AWS (Lambda execution role versus permission to invoke the Lambda function). [18][33][34][45]

# 9. Security design checklist

1. Separate human identity from workload identity. Use Workforce Identity Federation for people and Workload Identity Federation for external software workloads in Google Cloud. [7][8]
2. Prefer temporary, short-lived credentials. Avoid distributing long-lived service-account JSON keys, AWS access keys, or application secrets where managed identity or federation is available. [19][20][24]
3. Validate the complete trust tuple: issuer, audience/client ID, subject, signature/key source, token/assertion lifetime, and expected claims. Add attribute conditions so only the intended tenant, repository, account, role, or user population can federate. [8][20][21][39][43]
4. Use stable subject identifiers for principal mapping. Avoid mutable display names or email addresses as the only security identity when a durable object ID is available. [9][10]
5. Grant permissions to groups where supported for workforce access, and grant workload permissions to a dedicated workload identity. Keep permissions narrow and scoped to the required project, subscription, account, bucket, or service. [4][13][22]
6. Understand control-plane versus data-plane access. A role that can manage a storage account/bucket resource does not necessarily equal permission to read/write every data object; verify the actual data permissions. [4][23][30][31][32][44]
7. Keep trust and permission separate. Trust policies determine who can assume an AWS role; permission policies determine what the role can do. In Google Cloud, WIF provider trust and IAM allow policies are separate; in Azure, identity authentication and Azure RBAC assignments are separate. [4][6][14][23]
8. Plan key and certificate rollover. Monitor SAML signing-certificate expiry and OIDC JWKS rotation. A broken or stale trust key can cause federation failures. [16][42][21]
9. Enable and validate audit logging for administrative and identity changes. Test successful and denied access, and confirm the resulting activity is visible in the relevant cloud audit source. [26][27][28]
10. For log pipelines, test permissions at each hop independently: source log read/export, message publish, queue/topic consume, function/service invoke, object create, object list/read, and object delete. Do not assume one role grants all stages. [4][6][23][24][26][27][29][30][31][32][33][34][36][37][45][48][52][53][55]

# 10. Suggested learning sequence for the hands-on lab

1. Build the identity and resource map: identify the tenant/directory, cloud organization, root governance container, subscription/project/account, and lowest resource scope in each cloud.
2. Create a Google Cloud learning organization/project and compare it with a non-production Azure subscription/resource group and an AWS member account. Do not use production identities or broad administrator roles for the lab.
3. Configure one human federation path first: Entra → Google Workforce Identity Federation using SAML. Capture the actual metadata, assertion, mapped subject/group attributes, and Google IAM result.
4. Repeat with OIDC using the authorization-code flow. Inspect the issuer, audience, subject, expiry, JWKS signature validation, state, nonce, and PKCE behavior relevant to the client/provider flow.
5. Configure AWS IAM Identity Center with an external IdP and observe the additional user/group provisioning requirement (SCIM or manual) and permission-set assignment model.
6. Compare a workload identity in each cloud: Azure Managed Identity, Google attached service account, and AWS IAM role/instance profile. Then configure an Azure or AWS workload to access a Google resource with Google Workload Identity Federation.
7. Build the log export path in one cloud at a time: audit source → native log service → sink/diagnostic setting/trail → storage or event stream → collector/processor → destination bucket.
8. Add scheduling and invocation only after each identity and permission boundary is understood. Test both success and expected-denial cases.

# 11. Glossary

| Term | Meaning |
| --- | --- |
| IdP | Identity Provider; authenticates a user or workload and issues trusted identity information. |
| SP / RP | Service Provider / Relying Party; consumes the SAML assertion or OIDC token. |
| SAML | XML-based federation protocol commonly used for enterprise browser SSO. |
| OIDC | OpenID Connect; an identity layer on OAuth 2.0 that uses ID Tokens. |
| ACS URL | SAML Assertion Consumer Service endpoint that receives the SAML response. |
| Entity ID / Audience | Identifier of the SAML service provider / intended token recipient. |
| JWKS | JSON Web Key Set; publishes public keys used to validate JWT signatures. |
| SCIM | System for Cross-domain Identity Management; standard for provisioning user/group records. |
| Workforce Identity Federation | Google Cloud federation for human workforce users from external IdPs. |
| Workload Identity Federation | Google Cloud federation for non-human workloads from external environments. |
| Service account | Google Cloud workload-oriented identity; can receive IAM roles and can be impersonated when permitted. |
| Managed identity | Azure-managed workload identity whose credentials are maintained by the platform. |
| IAM role (AWS) | An assumable AWS identity with permission policies; sessions use temporary security credentials. |
| Permission set | IAM Identity Center template of policies provisioned as roles into target AWS accounts. |
| SCP | AWS Organizations Service Control Policy; a permission guardrail that limits what member-account principals can do but does not grant permissions. |
| Log sink | Google Cloud Logging routing rule that sends matching log entries to a configured destination. |
| Diagnostic setting | Azure Monitor configuration that routes selected resource logs/metrics to supported destinations. |
| Cloud Run Invoker | Google Cloud IAM role that authorizes a principal to invoke a Cloud Run service. |

# 12. Official references

The numbered citations in this document point to the vendor or standards documentation below. Prefer these primary sources over third-party summaries when implementing or troubleshooting a configuration.

<a id="ref-1"></a>
[1] **Google Cloud resource hierarchy.** https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy

<a id="ref-2"></a>
[2] **Google Cloud Organization resource setup.** https://docs.cloud.google.com/resource-manager/docs/organization-setup

<a id="ref-3"></a>
[3] **Azure management groups overview.** https://learn.microsoft.com/en-us/azure/governance/management-groups/overview

<a id="ref-4"></a>
[4] **Azure RBAC overview.** https://learn.microsoft.com/en-us/azure/role-based-access-control/overview

<a id="ref-5"></a>
[5] **AWS Organizations concepts and hierarchy.** https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html

<a id="ref-6"></a>
[6] **Google Cloud IAM allow policies and inheritance.** https://docs.cloud.google.com/iam/docs/allow-policies

<a id="ref-7"></a>
[7] **Google Cloud Workforce Identity Federation overview.** https://docs.cloud.google.com/iam/docs/workforce-identity-federation

<a id="ref-8"></a>
[8] **Google Cloud generic Workforce Identity Federation configuration.** https://docs.cloud.google.com/iam/docs/configuring-workforce-identity-federation

<a id="ref-9"></a>
[9] **Google Cloud Workforce Identity Federation with Microsoft Entra ID.** https://docs.cloud.google.com/iam/docs/workforce-sign-in-microsoft-entra-id

<a id="ref-10"></a>
[10] **Google Cloud Workforce Identity Federation with Okta.** https://docs.cloud.google.com/iam/docs/workforce-sign-in-okta

<a id="ref-11"></a>
[11] **AWS IAM Identity Center: external identity providers.** https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html

<a id="ref-12"></a>
[12] **AWS IAM Identity Center: SAML and SCIM federation with external IdPs.** https://docs.aws.amazon.com/singlesignon/latest/userguide/other-idps.html

<a id="ref-13"></a>
[13] **AWS IAM Identity Center: permission sets.** https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html

<a id="ref-14"></a>
[14] **AWS IAM: SAML 2.0 federation.** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html

<a id="ref-15"></a>
[15] **AWS IAM: create an OIDC identity provider.** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html

<a id="ref-16"></a>
[16] **Microsoft Entra: enable SAML SSO for an enterprise application.** https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso

<a id="ref-17"></a>
[17] **Microsoft Entra: app objects and service principals.** https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals

<a id="ref-18"></a>
[18] **Microsoft Entra: managed identities for Azure resources.** https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview

<a id="ref-19"></a>
[19] **Google Cloud: service accounts overview.** https://docs.cloud.google.com/iam/docs/service-account-overview

<a id="ref-20"></a>
[20] **Google Cloud: Workload Identity Federation with AWS or Azure VMs.** https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds

<a id="ref-21"></a>
[21] **Google Cloud: Workload Identity Federation with other IdPs.** https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-other-providers

<a id="ref-22"></a>
[22] **AWS Organizations: Service Control Policies.** https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html

<a id="ref-23"></a>
[23] **AWS IAM: policy types and permissions.** https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html

<a id="ref-24"></a>
[24] **AWS IAM: roles.** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html

<a id="ref-25"></a>
[25] **Azure RBAC: scope overview.** https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview

<a id="ref-26"></a>
[26] **Azure Monitor: diagnostic settings.** https://learn.microsoft.com/en-us/azure/azure-monitor/data-collection/diagnostic-settings

<a id="ref-27"></a>
[27] **Google Cloud Logging: route log entries.** https://docs.cloud.google.com/logging/docs/routing/overview

<a id="ref-28"></a>
[28] **AWS CloudTrail concepts.** https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html

<a id="ref-29"></a>
[29] **Amazon CloudWatch Logs: subscription filters.** https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html

<a id="ref-30"></a>
[30] **Google Cloud Storage overview.** https://docs.cloud.google.com/storage/docs/introduction

<a id="ref-31"></a>
[31] **Azure Blob Storage introduction.** https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction

<a id="ref-32"></a>
[32] **Amazon S3 overview.** https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

<a id="ref-33"></a>
[33] **Google Cloud Scheduler: authenticated HTTP targets.** https://docs.cloud.google.com/scheduler/docs/http-target-auth

<a id="ref-34"></a>
[34] **Cloud Run: authenticate service-to-service.** https://docs.cloud.google.com/run/docs/authenticating/service-to-service

<a id="ref-35"></a>
[35] **Azure Functions: Timer Trigger.** https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer

<a id="ref-36"></a>
[36] **Amazon EventBridge Scheduler.** https://docs.aws.amazon.com/eventbridge/latest/userguide/using-eventbridge-scheduler.html

<a id="ref-37"></a>
[37] **Amazon EventBridge: IAM roles for targets.** https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events-iam-roles.html

<a id="ref-38"></a>
[38] **AWS IAM: EC2 instance profiles.** https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html

<a id="ref-39"></a>
[39] **AWS STS: AssumeRoleWithWebIdentity.** https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithWebIdentity.html

<a id="ref-40"></a>
[40] **OpenID Connect Core 1.0 specification.** https://openid.net/specs/openid-connect-core-1_0.html

<a id="ref-41"></a>
[41] **OAuth 2.0 Security Best Current Practice (RFC 9700).** https://www.rfc-editor.org/rfc/rfc9700.html

<a id="ref-42"></a>
[42] **Microsoft Entra: certificate signing options in a SAML token.** https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/certificate-signing-options

<a id="ref-43"></a>
[43] **Microsoft Entra: Workload Identity Federation.** https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation

<a id="ref-44"></a>
[44] **Azure Storage: assign an Azure role for Blob data access.** https://learn.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access

<a id="ref-45"></a>
[45] **AWS Lambda: managing permissions.** https://docs.aws.amazon.com/lambda/latest/dg/lambda-permissions.html

<a id="ref-46"></a>
[46] **AWS IAM Identity Center: configure SAML and SCIM with Google Workspace.** https://docs.aws.amazon.com/singlesignon/latest/userguide/gs-gwp.html

<a id="ref-47"></a>
[47] **AWS Resource Groups: getting started.** https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html

<a id="ref-48"></a>
[48] **Google Cloud Pub/Sub overview.** https://docs.cloud.google.com/pubsub/docs/pubsub_overview

<a id="ref-49"></a>
[49] **Google Cloud Eventarc overview.** https://docs.cloud.google.com/eventarc/docs/overview

<a id="ref-50"></a>
[50] **Azure messaging services documentation.** https://learn.microsoft.com/en-us/azure/messaging-services/

<a id="ref-51"></a>
[51] **Azure: choose between Event Grid, Event Hubs, and Service Bus.** https://learn.microsoft.com/en-us/azure/service-bus-messaging/compare-messaging-services

<a id="ref-52"></a>
[52] **Azure Service Bus overview.** https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview

<a id="ref-53"></a>
[53] **Amazon Kinesis Data Streams overview.** https://docs.aws.amazon.com/streams/latest/dev/

<a id="ref-54"></a>
[54] **Amazon EventBridge documentation.** https://docs.aws.amazon.com/eventbridge/

<a id="ref-55"></a>
[55] **AWS decision guide: SQS, SNS, or EventBridge.** https://docs.aws.amazon.com/decision-guides/latest/decision-guides/sns-or-sqs-or-eventbridge.html
