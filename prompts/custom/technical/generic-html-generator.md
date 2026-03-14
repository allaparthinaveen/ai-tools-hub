**🚀 MASTER PROMPT FOR AI UI GENERATION – GENERIC HTML + TAILWIND DASHBOARD / TOOL**  

---

You are a **Senior Frontend Architect** and **FinTech / SaaS UI/UX Designer** with 15+ years building professional dashboards and tools (TradingView, Zerodha Kite, Bloomberg, Notion, Linear, Vercel). You specialize in pixel-perfect, high-performance, single-file HTML + Tailwind interfaces that feel premium and institutional-grade.

**OBJECTIVE**  
Create a **complete, production-ready, single-file HTML dashboard/tool** for **[INSERT PURPOSE OF THE TOOL HERE – e.g., “Multi-Strategy Automated Trading Bot Platform” or “Real-time Crypto Portfolio Tracker” or “AI SaaS Analytics Dashboard”]**. The page must look instantly professional, fully responsive (mobile-first), and ready to connect to any backend (Flask/FastAPI/Node) later. Use **static mock data only** — no real API calls. Support **both Light and Dark themes** with a working toggle switch (default = Dark).

**HTML STRUCTURE (exactly follow these industry-best standards)**  
- **Fixed Top Header** (sticky, shadow-sm, contains logo, title, user info, theme toggle, notifications, quick actions)  
- **Optional Collapsible Sidebar** (left, with navigation links – make it toggleable on mobile with hamburger)  
- **Main Content Area** (flex-1, scrollable, with padding – this is where all dynamic sections live)  
- **Fixed Bottom Footer** (minimal, shows status like “Last updated: 2s ago”, connection indicator, copyright)  
- Full `<html>`, `<head>`, `<body>` with proper semantic tags, meta viewport, and Tailwind CDN.  
- Dark theme defaults: `bg-zinc-950 text-zinc-100` accents `emerald-400` (profit/success) / `rose-400` (loss/error).  
- Light theme: `bg-white text-zinc-900` accents `emerald-500` / `rose-500` (auto-switch via Tailwind dark: prefix + JS toggle that adds `dark` class to `<html>`).  
- Glassmorphism cards (backdrop-blur, subtle borders), smooth hover scales, micro-animations (Tailwind + minimal vanilla JS).

**SPECIFIC UI REQUIREMENTS (REPLACE THIS ENTIRE SECTION WITH YOUR DETAILS)**  
[INSERT YOUR EXACT REQUIREMENT DETAILS HERE]  
Example format you can paste:  
“Section 1: AVAILABLE STRATEGIES – hero title, responsive grid of cards (name, description, metrics, Deploy button).  
Section 2: DEPLOYED STRATEGIES – accordion/tabs with expandable cards showing status, metrics table, live positions sub-table, recent transactions mini-table, action buttons.  
Include realistic mock data for Indian markets (NIFTY, BANKNIFTY etc.) or any domain you choose. Add filter bar, search, modals for details/edit.”

**ADDITIONAL PROFESSIONAL FEATURES (must include – non-negotiable)**  
- Theme toggle in header (sun/moon icon) that instantly switches Light ↔ Dark and persists via localStorage.  
- Smooth hover effects, glassmorphism cards (bg-white/10 dark:bg-zinc-900/50 backdrop-blur), subtle Tailwind transitions and scale animations.  
- Fake live updating numbers (JS interval that randomly increments P&L/metrics every 5-10 seconds for demo realism).  
- Responsive design: Tailwind breakpoints (mobile-first) – sidebar collapses to bottom nav or drawer on <768px.  
- Modal system (2-3 modals with backdrop): detail view + edit form + confirmation.  
- Accessible: ARIA labels, keyboard navigation, focus states, semantic HTML.  
- Lucide icons (via CDN or inline SVG) for professional look.  
- Dark theme first with the exact colors: bg-zinc-950, text-zinc-100, emerald-400/rose-400 accents. Light theme perfectly matched.  
- Realistic mock data relevant to the purpose (Indian stocks/indices when trading-related).

**TECHNICAL REQUIREMENTS**  
- **Single HTML file only** (everything self-contained).  
- Tailwind CSS via official CDN: `<script src="https://cdn.tailwindcss.com"></script>`.  
- Initialize Tailwind in `<head>` with custom colors and darkMode: 'class'.  
- Minimal vanilla JavaScript only (no frameworks): theme toggle, sidebar collapse, modals, fake live updater, accordion.  
- Clean, heavily commented code with clear sections (HTML → Tailwind script → JS at bottom).  
- Font: system-ui / Inter fallback.  
- Performance: <100 KB gzipped, instant load, no external dependencies except Tailwind CDN.  
- Industry best practices: semantic HTML5, no inline styles where avoidable, mobile-optimized, WCAG AA contrast.

**DELIVERABLES YOU MUST OUTPUT**  
Output the **complete single HTML file** inside ONE markdown code block titled `your-tool-name.html`.  
At the very top of the file include this comment block:  
```html
<!-- [TOOL NAME] DASHBOARD v1.0 – Single-file HTML + Tailwind | Light + Dark Themes  -->