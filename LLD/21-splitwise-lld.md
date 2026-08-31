# LLD of Splitwise (Expense Sharing App)

## Overview
- Design an expense-sharing app (Splitwise-style) — a very popular,
  frequently-asked LLD interview question.
- Start from requirement gathering: use the real app's happy path (add
  friends, add a group, add an expense, split it, check balances) to derive
  the requirements instead of guessing them upfront.
- Core design challenge is the **split** abstraction (equal / unequal /
  percentage) and how one expense update correctly fans out into every
  affected user's **balance sheet**.

## Key Concepts
### Requirements (from the happy path)
- Add friends to your account.
- Create a group, and add members to that group.
- Create an expense either **inside a group** or **directly between
  friends**, not attached to any group — both flows must be supported.
- When creating an expense, split the amount between friends using one of
  three types: **Equal**, **Unequal** (exact amount per person), or
  **Percentage**.
  - Equal — total divided evenly across the chosen friends.
  - Unequal/Exact — each friend is assigned an explicit amount; all the
    amounts must sum up to the total expense amount.
  - Percentage — each friend is assigned a percentage; all percentages
    must sum up to 100%.
- View a friend's or the whole account's **balance sheet** — how much you
  owe each friend, and how much each friend owes you, with a drill-down
  per friend.
- Removing a member from a group only removes them from that group, not
  from Splitwise itself — group membership and app-wide user identity are
  separate concerns.

### Core entities
- `User` — has a list of friends and maintains its own **balance sheet**:
  a map of friend → `FriendBalance` (how much to get back from / owe that
  specific friend).
- `Group` — groupId, groupName, its own list of member `User`s (add/remove
  member), and its own list of `Expense`s (add/remove expense).
- `Expense` — title/description, total amount, the `User` who paid, and a
  list of `Split`s.
- `Split` — a user and the amount that user owes for this expense; base
  type extended by `EqualSplit`, `UnequalSplit` (exact amount), and
  `PercentageSplit`.
- `FriendBalance` — per-friend running totals: how much you get back from
  this friend, how much you owe this friend.

```mermaid
classDiagram
    class User {
        -String userId
        -List~User~ friends
        -Map~User, FriendBalance~ balanceSheet
    }
    class Group {
        -String groupId
        -String groupName
        -List~User~ members
        -List~Expense~ expenses
        +addMember(User)
        +removeMember(User)
        +addExpense(Expense)
    }
    class Expense {
        -String title
        -double amount
        -User paidBy
        -List~Split~ splits
    }
    class Split {
        <<abstract>>
        -User user
        -double amount
    }
    class EqualSplit
    class UnequalSplit
    class PercentageSplit
    class FriendBalance {
        -double totalYouGetBack
        -double totalYouOwe
    }

    Split <|-- EqualSplit
    Split <|-- UnequalSplit
    Split <|-- PercentageSplit
    Expense --> Split : has many
    Group --> User : has many members
    Group --> Expense : has many
    User --> FriendBalance : maintains per friend
```

### Split creation — Factory pattern
- A `SplitFactory` returns the right concrete `Split` implementation
  (`EqualSplit`/`UnequalSplit`/`PercentageSplit`) based on the requested
  split type — same [[05-factory-vs-abstract-factory-pattern]] used
  elsewhere, see the full [[00c-design-patterns-catalog]].
- For percentage splits, two client scenarios are both valid: the UI
  computes the rupee amount from the percentage client-side and sends the
  amount, **or** the client sends only the percentage and the server
  computes the amount — the design should support either without changing
  the `Expense`/`Split` model.
- This is naturally extensible under OCP: if the server needs to compute
  amount from percentage, that logic can be added inside the
  `PercentageSplit` class itself (a new method) without touching
  `EqualSplit`/`UnequalSplit` or any other class.

```java
enum SplitType { EQUAL, UNEQUAL, PERCENTAGE }

abstract class Split {
    User user;
    double amount;
}
class EqualSplit extends Split { }
class UnequalSplit extends Split { } // exact amount per user
class PercentageSplit extends Split {
    double percentage;
    void computeAmount(double totalAmount) { // extension point, OCP: add without touching other Split types
        this.amount = totalAmount * percentage / 100;
    }
}

class SplitFactory {
    Split getSplitObject(SplitType type) {
        switch (type) {
            case EQUAL: return new EqualSplit();
            case UNEQUAL: return new UnequalSplit();
            case PERCENTAGE: return new PercentageSplit();
        }
        throw new IllegalArgumentException();
    }
}
```

### Creating an expense — validation and flow
- Client calls `ExpenseController.createExpense(...)` with: who paid, the
  split details (which friend owes how much/what percentage), the total
  expense amount, and a description.
- `ExpenseController` asks `SplitFactory` for the right `Split` objects,
  then validates the request before creating the `Expense`:
  - Percentage split — all percentages must add up to 100%.
  - Unequal/exact split — all individual amounts must add up to the total
    expense amount.
- Validation is written as its own extensible step, so a new split type's
  validation rule can be added without touching the others.
- Once valid, `ExpenseController` builds the `Expense` object and calls
  `BalanceSheetController` to update every affected user's balance sheet.

```mermaid
sequenceDiagram
    participant Client
    participant ExpenseController
    participant SplitFactory
    participant BalanceSheetController

    Client->>ExpenseController: createExpense(paidBy, splits, amount, description)
    ExpenseController->>SplitFactory: getSplitObject(type)
    SplitFactory-->>ExpenseController: Split instance(s)
    ExpenseController->>ExpenseController: validate (percentages sum to 100% / amounts sum to total)
    ExpenseController->>ExpenseController: create Expense
    ExpenseController->>BalanceSheetController: updateBalanceSheet(expense)
    BalanceSheetController-->>ExpenseController: done
```

### Updating the balance sheet
- `BalanceSheetController` holds the business logic for turning one
  `Expense` into balance-sheet updates — kept out of `ExpenseController` so
  each controller owns one responsibility.
- It iterates over the expense's `Split`s:
  - The payer's own split is just counted toward their own total spend —
    you don't owe yourself, so it doesn't touch any `FriendBalance`.
  - For every other user in the split, their `FriendBalance` entry for the
    payer is debited ("you owe this friend"), and the payer's
    `FriendBalance` entry for that user is credited ("you get back from
    this friend").
- Because each `User` keeps its own friend → `FriendBalance` map, a
  drill-down per friend (and a rolled-up total) is just a map read/iterate,
  not a fresh computation.
- Same separation-of-concerns reasoning applies to `Group`: group
  membership (`addMember`/`removeMember`) and its own expense list live
  inside `GroupController`/`Group` itself — otherwise that logic would leak
  into the top-level Splitwise app/driver class.

```mermaid
flowchart TB
    Iter["Iterate over Expense.splits"]
    Iter --> Self{"Split.user == paidBy?"}
    Self -->|yes| Own["Add to payer's own total expense\n(no FriendBalance update)"]
    Self -->|no| Other["Debit this user's FriendBalance for payer (owes)\nCredit payer's FriendBalance for this user (gets back)"]
```

## Trade-offs / Comparisons
| Split type | What's validated | Who computes the amount |
|---|---|---|
| Equal | N/A — computed as total ÷ number of friends | Server |
| Unequal/Exact | Sum of amounts == total expense amount | Client sends explicit amounts |
| Percentage | Sum of percentages == 100% | Either client (UI converts % → amount) or server (extend `PercentageSplit` to compute) |

## Example / Walkthrough
- Create an expense titled "Lunch", amount 400, split between all friends
  in the group.
- Client picks a split type (equal/unequal/percentage) — e.g. percentage,
  assigning each friend a share that must sum to 100%.
- `ExpenseController.createExpense()` gets the split type's `Split` objects
  from `SplitFactory`, validates the percentages sum correctly, builds the
  `Expense`, and hands off to `BalanceSheetController`.
- `BalanceSheetController` walks each `Split`: the payer's own portion adds
  to their own total spend only; every other friend's portion updates two
  `FriendBalance` entries — that friend now owes the payer, and the payer
  now expects to get that amount back from that friend.

## Diagram
```mermaid
classDiagram
    class UserController
    class GroupController
    class ExpenseController
    class BalanceSheetController
    class SplitFactory

    UserController --> User : manages
    GroupController --> Group : manages
    ExpenseController --> SplitFactory : requests Split objects
    ExpenseController --> Expense : creates
    ExpenseController --> BalanceSheetController : triggers update
    BalanceSheetController --> User : updates balanceSheet map
    Group --> User : members
    Group --> Expense : owns
```

## Interview Q&A
<details>
<summary>What are the three split types Splitwise must support, and what does each validate?</summary>

Equal (total ÷ number of friends, nothing to validate), Unequal/Exact
(sum of amounts must equal the total expense amount), and Percentage (sum
of percentages must equal 100%).

</details>

<details>
<summary>Which design pattern creates the right Split object, and why use it here?</summary>

Factory — a `SplitFactory` returns the correct `EqualSplit`/`UnequalSplit`/
`PercentageSplit` based on the requested type, keeping `ExpenseController`
free of type-checking/branching logic when new split types are added.

</details>

<details>
<summary>Can an expense exist without being part of a group?</summary>

Yes — an expense can be created either inside a group or directly between
friends with no group attached; both flows must be supported.

</details>

<details>
<summary>Who is responsible for updating balances when an expense is created?</summary>

`BalanceSheetController`, not `ExpenseController` — `ExpenseController`
validates and builds the `Expense`, then calls `BalanceSheetController` to
apply the balance updates, keeping the two responsibilities separate.

</details>

<details>
<summary>How does removing a member from a group affect their Splitwise account?</summary>

It doesn't — removing a member only removes them from that group's own
member list; it has no effect on their app-wide user account or their
existing friend balances.

</details>

<details>
<summary>If a percentage split needs the server to compute the actual amount, where does that logic go?</summary>

Inside `PercentageSplit` itself, as an added method — an OCP-friendly
extension, since `EqualSplit`, `UnequalSplit`, and the rest of the system
don't need to change.

</details>

<details>
<summary>Why does the payer's own portion of an expense not touch their FriendBalance map?</summary>

Because you can't owe yourself — the payer's own split is only added to
their own total spend; only the other participants' splits create entries
in the payer's and their own FriendBalance maps.

</details>

## Related Topics
- [[05-factory-vs-abstract-factory-pattern]] — the Factory pattern used to
  create the correct `Split` implementation.
- [[00c-design-patterns-catalog]] — full checklist of covered patterns,
  including Factory.
- [[14-bookmyshow-lld]] — another controller-per-entity case-study LLD with
  the same separation-of-concerns shape.
