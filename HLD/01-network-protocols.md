# Network Protocols

## Overview
- Two OSI layers matter for HLD: application layer and transport layer
- Protocol choice depends on the use case, not preference — chat needs push, video needs speed, pages need simple request/response

## Key Concepts

### What's a network protocol
- Rules two systems agree on so they can talk, even without understanding each other beyond the rules

### Client-server vs peer-to-peer
- **Client-server** — client always initiates, server responds (HTTP, FTP, SMTP)
- **WebSocket** — still client-server, but bidirectional once connected; server can push without being asked
- **Peer-to-peer** — any node can act as client or server, talks directly to other nodes, no central hop (WebRTC)

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    C->>S: HTTP request
    S-->>C: HTTP response (only after a request)
    Note over C,S: WebSocket — after one handshake, either side can send anytime
    C->>S: connect (handshake)
    S-->>C: connection open
    S->>C: push new message (server-initiated, no request needed)
```

### Application layer protocols
- **HTTP** — connection-oriented, used for web pages; HTTPS = HTTP + encryption
- **FTP** — two connections: control (stays open) + data (per transfer); data connection is unencrypted → replaced by HTTPS
- **SMTP** — sends mail, via a Message Transfer Agent (MTA)
- **IMAP** — reads mail off the server, syncs across devices — modern default
- **POP3** — downloads mail then deletes from server — mostly deprecated

```mermaid
flowchart LR
    Client -->|control connection - stays open| Server
    Client -->|data connection - opened per transfer, closed after| Server
```

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Mail Server
    Note over C,S: IMAP — mail stays on server, client syncs
    C->>S: fetch headers/messages
    S-->>C: messages (copy, stays on server)
    Note over C,S: POP3 — mail downloaded then removed
    C->>S: download messages
    S-->>C: messages
    C->>S: delete after download
```

### Transport layer protocols
- **TCP** — connection-oriented, packets sequenced + acknowledged, guarantees ordering, reliable but slower
- **UDP** — no connection, no ordering, no acknowledgement, best-effort delivery, fast

```mermaid
sequenceDiagram
    participant A as Sender
    participant B as Receiver
    Note over A,B: TCP — connection setup, then sequenced + acked
    A->>B: SYN
    B-->>A: SYN-ACK
    A->>B: ACK
    A->>B: data packet (seq 1)
    B-->>A: ack (seq 1)
    Note over A,B: UDP — no handshake, no ack, fire and forget
    A->>B: datagram (no seq, no ack)
```

## Diagram
```mermaid
graph LR
  subgraph "Client-Server (HTTP, WebSocket)"
    C1[Client 1] -->|request| S[Server]
    S -->|response| C1
    C2[Client 2] -->|request| S
    S -->|response| C2
  end
  subgraph "Peer-to-Peer (WebRTC)"
    P1[Peer 1] <-->|direct| P2[Peer 2]
  end
```
- Client-Server: clients never talk to each other, only through the server
- Peer-to-Peer: nodes talk directly, no server hop

## Trade-offs / Comparisons
| Protocol | Layer | Style | Guarantees | Use case |
|---|---|---|---|---|
| HTTP(S) | App, client-server | Request/response | Reliable | Web pages, APIs |
| WebSocket | App, client-server | Persistent, bidirectional | Reliable | Messaging apps |
| WebRTC | App, peer-to-peer | Direct P2P | Best-effort (over UDP) | Video calls, live streaming |
| FTP | App, client-server | Control + data connections | Reliable, unencrypted | Legacy — avoid |
| TCP | Transport | Sequenced + acked | Ordered, reliable | Anything needing correctness |
| UDP | Transport | Parallel datagrams | Unordered, lossy, fast | Live video/audio |

## Example / Walkthrough
- **Messaging app (WhatsApp):** WebSocket — server must push new messages to the recipient and push delivery acks back to sender, both server-initiated
- **Video calling (Google Meet):** WebRTC over UDP — skip the server hop, drop frames instead of retransmitting

## Interview Q&A
<details>
<summary>Is WebSocket peer-to-peer?</summary>

No — still client-server, just bidirectional; clients never talk to each other directly.

</details>

<details>
<summary>Why UDP over TCP for video calls?</summary>

Skips ordering/ack/retransmit overhead — a dropped frame is fine, a stalled stream isn't.

</details>

<details>
<summary>Why WebSocket instead of HTTP for chat?</summary>

HTTP can't let the server push without the client polling; WebSocket keeps the channel open both ways.

</details>

<details>
<summary>Why is WebRTC faster than routing through a server?</summary>

Peer-to-peer — data goes directly between machines, no extra hop.

</details>

<details>
<summary>Why did HTTPS replace FTP for file transfer?</summary>

FTP's data connection is unencrypted; HTTPS gives the same transfer with encryption.

</details>

<details>
<summary>IMAP vs POP3?</summary>

POP3 downloads and deletes from server (single device); IMAP syncs and stays on server (multi-device) — IMAP is standard now.

</details>

<details>
<summary>How does TCP guarantee ordering over an unordered network?</summary>

Packets are sequenced and acknowledged individually; missing acks trigger resends, receiver reassembles by sequence number.

</details>

## Related Topics
- Feeds into WhatsApp design and rate limiter (WebSocket/HTTP) and autocomplete (HTTP) later in [[00-roadmap]]
