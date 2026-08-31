# Design Patterns Catalog

## Overview
- Full checklist of the classic (GoF) design patterns, grouped by category,
  so we always know what's covered and what's left to add.
- ✅ = covered by a note in this repo (linked). ⬜ = not yet covered — one-line
  description kept here as a placeholder until it gets its own note.
- Case-study LLDs (parking lot, BookMyShow, etc.) aren't patterns
  themselves — they *combine* patterns from below; see the note at the
  bottom.

## Creational — controls how objects get created
- ⬜ **Singleton** — ensure a class has exactly one instance, with a global access point to it
- ⬜ **Factory Method** — subclasses decide which concrete class to instantiate, behind a common creation method
- ✅ [Factory vs Abstract Factory](05-factory-vs-abstract-factory-pattern.md) — centralize condition-based object creation; abstract factory adds a factory-of-factories layer for grouped product families
- ✅ [Builder](22-builder-design-pattern.md) — construct a complex object step-by-step via a Builder + optional Director, avoiding telescoping constructors
- ⬜ **Prototype** — create new objects by cloning an existing instance instead of instantiating from scratch

## Structural — controls how classes/objects are arranged together
- ✅ [Adapter](20-adapter-design-pattern.md) — bridge an existing interface and an expected interface via both is-a and has-a
- ⬜ **Bridge** — decouple an abstraction from its implementation so the two can vary independently
- ✅ [Composite](19-composite-design-pattern.md) — shared leaf/composite interface to model tree-shaped problems without instanceof branching
- ✅ [Decorator](04-decorator-design-pattern.md) — add features by wrapping at runtime instead of subclassing per combination
- ⬜ **Facade** — one simplified interface hiding a complex subsystem of classes
- ⬜ **Flyweight** — share common state across many fine-grained objects to cut memory use
- ✅ [Proxy](13-proxy-design-pattern.md) — centralize access validation/logging behind a stand-in that implements the same interface as the real object

## Behavioral — controls how objects communicate/interact once created
- ✅ [Chain of Responsibility](10-chain-of-responsibility-pattern.md) — a request travels through a chain of receivers until one handles it
- ⬜ **Command** — encapsulate a request as an object, enabling queuing, undo/redo, and logging of operations
- ⬜ **Interpreter** — define a grammar and an interpreter that evaluates sentences in that grammar
- ⬜ **Iterator** — access elements of a collection sequentially without exposing its underlying structure
- ⬜ **Mediator** — centralize how a set of objects interact, so they don't reference each other directly
- ⬜ **Memento** — capture and restore an object's internal state without violating encapsulation
- ✅ [Observer](03-observer-design-pattern.md) — auto-notify subscribers on state change
- ✅ [State](16-vending-machine-lld.md) — one class per state, context delegates every action to its current state (canonical example: Vending Machine; reused in [ATM](17-atm-lld.md))
- ✅ [Strategy](02-strategy-design-pattern.md) — swap out an algorithm/capability at runtime via composition
- ⬜ **Template Method** — define an algorithm's skeleton in a base class, letting subclasses override specific steps
- ⬜ **Visitor** — separate an operation from the object structure it operates on, so new operations don't touch existing classes

## Other commonly-taught patterns (non-GoF)
- ✅ [Null Object](15-null-object-pattern.md) — replace null with a default-behavior object to remove scattered null-checks

## Patterns combined in case-study LLDs
- [Parking Lot](06-parking-lot-lld.md) — Strategy (find-spot, pricing) + Factory (manager, cost computation)
- [ATM](17-atm-lld.md) — State (operation flow) + Chain of Responsibility (denomination-based cash withdrawal)
- [BookMyShow](14-bookmyshow-lld.md) — Strategy-flavored composition for seat/booking logic

## Related Topics
- [00a. What is LLD](00a-what-is-lld.md) — the creational/structural/behavioral definitions this catalog groups by
