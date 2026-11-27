# Accessibility, Keyboard & React/UI Quality Checklist

Reference guide for `frontend-component` covering interactive ARIA keyboard contracts, responsive rules, and React rendering pitfalls.

## 1. Keyboard & ARIA Pattern Contracts

| Component | Required Semantics & ARIA | Mandatory Keyboard Support |
|---|---|---|
| **Modal / Dialog** | `role="dialog"` (or native `<dialog>`), `aria-modal="true"`, `aria-labelledby`, `aria-describedby` | `Esc` closes (unless blocked by active submission), Tab cycles inside dialog (focus trap), focus restores to trigger button on close |
| **Dropdown / Menu** | Trigger `aria-expanded`, `aria-controls`; menu `role="menu"`, items `role="menuitem"` | `ArrowDown`/`ArrowUp` move items, `Enter`/`Space` activate, `Esc` closes and returns focus |
| **Combobox / Autocomplete** | Input `role="combobox"`, `aria-expanded`, `aria-activedescendant`, list `role="listbox"` | `ArrowDown`/`ArrowUp` highlight options, `Enter` selects, `Esc` clears/closes |
| **Tabs** | `role="tablist"`, `role="tab"` (`aria-selected`), `role="tabpanel"` (`aria-labelledby`) | `ArrowLeft`/`ArrowRight` switch tabs; `Tab` enters active panel |
| **Form Errors & Toasts** | Field `aria-invalid="true"` + `aria-describedby` pointing to error ID; live alert `role="alert"` / `aria-live="polite"` | Error summary or first invalid field focused on failed submit |

## 2. Visual, Motion & Responsive Hygiene
- Contrast >= `4.5:1` for normal text, >= `3:1` for large text and UI icons/borders.
- Support `prefers-reduced-motion: reduce` (`motion-reduce:transition-none` in Tailwind) on all non-essential transitions/animations.
- Maintain `>= 44x44px` hit target on mobile touch buttons/icon buttons.
- Test horizontally down to `360px` viewport (table wrappers `overflow-x-auto`, long user strings `break-words` or `truncate`).

## 3. React / Modern Frontend State Pitfalls
- **No Derived-State `useEffect`:** Compute derived values (`filteredItems`, `isValid`, `fullName`) directly during render (or `useMemo` only if genuinely expensive), not via `useState` + `useEffect` sync.
- **Prevent Prop Explosion:** Prefer compound components (`<Card><Card.Header /><Card.Body /></Card>`) or composition slots over 12 boolean layout flags (`hasFooter`, `noPadding`, `isCompact`).
- **Prevent Double Submit & Stale Closures:** Track pending state (`disabled={isSubmitting}` + `aria-busy={isSubmitting}`), clean up `AbortController` on unmount/filter changes so slow earlier responses never overwrite newer queries.
