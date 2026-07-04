# Skill: Figma-to-Code / UI Implementation

## Metadata
- **Skill Name:** `figma-to-code-ui-implementation`
- **Category:** Development / Frontend
- **Version:** 2.0.0
- **Prerequisites:** Figma access, modern framework setup, Node.js 20+, TypeScript configured

---

## Purpose
Convert Figma designs into production-ready frontend code using the latest technologies, component-driven architecture, and modern rendering patterns.

---

## Tech Stack (Latest)
| Category | Technologies |
|----------|--------------|
| Framework | Next.js 15 (App Router), React 19, Vue 3.5, SvelteKit 2, or Astro 5 |
| Language | TypeScript 5.7+ (strict mode) |
| Styling | Tailwind CSS 4, Panda CSS, Vanilla Extract, or CSS Modules + PostCSS |
| UI Library | shadcn/ui, Radix UI, or Headless UI (framework-agnostic) |
| State Management | Zustand, Jotai, TanStack Query, or Signals |
| Animations | Framer Motion, GSAP, or View Transitions API |
| Assets | Next/Image, Vite's import.meta.glob, or unplugin-icons |
| Testing | Vitest + Testing Library + Playwright |
| Linting | Biome (instead of ESLint + Prettier) or Oxlint |

---

## Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Figma design file | URL or REST API connection | Yes | Live design or exported frames |
| Design tokens | JSON via Tokens Studio | Yes | Colors (OKLCH), typography (clamp), spacing, breakpoints |
| Framework | String | Yes | Next.js, Vue, SvelteKit, Astro, or Remix |
| Rendering strategy | String | No | SSR, SSG, ISR, or CSR (default: framework default) |

---

## Outputs
| Output | Description |
|--------|-------------|
| Component files | `.tsx`, `.vue`, `.svelte` with TypeScript |
| Styles | Tailwind config, CSS variables, or zero-runtime CSS-in-JS |
| Optimized assets | WebP/AVIF images, inline SVGs, variable fonts |
| Composition layer | Server/Client component boundaries, Suspense fallbacks |
| Documentation | JSDoc, Storybook 8, or Style Dictionary |
| Performance budget | Core Web Vitals targets documented |

---

## Workflow Steps

### Phase 1: Analysis & Token Extraction
1. **Extract design tokens** – Use Tokens Studio or Figma REST API to export:
   - Colors (OKLCH format for wide gamut)
   - Typography (clamp() for fluid typography)
   - Spacing (4px/8px grid or custom scale)
   - Breakpoints (container queries preferred)
2. **Analyze component tree** – Map Figma frames to:
   - React Server Components vs Client Components
   - Vue composables or Svelte stores
   - Layout shifts and loading states
3. **Generate TypeScript types** – Automatically create interfaces for all component props.

### Phase 2: Scaffolding

4. **Initialize framework project** – Use official starters:

   | Framework | Command |
   |-----------|---------|
   | Next.js 15 | `npx create-next-app@latest --typescript --tailwind --app` |
   | Vue 3.5 | `npm create vue@latest` |
   | SvelteKit 2 | `npm create svelte@latest -- --template skeleton --types typescript` |
   | Astro 5 | `npm create astro@latest` |
   | Remix 2 | `npx create-remix@latest` |

5. **Configure build tools** – Set up the following:

   | Tool | Configuration |
   |------|---------------|
   | **Vite 6** (or Turbopack for Next.js) | `vite.config.ts` with aliases, plugins, and optimizations |
   | **TypeScript** | `tsconfig.json` with `strict: true`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax` |
   | **Linting & Formatting** | `biome.json` or `oxlintrc.json` (replace ESLint + Prettier) |
   | **Path Aliases** | `@/*` pointing to `./src/*` or `./app/*` |

   **Example configuration files:**

   <details>
   <summary>📁 tsconfig.json</summary>

   ```json
   {
     "compilerOptions": {
       "strict": true,
       "noUncheckedIndexedAccess": true,
       "verbatimModuleSyntax": true,
       "paths": {
         "@/*": ["./src/*"]
       }
     }
   }
   ```
   </details> <details> <summary>📁 biome.json</summary>
   {
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  }
}

</details> <details> <summary>📁 vite.config.ts</summary>
import { defineConfig } from 'vite';
import path from 'node:path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    target: 'es2022',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
});

Set up environment variables – Create .env.local with:

Variable	Purpose
NEXT_PUBLIC_API_URL	Backend API endpoint
NEXT_PUBLIC_SITE_URL	Production URL
NEXT_PUBLIC_FIGMA_TOKEN	Figma API access token (if using live sync)
Configure CI/CD pipeline – Add GitHub Actions workflow:

<details> <summary>📁 .github/workflows/ci.yml</summary>
yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test
      - run: npm run build
      - run: npm run preview & npx wait-on http://localhost:4173
      - run: npx playwright test
</details>
Install core dependencies – Run:

bash
# Essential
npm install typescript @types/node --save-dev

# Styling (choose one)
npm install tailwindcss@4 postcss autoprefixer
# OR
npm install @pandacss/dev

# UI primitives
npm install @radix-ui/react-slot @radix-ui/react-dialog
# OR for Vue
npm install radix-vue

# State management
npm install zustand
# OR
npm install @tanstack/react-query

# Testing
npm install vitest @vitest/ui @testing-library/react @testing-library/jest-dom --save-dev
npm install @playwright/test --save-dev

# Utilities
npm install clsx tailwind-merge
npm install framer-motion
