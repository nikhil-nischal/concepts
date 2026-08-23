# HLD Interview Answering Framework

## Overview
- Baseline/meta reference, not a system-design topic — how to *structure* any HLD interview answer
- Derived from a full mock interview: "Design a Key-Value Store (like Memcached)" with a Microsoft SWE
- Worked example below (LRU cache + consistent hashing + cache client) is the vehicle, not the point — reuse the framework for any HLD prompt
- Core idea: design for one instance first, then scale out, then revisit requirements as a checklist

## Key Concepts

### The framework (arrival order)
- Requirements gathering — split into functional vs non-functional before touching architecture
- Design for a single instance first — one service, one node, no distribution yet
- Pick the core data structure/algorithm that satisfies the functional requirements
- Scale out — partition/shard the single-instance design across many nodes
- Solve discovery/routing — how do callers find the right shard
- Solve availability — replication, failover
- Revisit the non-functional requirements checklist — confirm each one is actually satisfied, don't assume
- Address security/observability — access control, logging, metrics
- Be ready to discuss alternatives and trade-offs when the interviewer probes

### Requirements gathering
- Functional requirements — the operations the system exposes (here: `put`, `get`)
- Non-functional requirements — system-wide qualities (here: availability, scalability, performance)
- State them explicitly before designing — they become the checklist you revisit at the end

### Single-instance design (worked example)
- Hash table alone gives O(1) get/put but no eviction tracking
- Combine hash table + doubly linked list (DLL) for O(1) LRU eviction: hash table maps key → DLL node, DLL orders nodes by recency
- New/accessed items move to head; least-recently-used item sits at tail and gets evicted when full — no recomputation needed, the list order *is* the recency order
- Alternative eviction policies: LFU (evict least-frequently-used, good for "top N" style ranking), FIFO (evict oldest-inserted)
- Policy choice is business-driven, not purely technical — no single "correct" answer

### Scaling out — partitioning
- Split the keyspace across multiple cache servers (e.g. alphabetical ranges)
- Deployment choice: cache co-located with its service host vs cache on separate dedicated hosts
- Co-located — less operational overhead, scales together automatically, but one host failure takes down both service and cache
- Separate hosts — independently scalable, more resilient to a single host failure, but more infrastructure to maintain

### Routing — which cache owns this key
- Naive: `hash(key) % number_of_hosts` — simple, but the modulus changes whenever a host is added or removed, so nearly every key remaps and cache-hits collapse
- Fix: consistent hashing — place cache nodes as points on a hash ring; each node owns the key range from the previous node up to itself
- Adding/removing a node only remaps the small subset of keys in its immediate neighborhood, not the whole ring
- Known drawbacks: can produce uneven key distribution across nodes; memory overhead grows with (number of cache servers × number of services)
- Alternative mentioned: jump hashing — addresses consistent hashing's distribution/memory issues

### Cache client (routing ownership)
- A library/module embedded in each service — owns "which cache server do I talk to," so services don't reimplement routing logic
- Needs a way to discover current cache server URLs; three options, increasing in robustness:
  - Static config file, deployed via CI/CD — simple, but stale until next deploy
  - Periodic pull from a shared config store (e.g. S3) — fresher, but polling frequency is a tuning trade-off
  - Service discovery via something like Zookeeper — registration + health checks, best for high-criticality setups since a stale cache list causes cache misses that fall through to the DB

### Availability — replication
- Single cache instance per shard is a single point of failure — add read replicas per node
- Writes (`put`) go to the primary; reads (`get`) can be routed to replicas to spread load
- Async replication: primary → replica lag risks stale/missed reads if the primary crashes before replicating — favors performance
- Sync replication: guarantees consistency but adds write latency — favors correctness
- This is a CAP-style consistency-vs-availability trade-off; the right choice is business-driven, not universal

### Security & observability
- Cache servers should sit behind a firewall — accessible only to trusted clients (services, load balancers), never exposed publicly
- Log and monitor: access patterns, request frequency, cache hit/miss ratio, disk usage
- "If you can't measure it, you can't improve it" — applies to both performance tuning and security auditing

## Trade-offs / Comparisons
| Decision point | Option A | Option B | Choose A when... |
|---|---|---|---|
| Cache deployment | Co-located with service host | Separate dedicated hosts | Ops simplicity matters more than isolating failures |
| Routing | Naive `hash % N` | Consistent hashing | Never — naive breaks on any node change; use consistent hashing |
| Cache discovery | Static config / S3 poll | Zookeeper-style service discovery | Cache topology changes rarely and staleness is tolerable |
| Replication | Async | Sync | Availability/performance matters more than always-fresh reads (e.g. social view counts vs financial statements) |

## Example / Walkthrough
- Prompt: "Design a key-value store like Memcached"
- 1. Gather requirements: functional = put/get; non-functional = availability, scalability, performance
- 2. Design single service + single cache: hash table + DLL for O(1) LRU get/put
- 3. Scale to multiple services/caches: partition keyspace, choose co-located vs separate hosts
- 4. Solve routing: reject naive mod-hashing, adopt consistent hashing on a ring
- 5. Introduce cache client component to own routing logic per service, backed by Zookeeper-style discovery
- 6. Revisit checklist: get/put ✅ (hash table+DLL), scalability ✅ (consistent hashing+cache client), performance ✅ (O(1) ops), availability ❌ — fix with read replicas + primary/replica async or sync replication
- 7. Layer in security (firewalled, trusted clients only) and observability (hit/miss ratio, access logs)
- 8. Field follow-up questions on alternatives (jump hashing) and trade-offs

## Interview Q&A
<details>
<summary>Why start with a single-instance design instead of the distributed system directly?</summary>

Designing for one service/one cache first keeps the core algorithm (e.g. LRU) simple to get right; bolting on distribution concerns (partitioning, routing, replication) from step one makes the problem needlessly harder to reason about.

</details>

<details>
<summary>Why does naive `hash(key) % N` routing break as the cluster changes size?</summary>

The modulus N changes whenever a host is added or removed, so the hash-to-host mapping shifts for nearly every key, causing most existing cache entries to be looked up on the wrong node (mass cache misses).

</details>

<details>
<summary>How does consistent hashing limit the blast radius of adding/removing a node?</summary>

Nodes are placed as points on a hash ring, each owning the key range up to the next node clockwise; only the keys in the range adjacent to the changed node get remapped, everyone else's ownership is untouched.

</details>

<details>
<summary>What's the point of a separate "cache client" component instead of each service handling its own routing?</summary>

Separation of concerns — routing/discovery logic (which node owns a key, where cache servers currently live) is shared and non-trivial, so it's factored into a library embedded in each service rather than duplicated per service.

</details>

<details>
<summary>Async vs sync replication for cache read replicas — how do you decide?</summary>

It's a business trade-off between consistency and availability/performance: async risks serving stale data if the primary fails before replicating (acceptable for something like social view counts), sync guarantees freshness at the cost of write latency (needed for something like financial statements).

</details>

<details>
<summary>What are the known drawbacks of consistent hashing, and what's an alternative?</summary>

It can produce uneven key distribution across nodes and its memory overhead scales with (cache servers × services); jump hashing is mentioned as an alternative that improves on both issues.

</details>

<details>
<summary>Besides functional correctness, what else should an HLD answer address once the core design works?</summary>

Security (restrict cache access to trusted clients behind a firewall) and observability (log access patterns, hit/miss ratio, disk usage) — both needed to operate and improve the system, not just to build it.

</details>

## Related Topics
- [HLD/06. Consistent Hashing](../HLD/06-consistent-hashing.md)
- [HLD/09. Design a Key-Value Store (DynamoDB)](../HLD/09-key-value-store-dynamodb.md)
