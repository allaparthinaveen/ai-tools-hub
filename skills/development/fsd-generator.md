---
name: fsd-generator
description: >-
  Generates a Feature-Sliced Design (FSD) frontend architecture -- real folder structure, Public API index files, and code scaffolding -- from a groomed backlog (epics/stories/acceptance criteria) and/or a generated Figma design (screens + shared components), mapping business domains to entities, user actions to features, screens to pages, and shared UI kit pieces to the shared layer. Use this skill whenever the user asks to scaffold a frontend project, set up "feature-sliced design" or "FSD" architecture, turn a backlog or design into a codebase structure, generate the folder structure for a feature/app, or convert user stories into entities/features/pages in code. Chains naturally after the backlog-grooming and figma-design-generator skills, but works from a backlog alone if no design exists yet.
---

# Backlog/Design-to-FSD Generator

Turns requirements and/or a design (ideally the outputs of `backlog-grooming` and `figma-design-generator`) into an actual **Feature-Sliced Design** codebase: real directories, Public API (`index.ts`) barrel files per slice, and scaffolded (not fully implemented) components/stores/api-clients wired to match the import rules FSD requires.

## What Feature-Sliced Design is (reference, don't skip if unfamiliar)

FSD organizes a frontend app into **layers**, each layer split into **slices** (business domains), each slice split into **segments** (technical concerns). The critical rule that makes this different from a normal folder-by-type structure:

> **A module can only import from layers strictly below it.** Same-layer slices cannot import each other directly (except through `shared`). Higher layers can import lower ones; never the reverse.

| Layer | Purpose | Slice examples | Notes |
|---|---|---|---|
| `app` | App-wide setup: providers, routing, global styles, entry point | (no slices — this layer is global) | Composes everything below it |
| `pages` | One slice per routable screen | `login`, `product-list`, `checkout` | Usually thin — composes widgets/features |
| `widgets` | Composite, reusable chunks of UI made of multiple entities/features | `header`, `product-card-with-actions` | Use only when something is genuinely composite; don't force it |
| `features` | A user-facing action with business value | `auth-by-email`, `add-to-cart`, `filter-products` | Roughly 1:1 with backlog user stories |
| `entities` | Business domain nouns and how they're displayed/stored | `user`, `product`, `order`, `cart` | The "what the app is about," independent of any one feature |
| `shared` | Reusable, business-agnostic code | `ui` (design-system kit), `api` (base client), `lib`, `config` | No slices — flat segments. Cannot import from any other layer. |

Segments inside a slice (use only the ones a slice actually needs):
```
feature-name/
  ui/         — components
  model/      — state (store/hooks), types, selectors
  api/        — requests specific to this slice
  lib/        — slice-local helper functions
  config/     — slice-local constants
  index.ts    — Public API: the ONLY thing other layers may import
```

Everything not re-exported from `index.ts` is private to the slice. This is the mechanism that keeps the import rule enforceable — importing `features/add-to-cart/model/store` directly instead of `features/add-to-cart` is a violation even if it "works."

## Prerequisites — confirm the stack before scaffolding

If not already specified by the user or inferable from an existing project in the workspace, ask (or state a default and proceed if the request is casual/small):

- **Framework**: React, Vue, Svelte, or structure-only (folders + `index.ts` barrels, no components). Default: **React**, since it's what most FSD tooling/examples target — state this assumption if you pick it.
- **Styling**: Tailwind, CSS Modules, or CSS-in-JS. Default: **Tailwind**.
- **State management per slice**: a lightweight store (Zustand for React / Pinia for Vue) is the FSD-idiomatic default — it keeps state colocated with the slice instead of one global store. Fall back to local state/context for slices simple enough not to need one. Only reach for Redux Toolkit if the user already uses it or the app has genuinely complex cross-cutting state.

Detect an existing project (check for `package.json`, an existing `src/` structure) before assuming a fresh scaffold — if one exists, adapt to what's already there (existing framework/styling choice) rather than introducing a second stack.

## Workflow

### Step 1 — Gather inputs

Pull from whatever's available:
- **Backlog** (from `backlog-grooming`): Epics, Stories ("As a [role], I want [capability]..."), Acceptance Criteria
- **Design** (from `figma-design-generator`): screen inventory table, shared component list, states per screen

If only one input exists (e.g. backlog with no design yet), proceed from that alone — note in the output that UI detail is inferred from AC rather than an actual design, so component scaffolds will be rougher.

### Step 2 — Extract entities (the domain layer)

Read every story and AC for **nouns that represent persistent business concepts** — the things the app is *about*, independent of any specific action on them. `User`, `Product`, `Cart`, `Order` are entities; `login form` and `checkout button` are not — those are UI inside a feature.

Test: would this noun still make sense described to someone who's never seen the UI? "A cart holds items and a total" → entity. "A checkout button submits the cart" → feature detail, not an entity itself.

For each entity, scaffold:
```
entities/
  {entity}/
    model/
      types.ts       — the entity's shape
      store.ts        — (if the entity needs cross-feature shared state)
    ui/
      {Entity}Card.tsx   — smallest reusable display unit for this entity, if design shows one
    index.ts           — re-exports only what other layers should touch
```

### Step 3 — Extract features (the action layer)

Each user story is usually **one feature** — this is the layer where backlog and code map most directly. A story like "As a shopper, I want to add an item to my cart" becomes:

```
features/
  add-to-cart/
    ui/
      AddToCartButton.tsx
    model/
      useAddToCart.ts     — hook/store wiring the action to entities/cart
    api/
      addToCart.ts        — if a backend call is implied by AC
    index.ts
```

Map the story's **acceptance criteria directly into scaffold comments/stubs** so nothing gets lost between backlog and code — e.g. a `// TODO: AC — Given cart is full, Then show error` comment at the point in the stub where that logic belongs, rather than leaving it as an orphaned requirement. If a story splits across multiple features when its AC implies genuinely separate user actions (this mirrors the Step 4 splitting logic in `backlog-grooming`), split it here too.

If a story has no meaningful separate action (it's just "view X"), it usually collapses into the `entities` layer's `ui` segment instead of becoming its own feature — don't force a feature to exist for pure display.

### Step 4 — Extract pages (from the screen inventory)

Each screen from `figma-design-generator`'s inventory becomes one page slice. Pages should stay thin — they compose widgets/features/entities, not implement logic themselves:

```
pages/
  login/
    ui/
      LoginPage.tsx     — composes features/auth-by-email + entities/user display
    index.ts
```

If no design exists yet, derive pages directly from the backlog's epics/stories the same way Step 2 of `figma-design-generator` would — one page per distinct user-facing view, not one per story.

### Step 5 — Extract widgets (only where genuinely composite)

A widget is warranted when a chunk of UI combines multiple entities/features and reappears across pages — e.g. a header showing the current user (entity) plus a cart icon with item count (entity) plus a logout action (feature). If something only appears on one page, it probably belongs directly in that page, not in `widgets` — don't create a widgets slice just to have one.

### Step 6 — Build the shared layer

Anything business-agnostic goes here, matching the shared components already built as OpenPencil components in `figma-design-generator` Step 4 (buttons, inputs, cards with no domain meaning):

```
shared/
  ui/          — Button, Input, Card, Modal — design-system kit, no business logic
  api/         — base fetch client, error handling
  lib/         — generic utils (formatDate, debounce, etc.)
  config/      — env vars, constants
```

If a design file exists, walk its component list and generate one `shared/ui` component per design-system component (matching name and, where extractable, matching props to the variants seen in the design), rather than inventing a different naming scheme.

### Step 7 — Wire the app layer

```
app/
  providers/     — theme, router, global state providers
  styles/        — global CSS/Tailwind config
  App.tsx        — composes pages via the router
  main.tsx        — entry point
```

Routes map 1:1 to the `pages` slices from Step 4.

### Step 8 — Generate Public API files and check import direction

For **every** slice created above, generate an `index.ts` that re-exports only what other layers are meant to consume — nothing else should be imported from outside the slice. Then do a pass checking each generated import statement against the layer table's ordering (`app > pages > widgets > features > entities > shared`). Flag (don't silently fix) any same-layer cross-slice import that isn't going through `shared` — that's the one mistake that silently defeats the whole point of FSD, and it's worth calling out explicitly rather than quietly resolving.

### Step 9 — Deliver with traceability

Close with a mapping table linking backlog/design back to the generated structure, same discipline as the two upstream skills:

```markdown
| Backlog item | Design screen/component | FSD path |
|---|---|---|
| Epic: Auth → "As a user, I want to log in..." | Login — Default/Error/Loading | pages/login, features/auth-by-email, entities/user |
| Shared "Button/Primary" component | — | shared/ui/Button |
```

Also note anything that had **no upstream source** (a page you had to infer without a design, or a store you added because a feature needed state but nothing in the backlog specified persistence) — same "Open Questions/Assumptions" discipline as `backlog-grooming`, so nothing generated looks more authoritative than it is.

## Things to avoid

- Don't create a slice for every noun/verb mechanically — collapse pure-display stories into entities (Step 3), and don't force a widgets layer into existence (Step 5) if nothing is actually composite.
- Don't let two slices on the same layer import each other directly — route through `shared` or restructure, and flag it if you catch it rather than silently patching.
- Don't fully implement business logic — this skill scaffolds structure, stubs, and wiring with AC-derived TODOs; it does not replace actual development.
- Don't invent a different styling/state approach mid-project if one is already established in an existing codebase — detect and match it (Prerequisites section).
- Don't skip the Public API (`index.ts`) step even for small slices — a slice without one isn't actually FSD, it's just a folder with the same name.
