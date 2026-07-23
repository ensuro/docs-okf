---
type: Guide
title: Security and Monitoring
description: Ensuro prioritizes the security of our users.
tags:
- frontend
- security
timestamp: '2025-08-12T16:48:59+00:00'
---

# Security and Monitoring

Ensuro prioritizes the security of our users. Here's how we secure the Ensuro frontend application:

**Secure Development Foundation:** We adhere to a strict Secure Development Lifecycle Policy (SDL) under our Compliance Program with the Bermuda Monetary Authority to 

* Ensure all code dependencies used by the frontend are pinned to specific, well-tested versions. This minimizes vulnerabilities and supply-chain attacks.
* Ensure all released code is reviewed and thoroughly tested.
* Ensure that all deployments to productive environments are approved by senior management

**Robust Infrastructure:** The frontend application is built with ReactJS and deployed on Firebase Hosting. This leverages Google's secure infrastructure, including a global Content Delivery Network (CDN) for fast performance and advanced Distributed Denial-of-Service (DDoS) protection.

**Passwordless Login:** Ensuro utilizes Sign In With Ethereum (SIWE) for authentication. This approach leverages users' existing Ethereum accounts, eliminating the need to manage additional passwords and enhancing security.

**Wallet Security:** The frontend integrates with various wallets, including hardware wallets, using well-established and secure libraries, adding an extra layer of protection for your digital assets.

**Continuous Monitoring:** We constantly monitor the frontend's performance and availability. Alerts are triggered for any anomalies, such as outages or unexpected traffic surges. This allows us to swiftly address potential issues and ensure a smooth user experience.

**Deployment Safeguards:** Strict access controls are enforced on our code repositories and deployment platforms. Additionally, team-wide notifications are sent whenever new versions are deployed to the production environment, promoting transparency and accountability.
**This protocol has adopted the SEAL Safe Harbor Agreement for Whitehats, which empowers approved security researchers to intervene during active exploits to rescue funds. Full adoption details, scope, and bounty terms are publicly available upon request.**
