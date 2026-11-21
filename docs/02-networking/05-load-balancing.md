---
title: "Load Balancing Services"
description: "Load balancing comparison: L4/L7, global anycast, TLS termination, health checks, WAF integration, backend types, cost"
tags: [load-balancing, nlb, alb, cloud-lb, front-door, application-gateway, global-anycast]
cloud: all
level: 300
version: "1.0"
date: 2026-11-21
authors: ["LND Cloud Guide Contributors"]
references:
  - "AWS Elastic Load Balancing Documentation"
  - "Google Cloud Load Balancing Documentation"
  - "Azure Load Balancer Documentation"
---

# Abstract

Comparison of load balancing services across AWS (NLB, ALB), GCP (Cloud LB), and Azure (Standard LB, Front Door, Application Gateway).

# 1. Load Balancer Comparison

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| **L4 (Network)** | NLB (Layer 4, TLS passthrough) | Cloud LB (External TCP/UDP, SSL Proxy) | Standard LB (Layer 4), Front Door (L4 preview) |
| **L7 (Application)** | ALB (HTTP/HTTPS/gRPC), CLB (legacy) | Cloud LB (External HTTP/S, Internal HTTP/S) | Application Gateway (v2), Front Door |
| **Global Anycast** | Global Accelerator (separate) | Cloud LB (Premium Tier: native anycast) | Front Door (native anycast) |
| **TLS Termination** | ALB, NLB (TLS listener), Global Accelerator | Cloud LB (managed certs, self-managed) | App Gateway, Front Door (managed certs) |
| **Health Checks** | TCP, HTTP, HTTPS, gRPC | TCP, HTTP, HTTPS, gRPC, gRPC health | TCP, HTTP, HTTPS |
| **WAF Integration** | AWS WAF (ALB, CloudFront, API GW) | Cloud Armor (native) | Azure WAF (App Gateway, Front Door) |
| **Backend Types** | Instance, IP, Lambda, ALB | Instance groups, NEGs (GCE, GKE, Cloud Run) | VMSS, IP, App Service, AKS, Functions |
| **Session Affinity** | ALB (cookie), NLB (source IP) | Client IP, Generated cookie, Header | App Gateway (cookie), Front Door (cookie) |
| **Cost Model** | Hourly + LCU | Hourly + GB processed | Hourly + GB processed |

# 2. Load Balancer Architecture

### AWS
```mermaid
graph TB
    subgraph AWS[AWS Load Balancing]
        GA[Global Accelerator] -->|Anycast| ALB[ALB Regional]
        GA -->|Anycast| NLB[NLB Regional]
        ALB -->|ALB -> TG| TG1[Target Group: Instances]
        ALB -->|ALB -> TG| TG2[Target Group: IP/Lambda]
        NLB -->|NLB -> TG| TG3[Target Group: Instances]
        NLB -->|NLB -> TG| TG4[Target Group: IP/ALB]
    end
```

### GCP
```mermaid
graph TB
    subgraph GCP[GCP Cloud Load Balancing]
        LB[Cloud LB - Global Anycast] -->|Premium Tier| Backend[Backend Services]
        Backend --> IG[Instance Groups]
        Backend --> NEG[Network Endpoint Groups]
        NEG --> GCE[GCE VMs]
        NEG --> GKE[GKE Pods]
        NEG --> CR[Cloud Run]
    end
```

### Azure
```mermaid
graph TB
    subgraph Azure[Azure Load Balancing]
        FD[Front Door - Global Anycast] -->|Routing Rules| AG[Application Gateway Regional]
        FD -->|L4| LB[Standard LB Regional]
        AG -->|WAF| Pool[Backend Pool: VMSS, IP, AKS]
        LB --> Pool
    end
```

# 3. LND-Specific Load Balancer Configuration

| LND Service | Port | Protocol | Recommended LB | Health Check |
|-------------|------|----------|----------------|--------------|
| **P2P Gossip** | 9735 | TCP | NLB / TCP LB / Standard LB | TCP (SYN) |
| **gRPC** | 10009 | HTTP/2 | ALB / Cloud LB HTTP / App Gateway | gRPC Health Check |
| **REST API** | 8080 | HTTP/1.1 | ALB / Cloud LB HTTP / App Gateway | HTTP GET /health |

# References

[1] AWS, "Elastic Load Balancing Documentation," https://docs.aws.amazon.com/elasticloadbalancing/
[2] Google Cloud, "Cloud Load Balancing Documentation," https://cloud.google.com/load-balancing/docs
[3] Microsoft, "Azure Load Balancer Documentation," https://learn.microsoft.com/azure/load-balancer/
