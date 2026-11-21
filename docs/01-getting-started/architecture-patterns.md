---
title: "LND Architecture Patterns on Cloud"
description: "Architecture patterns for deploying Lightning Network Daemon on cloud: standalone, HA, multi-node, serverless, and Kubernetes-native deployments."
tags: [architecture, patterns, ha, kubernetes, serverless]
cloud: all
level: 200
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "LND High Availability Guide"
  - "Kubernetes Operator Pattern"
  - "Cloud Design Patterns"
---

# Abstract

This document describes proven architecture patterns for running LND on cloud platforms. Patterns range from simple standalone deployments to highly available multi-node clusters with automated failover. Each pattern includes trade-offs, prerequisites, and references to implementation guides.

# 1. Pattern Taxonomy

```mermaid
graph TB
    subgraph Patterns[Architecture Patterns]
        P1[Standalone VM]
        P2[Active-Passive HA]
        P3[Active-Active Multi-Node]
        P4[Kubernetes Native]
        P5[Serverless/Event-Driven]
        P6[Hybrid/Multi-Cloud]
    end
    
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
```

**Figure 1:** Architecture pattern progression from simple to complex.

# 2. Pattern 1: Standalone VM

## 2.1 Architecture [Figure 2]

```mermaid
graph TB
    subgraph Cloud[Cloud Provider]
        LB[Network Load Balancer]
        VM[LND VM]
        Disk[Encrypted Block Storage]
        Secrets[Secrets Manager]
        Monitoring[Monitoring Agent]
    end
    Internet((Internet)) --> LB
    LB --> VM
    VM --> Disk
    VM --> Secrets
    VM --> Monitoring
```

**Figure 2:** Standalone VM pattern.

## 2.2 Characteristics

| Aspect | Details |
|--------|---------|
| **Availability** | Single AZ, no automatic failover |
| **Recovery** | Manual (restore from snapshot) |
| **Scaling** | Vertical (resize instance) |
| **Operations** | SSH/SSM access, systemd management |
| **Cost** | Lowest (~$50-200/mo) |
| **Complexity** | Low |

## 2.3 When to Use

- Development/staging environments
- Low-value nodes (< 1 BTC capacity)
- Teams with strong VM ops skills
- Compliance requiring dedicated instances

## 2.4 Implementation Reference

- AWS: [§12.1] (Tutorial: AWS LND on VM)
- GCP: [§12.2] (Tutorial: GCP LND on VM)
- Azure: [§12.3] (Tutorial: Azure LND on VM)

# 3. Pattern 2: Active-Passive HA

## 3.1 Architecture [Figure 3]

```mermaid
graph TB
    subgraph Cloud[Cloud Provider]
        LB[Load Balancer<br/>Health Checks]
        subgraph AZ1[Availability Zone A]
            VM1[LND Primary]
            Disk1[Block Storage]
        end
        subgraph AZ2[Availability Zone B]
            VM2[LND Standby]
            Disk2[Block Storage]
        end
        Sync[Replication<br/>DRBD / rsync / EBS]
        Secrets[Secrets Manager<br/>Cross-AZ]
    end
    Internet((Internet)) --> LB
    LB -.->|Health Check| VM1
    LB -.->|Health Check| VM2
    VM1 --> Disk1
    VM2 --> Disk2
    VM1 -.->|Sync| Sync
    Sync -.->|Sync| VM2
    VM1 --> Secrets
    VM2 --> Secrets
```

**Figure 3:** Active-Passive HA pattern with cross-AZ replication.

## 3.2 Characteristics

| Aspect | Details |
|--------|---------|
| **Availability** | Multi-AZ, automatic failover (~30-60s) |
| **Recovery** | Automated via health checks |
| **Data Consistency** | Async replication (RPO ~1-5 min) |
| **Scaling** | Vertical only |
| **Cost** | 2x compute + replication |
| **Complexity** | Medium |

## 3.3 Failover Process

1. **Health check fails** on primary (LND RPC, P2P port)
2. **Load balancer** marks primary unhealthy
3. **Traffic shifts** to standby
4. **Standby promotes** to primary (mounts shared storage or syncs)
5. **DNS/Service discovery** updates

## 3.4 Implementation Reference

- Requires: Shared storage (EFS, Filestore, Azure Files) or block replication
- AWS: EBS Multi-Attach (io2) or DRBD on gp3
- GCP: Regional Persistent Disk (beta) or DRBD
- Azure: Shared Disks (Premium SSD v2) or DRBD

# 4. Pattern 3: Active-Active Multi-Node

## 4.1 Architecture [Figure 4]

```mermaid
graph TB
    subgraph Cloud[Cloud Provider]
        LB[Load Balancer<br/>Session Affinity]
        subgraph Cluster[LND Cluster]
            N1[LND Node 1]
            N2[LND Node 2]
            N3[LND Node 3]
        end
        Etcd[(etcd/Raft<br/>Channel State)]
        Channels[Channel DB<br/>Shared/Replicated]
        Watchtower[Watchtower<br/>Cluster]
    end
    Internet((Internet)) --> LB
    LB --> N1
    LB --> N2
    LB --> N3
    N1 --> Etcd
    N2 --> Etcd
    N3 --> Etcd
    N1 -.-> Channels
    N2 -.-> Channels
    N3 -.-> Channels
    N1 --> Watchtower
    N2 --> Watchtower
    N3 --> Watchtower
```

**Figure 4:** Active-Active multi-node pattern with shared state.

## 4.2 Characteristics

| Aspect | Details |
|--------|---------|
| **Availability** | Multi-AZ, no single point of failure |
| **Scaling** | Horizontal (add nodes) |
| **Throughput** | Linear with nodes (HTLC routing) |
| **Complexity** | High (distributed systems) |
| **Cost** | N x compute + shared state |

## 4.3 Challenges

- **Channel state synchronization**: LND doesn't natively support active-active
- **Solution**: Single writer (leader) + read replicas, or external coordination
- **Watchtower**: Must monitor all nodes
- **Macaroon rotation**: Distributed coordination required

## 4.4 Current Recommendation

Use **Pattern 2 (Active-Passive)** for production until LND adds native clustering support. See [§10.5] for experimental multi-node approaches.

# 5. Pattern 4: Kubernetes Native

## 5.1 Architecture [Figure 5]

```mermaid
graph TB
    subgraph K8s[Kubernetes Cluster]
        subgraph System[System Namespace]
            CertMgr[cert-manager]
            ExtDNS[ExternalDNS]
            PromOp[Prometheus Operator]
        end
        subgraph LND[LND Namespace]
            STS[StatefulSet<br/>LND Pods]
            SVC[Service<br/>Headless + LB]
            PVC[PVC<br/>Per-Pod Storage]
            Secret[Secret<br/>Macaroons, TLS]
            CM[ConfigMap<br/>lnd.conf]
        end
        subgraph Bitcoind[Bitcoind Namespace]
            BTCD[StatefulSet<br/>Bitcoind]
        end
    end
    Ingress[Ingress/Gateway] --> SVC
    SVC --> STS
    STS --> PVC
    STS --> Secret
    STS --> CM
    STS --> BTCD
```

**Figure 5:** Kubernetes-native pattern with StatefulSet.

## 5.2 Characteristics

| Aspect | Details |
|--------|---------|
| **Availability** | Pod disruption budgets, multi-AZ nodes |
| **Scaling** | Horizontal (replicas), vertical (VPA) |
| **GitOps** | ArgoCD/Flux sync from Git |
| **Cloud Integration** | IRSA (AWS), Workload Identity (GCP), Entra WI (Azure) |
| **Operations** | kubectl, Helm, Kustomize |

## 5.3 Key Components

- **StatefulSet**: Stable network identity, ordered deployment
- **PersistentVolumeClaim**: Per-pod block storage
- **Headless Service**: Direct pod-to-pod communication
- **LoadBalancer Service**: External access for P2P/gRPC/REST
- **ConfigMap/Secret**: Configuration and secrets management

## 5.4 Implementation Reference

- AWS EKS: [§12.4]
- GCP GKE: [§12.5]
- Azure AKS: [§12.6]
- Helm Chart: [§11.5] (Shared Terraform Modules)

# 6. Pattern 5: Serverless / Event-Driven

## 6.1 Architecture [Figure 6]

```mermaid
graph TB
    subgraph Cloud[Cloud Provider]
        API[API Gateway<br/>HTTPS/gRPC]
        Function[Cloud Function<br/>LND Container]
        Queue[Event Queue<br/>Pub/Sub, EventBridge]
        Storage[Object Storage<br/>Channel Backups]
        Secrets[Secrets Manager]
        Scheduler[Scheduler<br/>Cron Jobs]
    end
    User((User)) --> API
    API --> Function
    Scheduler --> Function
    Function --> Queue
    Function --> Storage
    Function --> Secrets
```

**Figure 6:** Serverless pattern for intermittent LND operations.

## 6.2 Use Cases

| Use Case | Trigger | Duration |
|----------|---------|----------|
| Channel backup | Scheduled (daily) | < 2 min |
| Watchtower check | Block height change | < 30s |
| Rebalancing | Fee rate change | < 5 min |
| Invoice settlement | Webhook | < 10s |
| Node health check | Scheduled (5m) | < 10s |

## 6.3 Limitations

- **Cold starts**: 100-500ms latency spike
- **State persistence**: Must use external storage (EFS, Cloud SQL, Disk)
- **P2P connectivity**: Requires VPC connector / Private Service Connect
- **Long-running**: Max 15-60 min (Lambda/Cloud Run)

## 6.4 Implementation Reference

- AWS Lambda: [§12.7]
- GCP Cloud Run: [§12.8]
- Azure Container Apps: (Planned)

# 7. Pattern 6: Hybrid / Multi-Cloud

## 7.1 Architecture [Figure 7]

```mermaid
graph TB
    subgraph Primary[Primary Cloud]
        P_LB[Load Balancer]
        P_LND[LND Primary]
        P_Storage[Storage]
    end
    subgraph Secondary[Secondary Cloud]
        S_LB[Load Balancer]
        S_LND[LND Standby]
        S_Storage[Storage]
    end
    Interconnect[Cloud Interconnect<br/>Direct Connect / ExpressRoute]
    DNS[Global DNS<br/>Route53 / Cloud DNS / Traffic Manager]
    
    Users((Users)) --> DNS
    DNS --> P_LB
    DNS -.->|Failover| S_LB
    P_LND --> P_Storage
    S_LND --> S_Storage
    P_Storage -.->|Async Replication| S_Storage
    P_LND -.->|Health Check| Interconnect
    Interconnect -.->|Health Check| S_LND
```

**Figure 7:** Multi-cloud disaster recovery pattern.

## 7.2 Characteristics

| Aspect | Details |
|--------|---------|
| **RTO** | 1-5 minutes (DNS failover) |
| **RPO** | 1-5 minutes (async replication) |
| **Cost** | 2x primary + interconnect |
| **Complexity** | Very high |

## 7.3 Implementation Reference

- Cross-cloud VPN: [§03.4]
- Global DNS: [§03.5]
- Tutorial: [§12.9] (Cross-Cloud HA)

# 8. Pattern Selection Guide

| Requirement | Recommended Pattern |
|-------------|---------------------|
| Dev/Test | Pattern 1 (Standalone) |
| Production, < 1 BTC | Pattern 1 + Backups |
| Production, 1-10 BTC | Pattern 2 (Active-Passive) |
| Production, > 10 BTC | Pattern 4 (Kubernetes) |
| High throughput routing | Pattern 4 (Kubernetes) |
| Event-driven automation | Pattern 5 (Serverless) |
| Regulatory multi-region | Pattern 6 (Multi-Cloud) |
| Team has K8s expertise | Pattern 4 (Kubernetes) |
| Team prefers VM ops | Pattern 2 (Active-Passive) |

# References

[1] Lightning Network Daemon, "High Availability," https://github.com/lightningnetwork/lnd/blob/master/docs/ha.md
[2] Kubernetes, "StatefulSet Documentation," https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
[3] AWS, "EBS Multi-Attach," https://docs.aws.amazon.com/ebs/latest/userguide/ebs-multi-attach.html
[4] Google Cloud, "Regional Persistent Disks," https://cloud.google.com/compute/docs/disks/regional-persistent-disk
[5] Microsoft Azure, "Shared Disks," https://learn.microsoft.com/azure/virtual-machines/disks-shared
