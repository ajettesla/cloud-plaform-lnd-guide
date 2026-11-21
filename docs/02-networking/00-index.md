---
title: "Networking"
description: "Networking category — backbone, data transfer costs, VPN, SD-WAN, peering, DNS, load balancing, firewall, NAT, shared VPC"
---

# Networking — Reading Order

| Order | File | Purpose |
|-------|------|---------|
| 1 | [01-backbone.md](01-backbone.md) | Global backbone: fiber ownership, subsea cables, network tiers (Premium/Standard), private connectivity (Direct Connect, Cloud Interconnect, ExpressRoute), latency |
| 2 | [02-network-security.md](02-network-security.md) | Network security: VPN (Site-to-Site, Client), SD-WAN (Cloud WAN, Virtual WAN, NCC), MPLS/private connectivity, VPC peering, PrivateLink/PSC/Private Endpoint |
| 3 | [03-network-components.md](03-network-components.md) | Network components: Router (TGW, Cloud Router, vWAN), Switch (implicit), NAT Gateway, Shared VPC, Firewall, Load Balancer, DNS |
| 4 | [04-dns.md](04-dns.md) | DNS: Route 53, Cloud DNS, Azure DNS — private zones, split horizon, health checks, traffic routing, hybrid DNS |
| 5 | [05-load-balancing.md](05-load-balancing.md) | Load balancing: L4/L7, global anycast, TLS termination, health checks, WAF integration, backend types, cost |
| 6 | [06-vpc-peering.md](06-vpc-peering.md) | VPC peering: scope, transitivity, cross-account, cross-region, IP overlap, bandwidth, cost |

**Cross-references**: Security services in [04-security](../04-security/00-index.md), Billing in [07-billing](../07-billing/00-index.md), Deployment in [08-deployment](../08-deployment/00-index.md)
