---
title: "Cloud Platform Fundamentals: AWS, GCP, and Azure"
description: "Comprehensive introduction to cloud computing concepts, service models, global infrastructure, high availability, identity, security, and operational models across AWS, GCP, and Azure."
tags: [overview, cloud-fundamentals, aws, gcp, azure, ha, iam, networking, cspm]
cloud: all
level: 100
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS Well-Architected Framework"
  - "Google Cloud Architecture Framework"
  - "Microsoft Azure Well-Architected Framework"
  - "NIST SP 800-145 Cloud Computing Definition"
---

# Abstract

This document provides a comprehensive foundation for understanding cloud computing across the three major providers: Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. It covers cloud service models, global infrastructure architecture, high availability principles, identity and access management, security posture management, Internet of Things (IoT), integration capabilities, and operational models. All claims are referenced to official provider documentation. This document serves as the prerequisite reading for all subsequent cloud-specific and cross-cloud guides.

# 1. Introduction to Cloud Computing

## 1.1 Definition and Service Models

Per NIST SP 800-145, cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort. The three standard service models are:

| Model | Description | Customer Responsibility | Provider Responsibility | Examples |
|-------|-------------|------------------------|------------------------|----------|
| **IaaS** (Infrastructure as a Service) | Virtualized compute, storage, network | OS, middleware, runtime, data, applications | Physical hardware, hypervisor, network fabric | EC2, Compute Engine, Virtual Machines |
| **PaaS** (Platform as a Service) | Managed runtime and development platform | Applications, data | OS, middleware, runtime, infrastructure | Elastic Beanstalk, App Engine, App Service |
| **SaaS** (Software as a Service) | Complete application delivered over network | Configuration, user management | Everything | Office 365, Google Workspace, Salesforce |

## 1.2 Deployment Models

| Model | Characteristics | Use Cases |
|-------|----------------|-----------|
| **Public Cloud** | Multi-tenant, provider-owned infrastructure | General workloads, burst capacity |
| **Private Cloud** | Single-tenant, on-premises or hosted | Regulated workloads, data sovereignty |
| **Hybrid Cloud** | Mix of public and private with orchestration | Legacy integration, gradual migration |
| **Multi-Cloud** | Multiple public clouds | Vendor diversity, best-of-breed services |

## 1.3 Shared Responsibility Model

All three providers follow a shared responsibility model where the provider secures the infrastructure (physical, network, hypervisor) and the customer secures their workloads (OS, applications, data, identity, network configuration). The boundary shifts based on service model:

- **IaaS**: Customer manages OS, firewall, patching, IAM
- **PaaS**: Provider manages OS/runtime; customer manages app/data/IAM
- **SaaS**: Provider manages almost everything; customer manages identity/access

References: [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/), [Google Cloud Shared Responsibility](https://cloud.google.com/security/shared-responsibility), [Microsoft Shared Responsibility](https://learn.microsoft.com/azure/security/fundamentals/shared-responsibility)

# 2. Global Infrastructure Architecture

## 2.1 Regions, Availability Zones, and Edge Locations

Each provider organizes global infrastructure hierarchically:

| Concept | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Region** | Geographically separate, isolated (e.g., us-east-1) | Geographically separate (e.g., us-central1) | Geographically separate (e.g., East US) |
| **Availability Zone (AZ)** | One or more discrete data centers with independent power, cooling, networking within a region. AZs are connected by low-latency links (< 2ms). | Zones within a region (e.g., us-central1-a). Single failure domain. | Zones within a region (e.g., East US 1, 2, 3). Independent power, cooling, networking. |
| **Edge Locations / PoPs** | CloudFront PoPs, Regional Edge Caches | Cloud CDN PoPs, Cloud Interconnect locations | Azure CDN PoPs, ExpressRoute peering locations |
| **Local Zones / Metro** | AWS Local Zones (single-digit ms to users) | GCP Edge Locations (limited) | Azure Edge Zones (preview) |

### Key Differences

- **AWS**: Largest number of regions (34+ launched, 38 announced). Each region has 3-6 AZs. AZ names are account-specific (your us-east-1a may differ from another account's us-east-1a).
- **GCP**: Regions contain 3-4 zones. Zone names are globally consistent (us-central1-a is the same physical location for all customers).
- **Azure**: Most regions have 3 zones. Some older regions are non-zonal. Zone names are consistent per region.

References: [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/), [Google Cloud Locations](https://cloud.google.com/about/locations), [Azure Global Infrastructure](https://azure.microsoft.com/global-infrastructure/geographies/)

## 2.2 Backbone Network Architecture

### AWS Global Network

AWS operates a purpose-built global backbone network connecting all regions via multiple 100-400 Gbps links. Key characteristics:

- **Private fiber**: AWS owns and operates trans-oceanic and terrestrial fiber
- **No internet transit**: Customer traffic between regions stays on AWS backbone
- **Multiple paths**: Redundant paths between every region pair
- **Transit Gateway**: Hub-and-spoke connectivity for VPCs across regions/accounts
- **Direct Connect**: Dedicated 1/10/100 Gbps private connections to AWS

Reference: [AWS Global Network](https://aws.amazon.com/about-aws/global-infrastructure/), [AWS Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/)

### Google Cloud Network

Google operates one of the largest private networks in the world, built on the same infrastructure that serves Search, YouTube, and Gmail:

- **Private global fiber**: Google-owned subsea cables (e.g., Curie, Dunant, Equiano, Grace Hopper) and terrestrial fiber
- **Software-defined networking**: Andromeda virtualization stack provides network virtualization
- **Premium Tier vs Standard Tier**: Premium Tier uses Google backbone for all egress; Standard Tier uses public internet for egress (cheaper, higher latency)
- **Network Connectivity Center**: Hub for hybrid/multi-cloud connectivity
- **Cloud Interconnect**: Dedicated (10/100 Gbps) and Partner Interconnect

Reference: [Google Cloud Network](https://cloud.google.com/network-connectivity/docs/network-connectivity-center/overview), [Google Network Tiers](https://cloud.google.com/vpc/docs/network-tiers)

### Azure Global Network

Microsoft operates a global network with 175+ PoPs and 190+ edge sites:

- **Private fiber**: Microsoft-owned subsea cables (MAREA, AEC-1, etc.) and terrestrial fiber
- **Azure Backbone**: Carries traffic between regions, stays on Microsoft network
- **ExpressRoute**: Private dedicated connections (50 Mbps - 100 Gbps) with ExpressRoute Global Reach for cross-region
- **Azure Virtual WAN**: Hub-and-spoke for branch-to-branch, VNet-to-VNet, VPN/ExpressRoute aggregation
- **Azure Front Door / CDN**: Edge network for application delivery

Reference: [Azure Global Infrastructure](https://azure.microsoft.com/global-infrastructure/), [Azure Networking](https://learn.microsoft.com/azure/networking/fundamentals/)

## 2.3 Backbone Network Comparison

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Network Ownership** | AWS-owned fiber | Google-owned fiber | Microsoft-owned fiber |
| **Traffic Path** | Always on AWS backbone (VPC peering, TGW) | Premium Tier: Google backbone; Standard: Public internet | Microsoft backbone (ExpressRoute, VNet peering) |
| **Inter-Region Latency** | < 50ms typical (e.g., us-east-1 to us-west-2 ~ 70ms) | < 50ms typical (e.g., us-central1 to us-west1 ~ 40ms) | < 50ms typical |
| **Dedicated Connectivity** | Direct Connect (1/10/100 Gbps) | Cloud Interconnect (10/100 Gbps + Partner) | ExpressRoute (50 Mbps - 100 Gbps) |
| **Edge Network** | CloudFront (400+ PoPs) | Cloud CDN (100+ PoPs) | Azure CDN / Front Door (175+ PoPs) |
| **Transit Hub** | Transit Gateway | Network Connectivity Center | Virtual WAN |

# 3. High Availability Architecture

## 3.1 HA Principles

High Availability (HA) is the ability of a system to remain operational despite component failures. Key metrics:

| Metric | Definition | Typical Target |
|--------|------------|----------------|
| **Availability** | Percentage of time system is operational | 99.9% (3 nines) to 99.999% (5 nines) |
| **RTO** | Recovery Time Objective - max downtime | < 5 min (HA) to < 1 hr (DR) |
| **RPO** | Recovery Point Objective - max data loss | 0 (synchronous) to < 1 hr (async) |
| **MTBF** | Mean Time Between Failures | Hardware dependent |
| **MTTR** | Mean Time To Repair | Process dependent |

## 3.2 HA Mechanisms by Cloud

### AWS HA

- **Multi-AZ Deployment**: Resources deployed across 2+ AZs within a region
- **Auto Scaling Groups**: Automatically replace unhealthy instances
- **Elastic Load Balancing**: NLB/ALB/GWLB distribute traffic across healthy targets
- **RDS Multi-AZ**: Synchronous replication to standby in different AZ (automatic failover ~ 60-120s)
- **S3 Cross-Region Replication (CRR)**: Async replication to another region
- **DynamoDB Global Tables**: Multi-region active-active with last-writer-wins
- **Route 53 Health Checks**: DNS failover with latency/geo routing

### GCP HA

- **Multi-Zonal Deployment**: Regional managed instance groups spread across zones
- **Regional Persistent Disks**: Synchronous replication across 2 zones (RPO=0)
- **Cloud Load Balancing**: Global anycast IP with health checks and failover
- **Cloud SQL High Availability**: Regional HA with synchronous replication (failover < 60s)
- **Cloud Spanner**: Multi-region strongly consistent database (99.999%)
- **Cloud Storage Dual-Region**: Geo-redundant with turbo replication (RPO ~ 0)
- **Cloud DNS**: Anycast DNS with health checks

### Azure HA

- **Availability Zones**: Deploy VMs, disks, LB across zones (99.99% VM SLA)
- **Availability Sets**: Logical grouping for fault/update domains (99.95% SLA)
- **Virtual Machine Scale Sets**: Auto-scaling with zone balancing
- **Azure Load Balancer / Application Gateway**: Zone-redundant frontends
- **Azure SQL Database**: Zone-redundant HA (failover < 30s)
- **Cosmos DB**: Multi-region with 99.999% availability
- **Azure Storage**: Zone-redundant storage (ZRS) and geo-redundant (GRS/GZRS)
- **Azure DNS / Traffic Manager**: DNS-based failover

## 3.4 HA Comparison with Evidence

| Capability | AWS | GCP | Azure | Evidence |
|------------|-----|-----|-------|----------|
| **VM SLA (Multi-AZ/Zone)** | 99.99% | 99.99% (regional MIG) | 99.99% (zonal) | [AWS SLA](https://aws.amazon.com/ec2/sla/), [GCP SLA](https://cloud.google.com/compute/sla), [Azure SLA](https://azure.microsoft.com/support/legal/sla/virtual-machines/) |
| **Managed DB Failover** | RDS Multi-AZ ~60-120s | Cloud SQL Regional HA <60s | Azure SQL Zone-redundant <30s | [RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html), [Cloud SQL](https://cloud.google.com/sql/docs/mysql/high-availability), [Azure SQL](https://learn.microsoft.com/azure/azure-sql/database/high-availability-sla) |
| **Global Load Balancer** | Global Accelerator / CloudFront | Cloud Load Balancing (anycast) | Front Door / Traffic Manager | [Global Accelerator](https://aws.amazon.com/global-accelerator/), [Cloud LB](https://cloud.google.com/load-balancing), [Front Door](https://learn.microsoft.com/azure/frontdoor/) |
| **Cross-Region Replication** | S3 CRR, DynamoDB Global Tables | Cloud Storage Dual-Region, Spanner | Cosmos DB, GRS/GZRS | [S3 CRR](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html), [Dual-Region](https://cloud.google.com/storage/docs/locations#dual-region), [Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/high-availability) |
| **Strong Consistency Multi-Region** | DynamoDB Global Tables (eventual) | Cloud Spanner (strong) | Cosmos DB (5 consistency levels) | [Spanner](https://cloud.google.com/spanner), [Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/consistency-levels) |

**Conclusion**: All three provide enterprise-grade HA. Azure SQL offers fastest documented failover (<30s). GCP Spanner provides unique strong consistency globally. AWS has most mature ecosystem for multi-region active-active.

# 4. Identity and Access Management (IAM)

## 4.1 IAM Fundamentals

IAM controls who (identity) can do what (permissions) on which resources.

| Concept | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Identity Store** | IAM Users, IAM Identity Center | Cloud Identity / Google Workspace | Microsoft Entra ID |
| **Workforce Federation** | IAM Identity Center (SAML+SCIM) | Workforce Identity Federation (SAML/OIDC, sync-less) | Entra ID native + Enterprise Apps |
| **Workload Identity** | IAM Roles + STS (IRSA, Instance Profile) | Service Accounts + Workload Identity Federation | Managed Identities + Federated Credentials |
| **Permission Model** | JSON Policies (identity-based, resource-based) | Allow Policies (principal + role + condition) | RBAC (role assignments at scopes) |
| **Guardrails** | SCPs (Organizations), Permission Boundaries | Organization Policies, Deny Policies | Azure Policy, Management Group Policies |

## 4.2 Cross-Cloud Federation

See [§04-cross-cloud.identity-federation-patterns] for detailed patterns. Key principle: **directionality matters** — Cloud A trusting Cloud B is not the same as Cloud B trusting Cloud A.

# 5. Security and Compliance

## 5.1 Cloud Security Posture Management (CSPM)

Each provider offers native CSPM capabilities:

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Native CSPM** | AWS Security Hub | Security Command Center (SCC) | Microsoft Defender for Cloud |
| **Compliance Frameworks** | CIS, PCI DSS, ISO, SOC, NIST, FedRAMP | CIS, PCI DSS, ISO, SOC, NIST, FedRAMP | CIS, PCI DSS, ISO, SOC, NIST, FedRAMP |
| **Continuous Monitoring** | Config Rules, Security Hub findings | SCC detectors, Policy Controller | Azure Policy, Defender assessments |
| **Remediation** | Systems Manager Automation | Cloud Functions / Config Connector | Logic Apps, Automation Accounts |
| **Multi-Account/Project** | Security Hub aggregation | SCC Organization level | Defender for Cloud management groups |

## 5.2 Encryption

| Layer | AWS | GCP | Azure |
|-------|-----|-----|-------|
| **At Rest (Default)** | AES-256 (EBS, S3, RDS) | AES-256 (PD, GCS, Cloud SQL) | AES-256 (Managed Disks, Blob, SQL) |
| **Customer-Managed Keys (CMK)** | KMS, CloudHSM | Cloud KMS, Cloud HSM | Key Vault, Managed HSM |
| **Client-Side Encryption** | S3 Encryption Client | GCS Customer-Supplied Keys | Blob Client-Side Encryption |
| **In Transit** | TLS 1.2+ (all services) | TLS 1.2+ (all services) | TLS 1.2+ (all services) |
| **VPC Encryption** | VPC Traffic Mirroring + Macie | VPC Flow Logs + SCC | VNet Flow Logs + Defender |

## 5.3 Compliance Certifications

All three maintain extensive compliance programs. Current certifications (verify current status):

| Standard | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **SOC 1/2/3** | Yes | Yes | Yes |
| **ISO 27001/27017/27018** | Yes | Yes | Yes |
| **PCI DSS Level 1** | Yes | Yes | Yes |
| **FedRAMP** | High/Moderate | High/Moderate | High/Moderate |
| **HIPAA** | Yes (BAA) | Yes (BAA) | Yes (BAA) |
| **GDPR** | Yes | Yes | Yes |

References: [AWS Compliance](https://aws.amazon.com/compliance/), [Google Cloud Compliance](https://cloud.google.com/security/compliance), [Azure Compliance](https://azure.microsoft.com/resources/trust-center/compliance/)

# 6. Internet of Things (IoT)

| Capability | AWS | GCP | Azure |
|------------|-----|-----|-------|
| **Device Management** | IoT Core (device registry, shadows, jobs) | Cloud IoT Core (deprecated → migrate to Pub/Sub) | IoT Hub (device twin, direct methods, jobs) |
| **Protocol Support** | MQTT, MQTT over WSS, HTTPS, LoRaWAN | MQTT, HTTP | MQTT, AMQP, HTTPS |
| **Edge Computing** | Greengrass (Lambda at edge) | Edge TPU + Cloud Run for Anthos | IoT Edge (modules, offline support) |
| **Device Provisioning** | Fleet Provisioning, JITR | Device Provisioning Service (DPS) | DPS (X.509, TPM, Symmetric Key) |
| **Rules Engine** | IoT Rules (SQL-like) | Cloud Functions / Dataflow | IoT Hub Routes + Stream Analytics |
| **Integration** | Kinesis, Lambda, S3, DynamoDB | Pub/Sub, Dataflow, BigQuery | Event Hubs, Functions, ADX, Blob |

**Note**: Google deprecated Cloud IoT Core (2023). Migration path: MQTT → Pub/Sub via protocol bridge.

# 7. Integration and Hybrid Capabilities

## 7.1 On-Premises Connectivity

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Dedicated Connection** | Direct Connect (1/10/100 Gbps) | Cloud Interconnect (10/100 Gbps) | ExpressRoute (50 Mbps - 100 Gbps) |
| **VPN** | Site-to-Site VPN (IPsec) | Cloud VPN (HA VPN, 99.99%) | VPN Gateway (Active/Active) |
| **Hybrid Kubernetes** | EKS Anywhere, EKS Distro | GKE On-Prem (Anthos) | AKS Hybrid (AKS on Azure Stack HCI) |
| **Management Extension** | Systems Manager Hybrid Activations | Config Connector, Anthos Config Management | Azure Arc (servers, Kubernetes, data services) |

## 7.2 Application Integration

| Pattern | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Event Bus** | EventBridge | Eventarc / Pub/Sub | Event Grid |
| **Messaging** | SQS (queues), SNS (pub/sub) | Pub/Sub | Service Bus, Event Hubs |
| **Workflow** | Step Functions | Workflows | Logic Apps |
| **API Management** | API Gateway | API Gateway (Apigee) | API Management |
| **Service Mesh** | App Mesh | Traffic Director (Istio) | Azure Service Mesh (Istio) |

# 8. Operational Models

## 8.1 Infrastructure as Code

| Tool | AWS | GCP | Azure |
|------|-----|-----|-------|
| **Native** | CloudFormation, CDK | Deployment Manager, Terraform | ARM Templates, Bicep |
| **Third-Party** | Terraform, Pulumi, CDKTF | Terraform, Pulumi | Terraform, Pulumi |
| **Policy as Code** | CloudFormation Guard, cfn-nap | Policy Controller, Terraform Sentinel | Azure Policy, Bicep Linter |

## 8.2 Monitoring and Observability

| Layer | AWS | GCP | Azure |
|-------|-----|-----|-------|
| **Metrics** | CloudWatch | Cloud Monitoring | Azure Monitor Metrics |
| **Logs** | CloudWatch Logs | Cloud Logging | Log Analytics |
| **Traces** | X-Ray | Cloud Trace | Application Insights |
| **Alerting** | CloudWatch Alarms | Alerting Policies | Alert Rules / Action Groups |
| **Dashboards** | CloudWatch Dashboards | Cloud Monitoring Dashboards | Azure Workbooks / Managed Grafana |
| **SLO/SLI** | ServiceLens | SLO Monitoring | Azure Monitor SLOs |

## 8.3 Cost Management

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **Billing** | Cost Explorer, CUR | Cloud Billing Reports | Cost Management + Billing |
| **Budgets/Alerts** | AWS Budgets | Cloud Billing Budgets | Azure Budgets |
| **Rightsizing** | Compute Optimizer | Recommender | Advisor |
| **Savings Plans** | Compute Savings Plans, EC2 Savings Plans | Committed Use Discounts | Reserved Instances, Savings Plans |

# 9. Service Category Mapping

## 9.1 Core Services

| Category | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **Compute** | EC2, Lambda, Fargate, Batch | Compute Engine, Cloud Run, Cloud Functions, Batch | Virtual Machines, Container Apps, Functions, Batch |
| **Kubernetes** | EKS | GKE | AKS |
| **Storage (Block)** | EBS | Persistent Disk | Managed Disks |
| **Storage (Object)** | S3 | Cloud Storage | Blob Storage |
| **Storage (File)** | EFS, FSx | Filestore | Azure Files |
| **Database (Relational)** | RDS, Aurora | Cloud SQL, AlloyDB | Azure SQL, PostgreSQL, MySQL |
| **Database (NoSQL)** | DynamoDB | Firestore, Bigtable | Cosmos DB |
| **Data Warehouse** | Redshift | BigQuery | Synapse Analytics |
| **Streaming** | Kinesis | Pub/Sub, Dataflow | Event Hubs, Stream Analytics |
| **ML/AI** | SageMaker, Bedrock | Vertex AI, Gemini | AI Studio, OpenAI Service |

## 9.2 Specialized Services

| Category | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **Quantum** | Braket | N/A | Quantum |
| **Satellite** | Ground Station | N/A | Orbital |
| **Blockchain** | Managed Blockchain | N/A | Blockchain Service |
| **Robotics** | RoboMaker | N/A | N/A |
| **Game Tech** | GameLift | Game Servers | PlayFab |

# 10. Reading Order for This Guide

This documentation is structured for sequential reading. Each section builds on the previous:

1. **00-cloud-intro/overview.md** (this document) — Cloud fundamentals, global infrastructure, HA, IAM, security, IoT, integration
2. **00-cloud-intro/prerequisites.md** — Required knowledge, account setup, tools
3. **00-cloud-intro/cloud-comparison.md** — Detailed service-by-service comparison
4. **00-cloud-intro/architecture-patterns.md** — LND-specific deployment patterns
5. **00-cloud-intro/backbone-network.md** — Deep dive on global network architecture
6. **00-cloud-intro/data-transfer-costs.md** — Egress/ingress, bucket, log costs
7. **00-cloud-intro/ha-comparison.md** — HA capabilities with evidence
7. **01-aws/**, **02-gcp/**, **03-azure/** — Cloud-specific guides (IAM, tutorials)
8. **04-cross-cloud/** — Cross-cloud comparisons (architecture, IAM, federation)
9. **05-identity-access/** — SAML/OIDC fundamentals
10. **06-reference/** — CLI cheatsheets, limits, pricing

# References

[1] NIST, "SP 800-145: The NIST Definition of Cloud Computing," 2011.
[2] AWS, "Well-Architected Framework," https://aws.amazon.com/architecture/well-architected/
[3] Google Cloud, "Architecture Framework," https://cloud.google.com/architecture/framework
[4] Microsoft, "Azure Well-Architected Framework," https://learn.microsoft.com/azure/well-architected/
[5] AWS, "Global Infrastructure," https://aws.amazon.com/about-aws/global-infrastructure/
[6] Google Cloud, "Locations," https://cloud.google.com/about/locations
[7] Microsoft, "Azure Global Infrastructure," https://azure.microsoft.com/global-infrastructure/
[8] AWS, "Shared Responsibility Model," https://aws.amazon.com/compliance/shared-responsibility-model/
[9] Google Cloud, "Shared Responsibility," https://cloud.google.com/security/shared-responsibility
[10] Microsoft, "Shared Responsibility," https://learn.microsoft.com/azure/security/fundamentals/shared-responsibility

# Appendices

## A. Acronyms

| Acronym | Definition |
|---------|------------|
| AZ | Availability Zone |
| BGP | Border Gateway Protocol |
| CDN | Content Delivery Network |
| CMK | Customer Managed Key |
| CSPM | Cloud Security Posture Management |
| DR | Disaster Recovery |
| HA | High Availability |
| HSM | Hardware Security Module |
| IaaS | Infrastructure as a Service |
| IAM | Identity and Access Management |
| IoT | Internet of Things |
| KMS | Key Management Service |
| MTBF | Mean Time Between Failures |
| MTTR | Mean Time To Repair |
| PaaS | Platform as a Service |
| PoP | Point of Presence |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |
| SaaS | Software as a Service |
| SLA | Service Level Agreement |
| SLO | Service Level Objective |
| SLI | Service Level Indicator |
| SCP | Service Control Policy |
| SLO | Service Level Objective |
| TLS | Transport Layer Security |
| VM | Virtual Machine |
| VPC | Virtual Private Cloud |
| ZRS | Zone-Redundant Storage |