---
name: frontend-component
description: Build clean, accessible, responsive, maintainable UI components that strictly follow the project's existing design system and avoid generic AI visual slop. Covers semantic HTML, keyboard navigation, ARIA states, loading/empty/error UI, and clean state boundaries. Use when creating or refining React/Vue/Svelte/HTML components ("tạo component", "UI component", "accessible form", "frontend").
license: MIT
compatibility: opencode
metadata:
  category: web-backend
  audience: developers
  version: "1.0.0"
---

# Frontend Component — Accessible, Intentional UI Engineering

Craft production-grade UI components that feel native to the project's design system, behave predictably across states, and work for every user including keyboard and screen-reader users.

## When to Use

- Building new UI components, forms, tables, modals, or interactive widgets (React, Next.js, Vue, Svelte, Tailwind, CSS Modules).
- Fixing layout fragility, missing accessibility, or messy prop-drilling in UI components.
- **Do NOT use** for backend API contract design (use `api-designer`).

## Step-by-Step Workflow

1. **Inspect the Project's Design System & Component Primitives**:
   - Check `package.json`, Tailwind config / CSS tokens, existing `components/ui/` primitives (Radix/shadcn/Headless UI/etc.), typography, spacing scale, and icon library.
   - Reuse existing tokens and primitives instead of inventing inline magic colors or duplicate button/modal wrappers.
2. **Lock a Compact Design Plan & State Ownership Before JSX**:
   - Before writing markup, pick a concise plan matching the host app: **4-6 semantic color tokens** (no arbitrary hex guessing), typography hierarchy, spacing rhythm, and responsive layout (`360px` mobile → `1440px` desktop).
   - Keep component API minimal, typed, and predictable (compose with compound components / `children` slots instead of 15 boolean flags).
   - Avoid derived-state `useEffect` (compute during render) and protect async actions with `AbortController` + double-submit locks.
3. **Cover Every UI State Explicitly**:
   - Never build only the happy path! Handle:
     - **Loading** (skeleton/spinner with `aria-busy` or disabled duplicate submit)
     - **Empty** (clear message + next action)
     - **Error** (inline, accessible `role="alert"` + retry path)
     - **Long text / overflow** (`truncate` or wrap cleanly on mobile 360px through desktop 1440px)
4. **Bake In Accessibility (A11y) from Line 1**:
   - Use native semantic elements (`<button>`, `<a href>`, `<label htmlFor>`, `<fieldset>`) instead of clickable `<div>`s.
   - Full keyboard support (`Enter`/`Space` activation, `Esc` dismiss, focus trap & focus restoration for dialogs/drawers, visible `focus-visible` ring).
   - Sufficient color contrast (`>= 4.5:1` normal text) and meaningful `aria-label` on icon-only controls.
5. **Apply Intentional Visual Craft (Zero Generic AI Slop)**:
   - Establish crisp visual hierarchy (clear typography scale, purposeful whitespace, restrained accent palette matching the host app).
   - Avoid unrequested purple/neon gradients, excessive drop shadows, decorative pulse animations, or fake metric cards.
6. **Verify Build, Types & Behavior**:
   - Run typecheck, linter, component tests (if configured), and visually/DOM-verify responsive breakpoints & keyboard states (`verification-before-done`).

## Anti-Patterns (Do Not)

- **DO NOT** use `<div onClick={...}>` instead of `<button type="button">` or `<a href>`.
- **DO NOT** slap default purple-indigo gradients, giant rounded glassmorphic boxes, and emoji headers onto every app ("generic AI dashboard look").
- **DO NOT** hardcode arbitrary hex colors (`bg-[#123456]`) when project CSS/Tailwind design tokens exist.
- **DO NOT** forget `disabled` / double-submit protection on async form actions.
- **DO NOT** remove outline focus rings (`outline-none`) without providing a clear `focus-visible:ring-*` replacement.

## Component Checklist

- [ ] Reuses project design tokens & existing UI primitives
- [ ] Handles loading, empty, error, disabled, and long-content overflow states
- [ ] Semantic HTML, labeled inputs, keyboard navigation, and `focus-visible` states
- [ ] Mobile-friendly layout (`360px`+) without horizontal overflow
- [ ] Typecheck & build pass after final edit

## Reference Files

- For interactive ARIA keyboard contracts (Dialog, Combobox, Tabs, Menu), responsive targets, and React state pitfalls, see [a11y-and-ui-checklist.md](references/a11y-and-ui-checklist.md).

## Examples

### Example: Accessible Async Search Combobox / Filter Bar
**Input:**
> "Tạo React + Tailwind component `DeleteAccountDialog` có confirm bằng cách gõ lại email, loading state, báo lỗi nếu API fail."

**Output Highlights:**
> Built `src/components/DeleteAccountDialog.tsx` reusing existing `Dialog`, `Button`, and `Input` tokens:
> - **Accessibility:** Focus moves to confirmation `<input>` on open, `Esc` closes unless `isSubmitting`, error banner uses `role="alert"` and `aria-describedby`, `<label htmlFor>` bound cleanly.
> - **Safety UX:** Confirm button stays disabled until `typedEmail.trim() === userEmail` and locks with `aria-busy="true"` during submission to prevent duplicate requests.
> - **Visual Craft:** Restraint-first destructive confirmation panel using existing `--destructive` semantic token rather than custom flashy gradients.
> - **Verified:** `npm run typecheck` and `npx vitest run tests/components/DeleteAccountDialog.test.tsx` (`5 passed`).
