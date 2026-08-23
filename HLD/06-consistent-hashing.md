# Consistent Hashing

## Overview
- Technique to distribute keys (requests, data) across a set of servers/nodes evenly.
- Solves the "mass rebalancing" problem that plain `hash % N` hashing has when the number of nodes changes.
- Used in load balancers, distributed caches, and sharded/distributed databases.
- Builds on top of a normal hash function + modulo, so understand that first.

## Key Concepts

### Plain hashing (mod N)
- Hash function — takes any input (key), returns a fixed-length output value.
- To map a key to one of N servers: `hash(key) % N` picks a server index.
- Works fine as long as N (number of servers/DB shards) stays fixed.
- Problem: if N changes (server added/removed, DB re-sharded), `mod N` changes for almost every key.
- Example: DB with 3 partitions, `id % 3` decides the partition. Add a 4th partition → now `id % 4` — nearly every key maps to a different partition than before, forcing a full data reshuffle (rebalancing) even though only one node changed.
- This is expensive at scale (millions of DB entries, or live traffic on a load balancer) — not acceptable to move almost everything for one node change.

```mermaid
flowchart LR
    subgraph Before["id % 3 (3 partitions)"]
        direction LR
        K1a["id=1"] --> P1a[Partition 0]
        K2a["id=2"] --> P2a[Partition 1]
        K3a["id=3"] --> P3a[Partition 2]
    end
    subgraph After["id % 4 (partition added)"]
        direction LR
        K1b["id=1"] --> P1b[Partition 1]
        K2b["id=2"] --> P2b[Partition 2]
        K3b["id=3"] --> P3b[Partition 3]
    end
    Before -.->|add 1 partition, modulo shifts for nearly every key| After
```

### Consistent hashing — the idea
- Arrange the hash output space as a ring (circle), e.g. values 0 to some max, wrapping back to 0.
- Hash each server onto a random point on the ring (using the same hash function).
- Hash each key onto a point on the ring the same way.
- A key is served by the first server found walking clockwise from the key's position.
- When a server is added: it only takes over the keys between itself and the previous server (counter-clockwise neighbor) — every other key stays put.
- When a server is removed: only the keys it was holding move to the next server clockwise — everyone else is unaffected.
- Net effect: adding/removing one node only remaps roughly `1/N` of the keys, not all of them.

```mermaid
flowchart LR
    S1((Server A)) -->|clockwise arc| S2((Server B))
    S2 -->|clockwise arc| S3((Server C))
    S3 -->|clockwise arc| S4((Server D))
    S4 -->|clockwise arc, wraps to start| S1
    K["Key X"] -.->|walk clockwise, first server found| S4
```
*(mermaid has no native circular layout — this cycle of arrows stands in for the ring; the wrap-around edge from D back to A closes it.)*

### Virtual nodes
- Placing each physical server at just one random ring point can lead to uneven key distribution (some servers get a much bigger arc than others).
- Fix: replicate each physical server at multiple random points on the ring (virtual nodes/replicas).
- More virtual nodes per server → more even split of the ring → more even load distribution.
- Number of replicas is tunable based on how balanced you need the load to be.

```mermaid
flowchart LR
    subgraph Single["1 point per server - uneven arcs"]
        direction LR
        SA((A)) -->|small arc| SB((B))
        SB -->|large arc| SC((C))
        SC -->|wraps to start| SA
    end
    subgraph Multi["3 points per server - balanced arcs"]
        direction LR
        MA1((A-v1)) --> MB1((B-v1))
        MB1 --> MC1((C-v1))
        MC1 --> MA2((A-v2))
        MA2 --> MB2((B-v2))
        MB2 --> MC2((C-v2))
        MC2 -->|wraps to start| MA1
    end
    Single -.->|replicate each server at multiple points| Multi
```

## Trade-offs / Comparisons
- Plain `hash % N`: simple, perfectly even split — but any change to N reshuffles almost all keys.
- Consistent hashing: slightly more complex (ring + virtual nodes) — but only ~`1/N` of keys move on any add/remove.
- Rule of thumb mentioned: a well-tuned consistent hashing ring should reshuffle close to `1/N` of keys on a node change, not more.

## Example / Walkthrough
- Load balancer with 3 app servers, using `mod 3` to route requests — works until a 4th server is added, then routing rule becomes `mod 4` and most in-flight assumptions about "which server has what" break.
- DB sharding example: 3 DB partitions splitting rows by `id % 3`. Adding partition 4 changes the modulo for nearly every row → massive rebalancing of already-stored data.
- Consistent hashing ring example: servers S1–S4 hashed onto random points on a ring; a key hashes to a point and is handled by the next server clockwise.
- Adding a new server S5 to the ring: only the keys in the arc between S5 and its counter-clockwise neighbor move to S5; all other keys' server assignment is unchanged.
- Removing a server: its keys fall through to the next server clockwise; rest of the ring is unaffected.
- Virtual nodes example: instead of placing S1 once, place it at several random points on the ring (aliased as S1 at each) so its share of the ring isn't just one lucky/unlucky arc.

## Diagram
Full ring with virtual nodes — each physical server (A, B, C) placed at multiple
points around the ring so no single server owns one unlucky/lucky large arc:
```mermaid
flowchart LR
    A1((A-v1)) --> B1((B-v1))
    B1 --> A2((A-v2))
    A2 --> C1((C-v1))
    C1 --> B2((B-v2))
    B2 --> A3((A-v3))
    A3 --> C2((C-v2))
    C2 -->|wraps to start| A1
```

## Interview Q&A
<details>
<summary>Why doesn't plain `hash % N` work well for a dynamic set of servers?</summary>

Because changing N (adding/removing a server) changes the modulo result for almost every key, forcing a near-total rebalance/reshuffle of data or routing.

</details>

<details>
<summary>What problem does consistent hashing solve?</summary>

It minimizes the number of keys that need to move when a server is added or removed — only about `1/N` of keys are affected instead of nearly all of them.

</details>

<details>
<summary>How are servers and keys placed in consistent hashing?</summary>

Both are hashed onto the same circular hash space (ring); a key is assigned to the first server encountered walking clockwise from the key's position.

</details>

<details>
<summary>What happens to keys when a new server joins the ring?</summary>

Only the keys in the arc between the new server and its counter-clockwise neighbor move to it — the rest of the ring's key-to-server mapping is untouched.

</details>

<details>
<summary>Why use virtual nodes instead of one ring position per server?</summary>

A single random point per server can give an uneven split of the ring (unbalanced load). Multiple virtual nodes per server spread its coverage across the ring more evenly.

</details>

<details>
<summary>Where is consistent hashing used in real systems?</summary>

Load balancers distributing traffic across app servers, distributed caches, and sharded/distributed databases — anywhere the set of nodes can grow or shrink.

</details>

## Related Topics
- [05. Scale from Zero to a Million Users](05-scale-zero-to-million-users.md) — load balancing and sharding context this builds on
