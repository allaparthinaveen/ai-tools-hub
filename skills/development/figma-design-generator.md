---
name: figma-design-generator
description: >-
  Generates real, editable Figma-compatible (.fig) design files -- screens, components, and design tokens -- from a groomed backlog, user stories, PRD, or feature description, using the open-source OpenPencil CLI/MCP tooling (Figma Plugin API-compatible, no Figma account needed). Use this skill whenever the user wants to turn requirements, user stories, or acceptance criteria into wireframes, mockups, UI screens, a Figma file, or a design system, or asks to "design this feature," "mock this up," "wireframe this flow," or "generate Figma screens from the backlog" -- even if they don't mention OpenPencil by name. Pairs naturally with the backlog-grooming skill -- run that first if the input is still raw requirements.
---

# Backlog-to-Figma Design Generator

Turns structured requirements (ideally the output of the `backlog-grooming` skill: epics → user stories → acceptance criteria) into an actual editable design file — screens, components, and a token-based design system — using **OpenPencil**, an open-source, MIT-licensed, Figma-compatible design editor. OpenPencil reads/writes native `.fig` files and exposes a full Figma Plugin API-compatible scripting environment (`figma.createFrame()`, `figma.createText()`, auto-layout, components, variables, etc.) via its CLI and MCP server — so screens can be generated programmatically rather than described in prose.

## Prerequisites — check before starting

Run this before doing anything else:

```bash
openpencil --version
```

- **If found**: proceed.
- **If not found**: install it (requires Node.js or Bun, and network access):
  ```bash
  npm install -g @open-pencil/cli
  # or: bun add -g @open-pencil/cli
  ```
  If installation isn't possible in the current environment (no network access, sandboxed shell), say so explicitly and offer the fallback in "No CLI available" below rather than silently producing nothing.

**Two operating modes** — pick based on context:
- **Headless mode** (default, no app needed): pass a `.fig` file path to every command. Best for one-shot batch generation of a full screen set from a backlog. This is the default for this skill.
- **App/live mode**: if the user has the OpenPencil desktop app open, omit the file path — commands connect via RPC to the live document (`http://127.0.0.1:7600`). Useful when the user wants to watch screens appear and iterate visually. Ask which they want if it's unclear from context; default to headless if they haven't opened the app.

## Workflow

### Step 1 — Get or build the requirements

If the user hasn't already given you a groomed backlog, and raw material (notes, a PRD, a feature description) is available instead, run the `backlog-grooming` skill first to get Epics → Stories → Acceptance Criteria. Don't try to design directly from an unstructured paragraph — the AC are what tell you what states and elements a screen actually needs.

### Step 2 — Derive the screen inventory and IA

Read through the backlog and build a table before writing any code:

| Screen | Epic / Stories it serves | Key elements implied by AC | States needed |
|---|---|---|---|
| Login | Auth epic, "As a user I want to log in..." | email field, password field, submit button, error text | default, error (bad credentials), loading |
| ... | | | |

Rules for deriving this:
- **One screen per distinct user-facing view**, not one screen per story — several stories often share a screen (e.g. "add item to cart" and "remove item from cart" both live on the Cart screen).
- **States come from acceptance criteria**, not invention. If a story's AC says "Given invalid input, Then show an error message," that's a required state/frame. If AC never mentions an empty or error state, don't invent one — note it as a gap instead (this mirrors the "Open Questions" discipline from backlog-grooming).
- **Identify shared components** across screens (buttons, nav bar, form fields, cards) before laying out individual screens — build these once, reuse everywhere, rather than rebuilding per-screen.
- Group screens by epic using OpenPencil **Sections**, so the resulting file reads the same way the backlog does.

Show this table to the user before generating anything if the backlog is large (>6 screens) or if screen boundaries are genuinely ambiguous — getting IA wrong is expensive to unwind after 20 frames exist. Skip this checkpoint for small, unambiguous requests.

### Step 3 — Establish design foundations first

Before any screen, create the token layer so every screen pulls from the same system rather than hardcoded values. Use OpenPencil **Variables** (color, float, string types, with Light/Dark modes if relevant):

```bash
openpencil eval design.fig -w -c '
  const collection = figma.variables.createVariableCollection("Design Tokens");
  const lightMode = collection.modes[0];

  const colorVars = {
    "color/primary":    "#4F46E5",
    "color/bg":         "#FFFFFF",
    "color/text":       "#111827",
    "color/text-muted": "#6B7280",
    "color/error":      "#DC2626",
    "color/border":     "#E5E7EB",
  };
  for (const [name, hex] of Object.entries(colorVars)) {
    const v = figma.variables.createVariable(name, collection, "COLOR");
    v.setValueForMode(lightMode.modeId, hexToRgb(hex));
  }

  const spaceVars = { "space/xs": 4, "space/sm": 8, "space/md": 16, "space/lg": 24, "space/xl": 32 };
  for (const [name, val] of Object.entries(spaceVars)) {
    const v = figma.variables.createVariable(name, collection, "FLOAT");
    v.setValueForMode(lightMode.modeId, val);
  }

  function hexToRgb(hex) {
    const n = parseInt(hex.replace("#",""), 16);
    return { r: ((n>>16)&255)/255, g: ((n>>8)&255)/255, b: (n&255)/255 };
  }
'
```

For typography and spacing scale decisions, and for general visual taste (don't default to generic-looking UI), consult the `frontend-design` skill — it covers the same token/hierarchy thinking, just for code instead of a design file. Reuse those principles here: a deliberate type scale, real hierarchy, and restraint on color count.

### Step 4 — Build shared components once

For every element that recurs across screens (buttons in multiple states, form fields, nav bars, cards), create it as a real OpenPencil **Component**, not a copy-pasted frame — this is what makes the output actually useful to a designer picking it up afterward, since instances stay live-linked to the source.

```bash
openpencil eval design.fig -w -c '
  const btn = figma.createFrame();
  btn.name = "Button/Primary";
  btn.layoutMode = "HORIZONTAL";
  btn.primaryAxisAlignItems = "CENTER";
  btn.counterAxisAlignItems = "CENTER";
  btn.paddingLeft = btn.paddingRight = 16;
  btn.paddingTop = btn.paddingBottom = 10;
  btn.cornerRadius = 8;
  btn.fills = [{ type: "SOLID", color: { r: 0.31, g: 0.27, b: 0.90 } }]; // bind to color/primary variable in practice

  const label = figma.createText();
  label.characters = "Button";
  label.fontSize = 14;
  label.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
  btn.appendChild(label);

  const component = figma.createComponentFromNode(btn); // or figma.createComponent() + append, depending on API version
  component.name = "Button/Primary";
'
```

If a component needs variants (e.g. Button: Primary/Secondary/Disabled, or an input field's Default/Focus/Error), group them into a **Component Set** (`⇧⌘K` equivalent via API) rather than creating unrelated components with similar names.

### Step 5 — Generate each screen

For each row in the Step 2 table, build a top-level Frame (standard sizes: 1440×1024 for desktop web, 375×812 for mobile — ask if unclear) using auto-layout so it holds together if content changes:

```bash
openpencil eval design.fig -w -c '
  const screen = figma.createFrame();
  screen.name = "Login — Default";
  screen.resize(375, 812);
  screen.layoutMode = "VERTICAL";
  screen.primaryAxisAlignItems = "CENTER";
  screen.paddingTop = 64;
  screen.itemSpacing = 16;
  screen.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];

  // ...append instances of shared components (email field, password field, Button/Primary) as children...
'
```

Generate one frame per **state** identified in Step 2 (e.g. "Login — Default", "Login — Error", "Login — Loading"), placed adjacently on the canvas so they read as a set. Name frames `Screen — State` consistently; this naming is what makes the file navigable afterward and is also what you'll use to verify traceability in Step 7.

Where the OpenPencil **AI chat / MCP `render` tool** is available and the user is in app/live mode, it's often faster to describe the frame as design-JSX and let the tool build it rather than hand-writing every `createX()` call:

```jsx
<Frame name="Login — Default" width={375} height={812} direction="vertical" gap={16} padding={64}>
  <Text size={24} weight="bold">Log in</Text>
  <Instance component="Input/Text" props={{ label: "Email" }} />
  <Instance component="Input/Password" props={{ label: "Password" }} />
  <Instance component="Button/Primary" props={{ label: "Log in" }} />
</Frame>
```

Use whichever generation path (raw `eval` calls or JSX `render`) is actually available in the current environment — check for the MCP server / render tool before assuming it's there, and fall back to `eval` + `createX()` calls otherwise.

### Step 6 — Assemble into pages and sections

Group generated screens into **Sections** per epic so the file mirrors the backlog structure, and order screens left-to-right in the sequence a user would move through the flow (this becomes a rough user-flow map even before real prototyping/connectors are added).

### Step 7 — Verify and export

After generating, check the work rather than assuming it rendered correctly:

```bash
openpencil tree design.fig                 # confirm structure matches the screen inventory
openpencil export design.fig -f png -o previews/   # render every frame for visual review
```

Look at the PNG previews yourself (via the `view` tool) before handing off — catch obviously broken layouts (overlapping elements, zero-size frames, missing fills) rather than passing them straight through. If `openpencil analyze colors design.fig` or `openpencil analyze spacing design.fig` are available, run them as a quick consistency check on the token usage from Step 3.

### Step 8 — Deliver with traceability

Produce a short mapping table alongside the `.fig` file so the design and the backlog stay linked:

```markdown
| Backlog item | Screen(s) / Frame(s) | Notes |
|---|---|---|
| Epic: Auth → "As a user, I want to log in..." | Login — Default, Login — Error, Login — Loading | Error copy is placeholder — AC didn't specify exact message |
```

Save the `.fig` file and any PNG previews to the outputs directory and present them to the user. Mention that the file opens directly in OpenPencil (free) or in Figma itself, since `.fig` is Figma's native format.

## No CLI available

If OpenPencil can't be installed in the current environment (no network, restricted sandbox), don't fabricate a fake design file. Instead:
1. Say plainly that the CLI isn't available here.
2. Still do Steps 1–2 (requirements → screen inventory/IA table) since that's pure analysis — it's useful on its own and is exactly what someone would hand a designer.
3. Offer to produce an HTML/CSS mockup instead (via the `frontend-design` skill) as a visual stand-in, or provide the OpenPencil `eval` scripts from Steps 3–6 as a ready-to-run script for the user to execute in their own environment.

## Things to avoid

- Don't invent screens, elements, or states that nothing in the backlog implies — every frame should trace back to a story or AC (Step 8's table should have no orphans in either direction).
- Don't hardcode colors/spacing directly on every element once tokens exist (Step 3) — bind to variables so the file stays a real design system, not a one-off mockup.
- Don't rebuild the same button/field/card by hand on every screen — components (Step 4) exist so instances stay in sync.
- Don't skip Step 7 — an unverified batch of `eval` calls can silently produce a zero-size or overlapping frame, and that's worse to hand off than no file at all.
- Don't default to generic, templated-looking layouts — apply real visual hierarchy and a deliberate type/color scale (see `frontend-design` skill) rather than evenly-spaced boxes with default styling.
