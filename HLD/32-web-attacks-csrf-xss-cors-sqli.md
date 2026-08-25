# Common Web Attacks: CSRF, XSS, CORS, SQL Injection

## Overview
- Four foundational web security concepts, essential background before diving into a framework's security layer (e.g. Spring Security) or discussing security in a system design interview.
- Three are attacks (CSRF, XSS, SQL Injection); CORS itself is not an attack — it's a browser-enforced security feature that helps defend against cross-origin abuse.
- Common thread: user input or browser-automatic behavior (cookies, session handling) gets trusted or used unsafely by a server/browser, and an attacker exploits that trust.
- Demonstrated with live Spring Boot examples in the source video — this note captures the concepts and mitigations, not the demo mechanics.

## Key Concepts

### CSRF (Cross-Site Request Forgery)
- Tricks a user's browser into making an unwanted request to a site where the user is **already authenticated** — most applicable to session/cookie-based (stateful) authentication.
- Mechanism: browser stores a session ID in a cookie after login; browsers **automatically attach** cookies to any request sent to that domain, regardless of what triggered the request.
- Attacker crafts a malicious link/page that silently fires a request to the target site (e.g. a money-transfer endpoint); since the victim's browser auto-attaches the valid session cookie, the server sees what looks like a legitimate, authenticated request.
- Victim is unaware — they only clicked a link expecting something else, but a hidden request fired in the background using their active session.
- **Mitigation — CSRF token:** server returns a token (in addition to the cookie) that only a legitimate, authenticated page/form knows and can append to its requests; an attacker's external page has no way to know or include this token, so the server can reject requests missing it.

```mermaid
sequenceDiagram
    participant U as User's Browser
    participant Target as Target Site (e.g. Gmail/Bank)
    participant Attacker as Attacker's Page

    U->>Target: login
    Target->>U: session cookie stored
    U->>Attacker: clicks malicious link
    Attacker->>U: page auto-fires request to Target
    U->>Target: request (browser auto-attaches session cookie)
    Target->>Target: cookie looks valid → request appears authenticated
    Target->>U: unwanted action executed (e.g. money transferred)
```

### XSS (Cross-Site Scripting)
- Allows an attacker to inject a malicious script into a web page that will be viewed by **other users** — the victim's own browser ends up executing the attacker's script as if it were the page's own code.
- Classic scenario: a comment/post feature stores raw user input and re-renders it unescaped for every viewer; if the "comment" is actually `<script>...</script>`, every viewer's browser executes it.
- Impact ranges from a harmless popup (proof of concept) up to **session/cookie theft** — a script reading `document.cookie` and sending it to an attacker-controlled endpoint lets the attacker hijack the victim's authenticated session entirely, or the page can be defaced.
- **Mitigation:**
  - **Escape special characters** in user input before rendering (e.g. `<script>` → its HTML-entity-escaped form) so the browser treats it as inert text, not executable markup.
  - **Input validation** — restrict what characters/patterns are allowed in user-submitted fields in the first place.

```mermaid
sequenceDiagram
    participant Attacker as Attacker
    participant Server as Server (stores comments)
    participant Victim as Other User's Browser

    Attacker->>Server: POST /comment with <script>steal cookie</script>
    Server->>Server: stores raw, unescaped input
    Victim->>Server: GET /comments (loads page)
    Server->>Victim: returns comment list, including the script
    Victim->>Victim: browser executes injected script
    Victim->>Attacker: document.cookie exfiltrated
```

### CORS (Cross-Origin Resource Sharing)
- **Not an attack** — a browser-enforced security feature that restricts web pages from making requests to a different **origin** unless the server explicitly allows it.
- **Origin** = protocol + domain + port, all three must match for two URLs to be considered the "same origin"; differing on any one (e.g. `http` vs `https`, different subdomain, different port) counts as a different origin.
- Server controls which origins are permitted via response headers (e.g. `Access-Control-Allow-Origin`, allowed methods, allowed headers) — configured per allowed origin list, methods (GET/POST/PUT/DELETE), and headers.
- Acts as a **first line of defense**: if an attacker's page runs on a different origin, the browser blocks its cross-origin request to the target server outright, before it even needs CSRF tokens or other server-side checks to kick in.
- Same-origin requests are always allowed by default; CORS configuration only matters for legitimately-needed cross-origin access (e.g. a frontend on one port calling a backend API on another).

```mermaid
flowchart LR
    ClientA["Allowed Origin\nhttps://sub.local:9090"] -->|allowed by CORS config| Server[Server]
    ClientB["Different Protocol\nhttp://sub.local:9090"] -.->|blocked: different origin| Server
    ClientC["Different Port\nhttps://sub.local:8080"] -.->|blocked: different origin| Server
    ClientD["Different Domain\nlocal vs sub.local"] -.->|blocked: different origin| Server
```

### SQL Injection
- Attacker manipulates a SQL query by inserting malicious input into a user-controlled field that gets concatenated directly into the query string.
- Classic technique: injecting logic that always evaluates true (e.g. `' OR 1=1`) into a `WHERE` clause, turning a query meant to filter by a specific value into one that returns **all rows**, bypassing the intended filter/authorization entirely.
- Beyond just leaking extra rows, attackers can potentially discover table/column names, access unauthorized data, or even drop tables/databases, depending on the query's privileges and structure.
- **Mitigation — parameterized queries:** bind user input as a query **parameter/value**, not as raw concatenated query text, so the database treats it strictly as data (a literal string to match) rather than executable query syntax — injected logic like `OR 1=1` then simply fails to match anything instead of altering the query's structure.

```mermaid
flowchart TD
    subgraph Vulnerable["Vulnerable: string concatenation"]
        Input1["User input: ' OR 1=1"] --> Query1["SELECT * FROM user_details\nWHERE username = '' OR 1=1"]
        Query1 --> Result1["Returns ALL rows\n(condition always true)"]
    end
    subgraph Safe["Safe: parameterized query"]
        Input2["User input: ' OR 1=1"] --> Query2["SELECT * FROM user_details\nWHERE username = ?\n(bound as literal value)"]
        Query2 --> Result2["No match found\n(treated as literal string, not SQL)"]
    end
```

## Trade-offs / Comparisons
| Attack | Exploits | Root cause | Primary mitigation |
|---|---|---|---|
| CSRF | Browser auto-attaching session cookies | Server trusts any request carrying a valid session cookie | CSRF token unknown to attacker pages |
| XSS | Browser executing injected script as page content | Unescaped user input rendered as HTML/JS | Escape output, validate input |
| CORS (defense) | N/A — browser-enforced restriction | N/A | Explicit origin/method/header whitelisting |
| SQL Injection | Query built via raw string concatenation | User input treated as executable query syntax | Parameterized queries |

## Example / Walkthrough
- **CSRF demo:** a server requires authentication for all requests including `/transfer`; user logs in via session-based auth and gets a session cookie. A crafted HTML page (hosted elsewhere) auto-submits a request to `/transfer` when clicked; because the browser automatically attaches the existing session cookie, the server treats it as a legitimate authenticated request and executes the transfer — the same session ID observed in the login response reappears in the malicious request's cookie header.
- **XSS demo:** a `/xss` page renders stored comments via a server-side template (`@Controller`, not `@RestController`, so the HTML is rendered); a `POST /comment` endpoint stores raw comment text in memory/DB without escaping. Submitting `<script>alert('xss attack')</script>` as a comment causes the alert popup to fire for every subsequent viewer of the comments page — demonstrating that the script executes in the victim's browser. Swapping the payload for one that reads `document.cookie` and sends it to an attacker endpoint would exfiltrate session cookies instead of just popping an alert.
- **CORS demo:** server configuration whitelists a specific allowed origin (e.g. `https://sub.local:9090`) for GET/POST/PUT/DELETE plus specific headers; requests from any other protocol, port, or domain combination are rejected by the browser before reaching application logic.
- **SQL Injection demo:** a `/find` endpoint builds a query like `SELECT * FROM user_details WHERE username = '<input>'` by direct string substitution. Normally submitting a username returns just that user's row. Submitting `' OR 1=1` (crafted so the resulting query becomes `WHERE username = '' OR 1=1`) returns **every row in the table**, since `1=1` is always true — demonstrating unauthorized data exposure from unsanitized query construction. Using a parameterized query (binding the input as a literal parameter rather than concatenating it) makes the same payload match nothing, since it's treated as a literal string value, not query syntax.

## Diagram
```mermaid
flowchart TB
    subgraph CSRF["CSRF"]
        C1["Browser auto-attaches session cookie"] --> C2["Attacker page triggers unwanted request"] --> C3["Mitigate: CSRF token"]
    end
    subgraph XSS["XSS"]
        X1["Unescaped user input stored/rendered"] --> X2["Victim's browser executes injected script"] --> X3["Mitigate: escape output + validate input"]
    end
    subgraph CORS["CORS (defense, not attack)"]
        O1["Browser checks request origin\n(protocol+domain+port)"] --> O2["Server allow-list decides"] --> O3["Blocks cross-origin unless whitelisted"]
    end
    subgraph SQLi["SQL Injection"]
        S1["User input concatenated into query string"] --> S2["Malicious input alters query logic\n(e.g. OR 1=1)"] --> S3["Mitigate: parameterized queries"]
    end
```

## Interview Q&A
<details>
<summary>What is CSRF and why does it primarily affect session/cookie-based authentication?</summary>

CSRF tricks a user's browser into sending an unwanted request to a site where they're already authenticated. It's tied to session-based auth because browsers automatically attach stored cookies (including the session ID) to any request sent to that domain, regardless of what triggered the request — the server has no way to distinguish a legitimate user action from an attacker-triggered one just by seeing a valid cookie.

</details>

<details>
<summary>How does a CSRF token protect against CSRF attacks?</summary>

The server issues a token known only to legitimate, authenticated forms/pages; since an attacker's external page has no way to obtain or include this token, requests missing it can be rejected, even if the browser auto-attaches a valid session cookie.

</details>

<details>
<summary>What is XSS, and what's the worst-case impact beyond a simple alert popup?</summary>

Cross-Site Scripting lets an attacker inject a malicious script into content later rendered for other users, whose browsers then execute it. Beyond a harmless popup, a script can read `document.cookie` and exfiltrate it to an attacker-controlled server, allowing full session hijacking wherever that session/cookie is valid.

</details>

<details>
<summary>What are the two main mitigations for XSS?</summary>

Escaping special characters in user input before rendering it (so the browser treats it as inert text, not executable code), and validating what input is allowed in the first place.

</details>

<details>
<summary>Is CORS an attack? What does it actually do?</summary>

No — CORS is a browser-enforced security feature (not an attack) that restricts a web page from making requests to a different origin (protocol + domain + port) unless the target server explicitly allows it via response headers like Access-Control-Allow-Origin.

</details>

<details>
<summary>What counts as a "different origin" under CORS?</summary>

Any difference in protocol, domain, or port between the requesting page and the target server — e.g. http vs https, a different subdomain, or a different port number, even if the rest of the URL matches.

</details>

<details>
<summary>How does SQL injection work, and what does a payload like ' OR 1=1 accomplish?</summary>

It exploits queries built by directly concatenating unsanitized user input into SQL text. A payload like `' OR 1=1` turns a WHERE clause intended to match one specific value into a condition that's always true, causing the query to return every row in the table instead of the intended filtered result.

</details>

<details>
<summary>How do parameterized queries prevent SQL injection?</summary>

They bind user input as a literal parameter/value rather than concatenating it directly into the query text, so the database engine treats it strictly as data to match against — not as executable query syntax — meaning injected logic like `OR 1=1` simply fails to match anything instead of altering the query's structure.

</details>

## Related Topics
- [[26-jwt]] — token-based (stateless) auth as an alternative to session/cookie-based auth that CSRF specifically targets
- [[24-oauth-2]] — authorization framework where CSRF-style state-token protections (the `state` parameter) follow the same principle as CSRF tokens
