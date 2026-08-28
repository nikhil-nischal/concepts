- [00. Roadmap](00-roadmap.md) — planned topic order for HLD prep

## Concepts
- [01. Network Protocols](concepts/01-network-protocols.md) — client-server vs P2P, HTTP/WebSocket/WebRTC, TCP vs UDP, when to use each
- [02. CAP Theorem](concepts/02-cap-theorem.md) — Consistency vs Availability vs Partition Tolerance, why only 2 of 3, CP vs AP
- [03. Microservices Design Patterns](concepts/03-microservices-design-patterns.md) — monolith vs microservices, decomposition, Strangler migration, Saga (distributed transactions), CQRS
- [05. Scale from Zero to a Million Users](concepts/05-scale-zero-to-million-users.md) — load balancer, DB replication, caching, CDN, multi-datacenter routing, message queues, sharding
- [06. Consistent Hashing](concepts/06-consistent-hashing.md) — ring hashing, virtual nodes, minimal rebalancing on node add/remove
- [08. Back-of-the-Envelope Estimation](concepts/08-back-of-envelope-estimation.md) — traffic/storage/RAM/server capacity planning, worked Facebook example
- [10. SQL vs NoSQL](concepts/10-sql-vs-nosql.md) — structure, nature, scalability, ACID vs BASE, when to use which DB
- [15. High Availability & Resilience](concepts/15-high-availability-active-passive-active-active.md) — single point of failure, active-passive (primary + replica, DR failover) vs active-active (multi-master, bi-directional sync)
- [16. Distributed Messaging Queue](concepts/16-messaging-queue-kafka-rabbitmq.md) — Kafka (topic/partition/offset/broker/cluster/zookeeper, leader-follower) vs RabbitMQ (exchange/routing key, push-based), retry + DLQ
- [17. Proxy vs Reverse Proxy](concepts/17-proxy-vs-reverse-proxy.md) — forward proxy vs reverse proxy, CDN as reverse proxy, proxy vs VPN vs load balancer vs firewall
- [18. Load Balancer & Algorithms](concepts/18-load-balancer-algorithms.md) — L4 vs L7, static (round robin, weighted round robin, IP hash) vs dynamic (least connection, weighted least connection, least response time/TTFB)
- [19. Distributed Cache & Caching Strategies](concepts/19-caching-strategies.md) — distributed caching via consistent hashing, cache-aside, read-through, write-around, write-through, write-back
- [20. Distributed Transactions](concepts/20-distributed-transactions.md) — ACID recap, Two-Phase Commit, Three-Phase Commit, Saga pattern (compensating transactions)
- [21. Database Indexing](concepts/21-database-indexing.md) — data pages vs data blocks, B/B+ Tree mechanics, clustered vs non-clustered index, page splitting, indexing overhead
- [22. Concurrency Control](concepts/22-concurrency-control.md) — shared/exclusive locks, isolation levels (dirty/non-repeatable/phantom reads), optimistic (versioning) vs pessimistic (locking, deadlock) concurrency control
- [23. Two Phase Locking (2PL)](concepts/23-two-phase-locking.md) — growing/shrinking phase, Basic/Conservative/Strong Strict 2PL, deadlock (WFG, wait-die, wound-wait) and cascading aborts
- [24. OAuth 2.0](concepts/24-oauth-2.md) — 4 actors, authorization code grant flow, access/refresh tokens, CSRF protection via state, implicit/password/client-credentials grants
- [25. Symmetric & Asymmetric Encryption](concepts/25-symmetric-asymmetric-encryption.md) — AES internals (state array, key expansion, rounds), Diffie-Hellman key exchange, digital signatures (auth + integrity)
- [26. JWT (JSON Web Token)](concepts/26-jwt.md) — JWT vs session ID, token structure (header/payload/signature), SSO, invalidation challenges, JWE, JWK exploit
- [28. API Gateway](concepts/28-api-gateway.md) — API Gateway vs load balancer, API composition, auth, rate limiting, service discovery, multi-region/AZ scaling, DNS load balancing
- [29. Service Mesh](concepts/29-service-mesh.md) — sidecar proxy pattern, data plane vs control plane, Istio (Envoy/Galley/Pilot/Citadel), circuit breaker, retries, canary deployment, telemetry
- [30. DNS (Domain Name System)](concepts/30-dns.md) — domain hierarchy, A/CNAME records, recursive vs iterative resolution, root/TLD/authoritative servers, registrar chain, DNS zones
- [31. Dividing a Monolith into Microservices (DDD)](concepts/31-monolith-to-microservices-ddd.md) — event storming, bounded context, distributed monolith anti-pattern, Amazon Prime Video case study
- [32. Common Web Attacks: CSRF, XSS, CORS, SQL Injection](concepts/32-web-attacks-csrf-xss-cors-sqli.md) — attack mechanisms and mitigations (CSRF tokens, output escaping, origin whitelisting, parameterized queries)

## Examples (design problems)
- [07. URL Shortener](examples/07-url-shortener.md) — base62 encoding, unique ID generation (Snowflake, Zookeeper ranges), TinyURL design
- [09. Design a Key-Value Store](examples/09-key-value-store.md) — Memcached-style: LRU hash table + DLL, consistent hashing for server selection, cache client, read replicas for HA
- [09a. Design a Key-Value Store (DynamoDB-style)](examples/09a-key-value-store-dynamodb.md) — partitioning, replication, quorum get/put, vector clocks, gossip, Merkle tree
- [11. WhatsApp / Chat Application Design](examples/11-whatsapp-system-design.md) — WebSocket vs polling, user mapping/Zookeeper, NoSQL partitioning, offline delivery, presence
- [12. Design a Rate Limiter](examples/12-rate-limiter.md) — Token Bucket, Leaking Bucket, Fixed/Sliding Window Counter, Sliding Window Log, shared counter store + atomicity
- [14. Design Idempotent POST API](examples/14-idempotent-post-api.md) — idempotency key, CREATED/COMPLETED status, 409 conflict, mutex/distributed lock for parallel duplicates
