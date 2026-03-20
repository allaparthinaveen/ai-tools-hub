You are a Senior Full‑Stack Engineer and Developer Tools UX Designer.
I have a Confluence page that documents all our AWS Elasticsearch / OpenSearch APIs in a structured table (endpoint, method, headers, auth, request/response examples, folder/app grouping, etc.).

I also have the Confluence MCP tool configured in Claude Code, so you can programmatically read that page.

Your goal:
Build a single-page, Insomnia‑style HTML+JS utility that:

Loads API metadata from the specified Confluence page using MCP.

Displays the APIs in a sidebar (organized by app/folder, similar to Insomnia collections).

Lets me select an API, view/edit the request in the main panel (URL, method, headers, body, query params).

Execute that API against the configured base URL(s) and show the JSON response, status code, and timing.

Optionally run multiple APIs in sequence (batch) based on:

Folder / app name

Manual multi‑select of APIs

This is not a production product, but the UX should feel close to Insomnia/Postman for daily use.

1. Inputs and assumptions
I will provide:

The Confluence page URL or ID that contains the API table.

The column headers used (e.g., App, Folder, API Name, Method, Path, Base URL, Headers, Auth Type, Request Example, Notes).

Use MCP to:

Fetch the Confluence page contents.

Parse the table rows into a typed internal JSON structure representing APIs.

Assume:

We’ll run the HTML file locally in a browser.

For API calls, we will:

Either call the real AWS ES endpoints directly (CORS-permitting), or

Later plug this HTML into a simple local proxy backend.

For now, you can:

Implement fetch calls directly from the browser,

And clearly isolate the place where we’d instead call a local Node/Python proxy.

2. Data model (from Confluence → internal JSON)
Define a JS data model like:

ts
type ApiDefinition = {
  id: string;              // unique ID
  app: string;             // application name
  folder: string;          // logical grouping / feature
  name: string;            // human title
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH' | string;
  baseUrl: string;         // e.g., https://my-es-domain.amazonaws.com
  path: string;            // e.g., /_search or /index/_doc
  fullUrl?: string;        // computed
  defaultHeaders: Record<string, string>;
  authType: 'none' | 'basic' | 'bearer' | 'aws-sigv4' | string;
  defaultQuery?: Record<string, string>;
  defaultBody?: string;    // JSON string or DSL from Confluence example
  notes?: string;
};
Tasks:

Use the Confluence MCP tool to read and parse the table into an array of ApiDefinition.

Normalize:

Trim strings, handle missing columns, build ids.

Compute fullUrl from baseUrl + path.

Expose this JSON in the HTML via an embedded <script> tag or a small JS module so the UI is data-driven.

3. UI/UX requirements – Insomnia‑style layout
Create a single-file HTML+CSS+JS (no React needed) with a layout similar to Insomnia/Postman:

Top bar

App title, environment selector (e.g., Dev, QA, Prod), and a simple status indicator.

Environment selector changes base URL overrides (e.g., dev vs prod ES domains).

Left sidebar (like Insomnia collection tree):

List of apps/folders:

Top level: app name

Nested: folder / feature

Under each folder, show API names as clickable items.

Provide:

A filter/search box to search by API name, path, or method.

Checkboxes next to APIs to multi‑select for batch execution.

Clicking one API:

Loads its details into the main editor.

Main request editor panel (central column):

Top row:

HTTP method dropdown

URL input box (editable, computed from base + path)

“Send” button and small latency/status display.

Tabs/sections below:

Params (query string key/value editor).

Headers (editable key/value grid prefilled from defaultHeaders).

Body (JSON editor textarea; prefilled from defaultBody from Confluence).

Show the origin (Confluence note) and API description/notes in a side area.

Right response panel:

Show:

Response status code, text, and time taken.

Pretty‑printed JSON body (syntax highlighting).

Raw body tab (optional).

Response headers (optional).

Batch runner controls:

Somewhere (e.g., top of sidebar or a toolbar) add:

“Run selected APIs” button (runs APIs with checked boxes sequentially).

“Run folder” button (run all APIs inside the currently selected folder).

Show minimal run log:

For each API: name, status (success/fail), status code, and duration.

Allow a small delay between calls (e.g., 100–500 ms configurable) to avoid rate limits.

Design should be clean, keyboard-friendly, dark theme by default, inspired by Insomnia/Postman.

4. Execution and environment handling
Implement the core execution logic:

Environment config:

Provide a small, hardcoded environment map in JS:

js
const ENVIRONMENTS = {
  dev: { label: 'Dev', baseUrlOverrides: { /* app or global domain overrides */ } },
  qa:  { label: 'QA',  baseUrlOverrides: {} },
  prod:{ label: 'Prod',baseUrlOverrides: {} },
};
When the environment changes, recompute fullUrl for the selected API(s).

Request building:

Combine:

Base URL (from env override or API default)

Path

Query params from the UI

Headers (merge defaults from Confluence + user edits)

Body (JSON string or text)

Support Content-Type: application/json and simple JSON body input.

Auth:

For now, keep it simple:

Support none, basic, bearer as direct header injection from user inputs in the UI.

For aws-sigv4, just plan it:

Design a placeholder section where we’d later plug in SigV4 signing (using a local proxy or browser library).

Render a small auth editor section based on authType from the API definition.

Batch execution:

Run selected APIs sequentially using fetch.

For each, capture:

start time, end time, duration, status code, error (if any).

Aggregate results into a table/log area.

5. Confluence MCP integration behavior
Since Claude Code has MCP access:

Use the Confluence tool to:

Fetch the exact table on the specified page.

Parse each row into ApiDefinition.

If table structure is ambiguous:

Ask me which columns correspond to which fields.

Generate:

A small helper script or function that can be re-run later to re‑sync the HTML’s API JSON from Confluence when the documentation changes.

This can be a separate script (e.g., Node/Python) that:

Calls Confluence via MCP or API

Writes apis.json consumed by the HTML file.

If you can’t actually call MCP in this environment, at least generate the parsing and transformation code assuming we’ll plug in the raw table JSON.

6. Technical constraints
Frontend:

Pure HTML + CSS + vanilla JS (ES modules allowed).

You may optionally use a light utility like CDN Tailwind or a minimal CSS framework, but no heavy React/Vue.

Single page, ideally in one HTML file plus optional apis.json for data.

Modular JS:

Split logic into:

Data loading / Confluence-derived metadata

UI rendering (sidebar, editor, response panel)

Execution engine (single call + batch).

Make it easy later to:

Swap fetch() with a call to a local proxy backend.

7. Deliverables from you (the AI)
Architecture overview:

Brief description of the UI layout and flow (sidebar → editor → response, batch runner).

How the Confluence table is mapped into ApiDefinition.

Data model & parsing code:

Types / interfaces for API definitions.

Parsing logic (from a generic Confluence table JSON to ApiDefinition[]).

Complete single‑page HTML utility:

All HTML + CSS + JS in one file, using mock ApiDefinition[], with clear placeholder for where the Confluence‑derived data will be injected.

Optional sync script:

Example Node/Python script that, given Confluence API credentials / MCP output, writes apis.json consumed by the HTML page.

Focus on making this tool immediately usable for manual testing and batch‑running ES APIs, while keeping the Confluence table as the single source of truth for API definitions.
