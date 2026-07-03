# Skill: Figma-to-Code / UI Implementation

## Metadata
- **Skill Name:** `figma-to-code-ui-implementation`
- **Category:** Development / Frontend
- **Version:** 1.0.0
- **Prerequisites:** Figma access, project framework setup (React/Vue/Angular), CSS preprocessor or Tailwind, linter/formatter configured

---

## Purpose
Convert Figma designs into production-ready frontend code with pixel-perfect accuracy, responsive layout, design token alignment, and accessibility compliance.

---

## Inputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Figma design file | URL or exported assets | Yes | Link to design or exported frames |
| Design tokens | JSON | Yes | Colors, typography, spacing, breakpoints |
| Target framework | String | Yes | React, Vue, Angular, or Vanilla JS |
| Breakpoints | Array | No | Custom breakpoints (default: 320, 768, 1024, 1440) |
| Component list | Array | No | Prioritized list of components to implement |

---

## Outputs
| Output | Description |
|--------|-------------|
| Component source files | JSX/TSX/Vue files |
| Stylesheets | CSS/SCSS/Tailwind configuration |
| Optimized assets | Images, icons, fonts |
| Documentation | Component usage, props, styling overrides |
| Storybook/Styleguide updates | If applicable |

---

## Workflow Steps

### Phase 1: Preparation
1. **Extract design tokens** – Export colors, typography, spacing, and breakpoints from Figma (manual or via Tokens Studio plugin).
2. **Analyze layout structure** – Identify layers, frames, auto-layouts, constraints, and nesting hierarchy.
3. **Map components** – Break UI into reusable components (atoms → molecules → organisms → templates).
4. **Set up project scaffolding** – Create component folders, install dependencies, configure build tools.

### Phase 2: Implementation
5. **Write semantic HTML** – Use appropriate tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`).
6. **Apply styles** – Implement using extracted design tokens; ensure mobile-first responsive design.
7. **Implement interactivity** – Add JavaScript/TypeScript for dynamic behaviors (hover, click, form validation, modals, carousels).
8. **Integrate assets** – Export and optimize images (WebP/AVIF), icons (SVG), and fonts (WOFF2).

### Phase 3: Quality Assurance
9. **Ensure accessibility** – Add ARIA labels, focus management, keyboard navigation, and proper color contrast (WCAG 2.1 AA).
10. **Cross-browser testing** – Verify on Chrome, Firefox, Safari, Edge (desktop + mobile).
11. **Responsive validation** – Test at all breakpoints against Figma frames.
12. **Visual regression check** – Compare rendered output against Figma design using Percy, Chromatic, or manual diff tools.

### Phase 4: Handoff
13. **Code review** – Submit for peer review; address linting, performance, and maintainability feedback.
14. **Update documentation** – Record component usage, props, and styling overrides in project docs.
15. **Commit and push** – Commit with clear message; push to feature branch for integration.

---

## Quality Gates
- [ ] Pixel-perfect match to Figma designs (within 2px tolerance)
- [ ] Fully responsive across all breakpoints
- [ ] Lighthouse performance score ≥ 90
- [ ] WCAG 2.1 AA accessibility compliance
- [ ] No console errors or warnings
- [ ] Unit tests cover critical component logic
- [ ] Code passes linting and formatting checks
- [ ] Design tokens consistently applied (no hardcoded values)

---

## Tools & Plugins
| Tool | Purpose |
|------|---------|
| Tokens Studio | Export design tokens from Figma |
| Figma API | Automated asset extraction |
| Percy/Chromatic | Visual regression testing |
| Storybook | Component documentation and testing |
| SVGO | SVG optimization |
| ImageMagick / Sharp | Image optimization |
| Lighthouse | Performance auditing |
| axe / Wave | Accessibility testing |

---

## Common Pitfalls & Mitigations
| Pitfall | Mitigation |
|---------|------------|
| Hardcoded pixel values | Use design tokens and CSS variables |
| Missing responsive behavior | Test on real devices early |
| Unoptimized images | Automate compression in build pipeline |
| Accessibility oversights | Run axe checks after each component |
| Framework-specific mismatches | Validate props/state patterns per framework |

---

## Definition of Done
- [ ] All components from design implemented
- [ ] All quality gates passed
- [ ] PR approved by at least one reviewer
- [ ] Deployed to staging environment for UAT
- [ ] Documentation updated
