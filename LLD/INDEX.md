- [00. Roadmap](00-roadmap.md) — planned topic order for LLD prep

## Concepts
- [00a. What is LLD](concepts/00a-what-is-lld.md) — LLD vs HLD, creational/structural/behavioral patterns, is-a vs has-a
- [00b. Java Interfaces](concepts/00b-java-interfaces.md) — static/default methods, achieving multiple inheritance
- [00c. Design Patterns Catalog](concepts/00c-design-patterns-catalog.md) — checklist of all GoF patterns by category, which are covered vs. still to add
- [01. SOLID Principles](concepts/01-solid-principles.md) — SRP, OCP, LSP, ISP, DIP with examples
- [01.1. LSP with Solution](concepts/01.1-lsp-solution.md) — fixing an LSP violation via inheritance restructuring
- [01.2. is-a vs has-a: How Each Looks in Code](concepts/01.2-is-a-vs-has-a.md) — extends/implements vs constructor-injected field, and when a class needs both
- [02. Strategy Design Pattern](concepts/02-strategy-design-pattern.md) — composition over inheritance via a swappable strategy interface
- [03. Observer Design Pattern](concepts/03-observer-design-pattern.md) — auto-notify subscribers on state change, constructor-injected observers
- [04. Decorator Design Pattern](concepts/04-decorator-design-pattern.md) — add features by wrapping at runtime instead of subclassing per combination
- [05. Factory vs Abstract Factory Pattern](concepts/05-factory-vs-abstract-factory-pattern.md) — centralize condition-based object creation; abstract factory adds a factory-of-factories layer for grouped product families
- [10. Chain of Responsibility Design Pattern](concepts/10-chain-of-responsibility-pattern.md) — request forwarded through a chain of receivers until handled; logging system worked example
- [12. HashMap Internal Implementation](concepts/12-hashmap-internal-implementation.md) — bucket chaining, power-of-2 capacity, hash spreading, load-factor resize
- [13. Proxy Design Pattern](concepts/13-proxy-design-pattern.md) — centralize access validation/logging behind a proxy that implements the same interface as the real object
- [15. Null Object Pattern](concepts/15-null-object-pattern.md) — replace null with a default-behavior object to remove scattered null-checks
- [19. Composite Design Pattern](concepts/19-composite-design-pattern.md) — shared leaf/composite interface to model tree-shaped problems (file system, expression tree) without instanceof branching
- [20. Adapter Design Pattern](concepts/20-adapter-design-pattern.md) — bridge an existing interface and an expected interface via both is-a and has-a, e.g. converting pounds to kg
- [22. Builder Design Pattern](concepts/22-builder-design-pattern.md) — step-by-step object construction to avoid telescoping constructors, plus Director orchestration and the Builder vs. Decorator distinction
- [24. Facade Design Pattern](concepts/24-facade-design-pattern.md) — hide subsystem complexity behind one simplified interface; contrasted with Proxy (same interface, one object) and Adapter (solves incompatibility, not complexity)

## Examples
- [06. LLD of Parking Lot](examples/06-parking-lot-lld.md) — requirements-first design combining Strategy (find-spot, pricing) and Factory (manager, cost-computation) patterns
- [07. LLD of Tic-Tac-Toe](examples/07-tic-tac-toe-lld.md) — extensible board/symbols/players via abstract Piece and a turn queue
- [09. LLD of Car Rental System](examples/09-car-rental-system-lld.md) — store/location/inventory/reservation design, keep interview scope as simple as asked
- [11. LLD of Snake and Ladder](examples/11-snake-and-ladder-lld.md) — Jump superclass shared by Snake/Ladder, random board setup, turn-queue rotation
- [14. LLD of BookMyShow](examples/14-bookmyshow-lld.md) — movie ticket booking class design + optimistic locking for concurrent seat booking
- [16. LLD of Vending Machine](examples/16-vending-machine-lld.md) — one class per machine state (State Design Pattern), context delegates every button press to current state
- [17. LLD of ATM](examples/17-atm-lld.md) — State pattern for the operation flow + Chain of Responsibility for denomination-based cash withdrawal
- [18. LLD of Chess Game (Mock Interview)](examples/18-chess-game-lld.md) — Cell owns position not Piece, abstract Piece per type, move-as-validation vs move-as-mutation, plus interview-process lessons
- [21. LLD of Splitwise](examples/21-splitwise-lld.md) — Equal/Unequal/Percentage splits via a Factory, per-user friend-balance-sheet updates on each expense; plus Part 2: the Simplify debt-reduction algorithm (DFS/backtracking, NP-hard)
- [23. LLD of Cricbuzz / CricInfo](examples/23-cricbuzz-lld.md) — Match/Innings/Over/Ball hierarchy, batting/bowling controllers, MatchType polymorphism, Observer-driven scorecard updates
