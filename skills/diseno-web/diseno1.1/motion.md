# Motion (React animation library) — implementation reference

Motion (`github.com/motiondivision/motion`) is published under two npm names for the same
library: `framer-motion` (the original name, still maintained) and `motion` (the newer
framework-agnostic entry point, with `motion/react` as the React-specific import). If a
project already depends on `framer-motion`, keep using that import path — don't mix both
packages in one project. Check `package.json` before adding anything.

```bash
# check what's already installed before adding a dependency
grep -E '"(motion|framer-motion)"' package.json
```

## Core mental model

Every animatable value goes through a **transition** — either a `tween` (duration + easing
curve) or a `spring` (physical stiffness/damping/mass). Prefer springs for anything that
responds to user interaction (press, drag, hover) — they interrupt and reverse naturally
mid-motion, which a duration-based tween can't do without looking broken. Reserve tweens for
non-interactive entrances (page load, scroll reveal) where a fixed duration reads as
intentional pacing rather than physics.

```tsx
// interactive (press/hover/drag) -> spring
transition={{ type: "spring", stiffness: 400, damping: 20 }}

// passive entrance (mount, scroll-into-view) -> tween
transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }} // "ease-out-expo"-ish
```

Common spring presets, by feel:
- **Snappy UI feedback** (buttons, toggles): `stiffness: 400, damping: 20`
- **Cards / panels entering**: `stiffness: 260-300, damping: 24-28`
- **Large layout shifts** (modals, drawers): `stiffness: 300-320, damping: 26`
- Higher `damping` relative to `stiffness` = less bounce. Don't go below damping ~18 for UI
  chrome — visible overshoot on a button reads as buggy, not delightful.

## Pattern library

### 1. Press/hover feedback (buttons, cards, nav items)

```tsx
<motion.button
  whileHover={{ scale: 1.03 }}
  whileTap={{ scale: 0.96 }}
  transition={{ type: "spring", stiffness: 400, damping: 20 }}
>
  Confirm
</motion.button>
```
Scale range 0.95–1.05 per the standard UI motion guideline — bigger reads as janky, smaller
is imperceptible. Never scale a fixed-width sidebar/nav item enough to shift layout; wrap the
scaling element so surrounding content doesn't reflow.

### 2. Mount/unmount (exit animations) — `AnimatePresence`

Anything that conditionally renders (`{show && <X/>}`) needs `AnimatePresence` to animate
*out* — without it, React just unmounts instantly and `exit` never runs.

```tsx
<AnimatePresence>
  {show && (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration: 0.15 }}
    />
  )}
</AnimatePresence>
```
Rule of thumb: exit duration should be ~60–70% of enter duration — leaving feels faster than
arriving, which reads as responsive rather than sluggish.

### 3. Modal / dialog open-close

Animate from the trigger source when possible (scale+fade reads as "this grew out of what I
clicked"); a bare fade for the scrim, scale+fade for the panel:

```tsx
<AnimatePresence>
  {open && (
    <motion.div /* scrim */
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      transition={{ duration: 0.15 }}
      className="fixed inset-0 bg-black/50"
    >
      <motion.div /* panel */
        initial={{ opacity: 0, scale: 0.94, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96, y: 8 }}
        transition={{ type: "spring", stiffness: 320, damping: 26 }}
      >
        {children}
      </motion.div>
    </motion.div>
  )}
</AnimatePresence>
```

### 4. List / grid stagger

Use `variants` with a parent `staggerChildren` rather than manual per-item delays — it
composes correctly with `AnimatePresence` and reduced-motion checks.

```tsx
const container = { hidden: {}, show: { transition: { staggerChildren: 0.05 } } };
const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 280, damping: 26 } },
};

<motion.div variants={container} initial="hidden" animate="show">
  {items.map((it) => (
    <motion.div key={it.id} variants={item}>{it.label}</motion.div>
  ))}
</motion.div>
```
Stagger 30–50ms per item. Past ~8-10 visible items, cap the stagger delay (or drop it) —
a long cascading reveal on a 50-row table reads as slow, not polished.

### 5. Shared-element / layout transitions — `layout` and `layoutId`

This is Motion's signature feature and the fastest way to make an app feel "native": give two
elements across different render trees the same `layoutId` and Motion automatically
tweens position/size between them (a sliding active-tab indicator, a card that expands into
a detail view, a moved list item).

```tsx
// sliding active-nav-item pill, no manual position math
{links.map((link) => (
  <Link key={link.href} href={link.href} className="relative px-3 py-2">
    {isActive(link) && (
      <motion.span
        layoutId="nav-active-pill"
        className="absolute inset-0 rounded-full bg-primary/10"
        transition={{ type: "spring", stiffness: 380, damping: 30 }}
      />
    )}
    <span className="relative z-10">{link.label}</span>
  </Link>
))}
```
Add the plain `layout` boolean prop (not `layoutId`) to any element whose size/position
changes for a reason *other* than a matching sibling (e.g., an accordion panel that pushes
content down) — Motion will animate the resulting shift instead of snapping.

### 6. Scroll-linked reveals

For "fade in once visible," use `whileInView` (cheap, no scroll listener):
```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-80px" }}
  transition={{ duration: 0.4 }}
/>
```
For continuous scroll-driven values (parallax, progress bars), use `useScroll` +
`useTransform` — but gate it behind `useReducedMotion()` (see below), since parallax is the
motion type most likely to cause discomfort.

### 7. Drag gestures

```tsx
<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 0 }}
  dragElastic={0.2}
  onDragEnd={(_, info) => { if (info.offset.x < -100) dismiss(); }}
/>
```
Always set `dragConstraints` (even `{left:0,right:0}` with elastic overshoot) — unconstrained
drag on desktop web reads as broken, not free-form.

### 8. Icon-swap / crossfade (e.g. theme toggle sun↔moon)

```tsx
<AnimatePresence mode="wait" initial={false}>
  <motion.span
    key={theme} // re-mounts on change, driving enter/exit
    initial={{ opacity: 0, rotate: -90, scale: 0.6 }}
    animate={{ opacity: 1, rotate: 0, scale: 1 }}
    exit={{ opacity: 0, rotate: 90, scale: 0.6 }}
    transition={{ type: "spring", stiffness: 300, damping: 20 }}
  >
    {theme === "dark" ? <Sun/> : <Moon/>}
  </motion.span>
</AnimatePresence>
```

## Accessibility — always gate on reduced motion

```tsx
import { useReducedMotion } from "framer-motion"; // or "motion/react"
const reduce = useReducedMotion();
<motion.div
  variants={reduce ? undefined : container}
  initial={reduce ? undefined : "hidden"}
  animate={reduce ? undefined : "show"}
/>
```
`useReducedMotion()` reads the OS-level `prefers-reduced-motion` setting reactively — prefer
it over a raw CSS media query when the animation is JS-driven (variants, layout, drag),
since it lets you skip building the variant object entirely rather than just zeroing a
duration. Never disable the resulting state change itself, only the motion getting there.

## Performance

- Animate only `transform` (`x`, `y`, `scale`, `rotate`) and `opacity`. Animating `width`,
  `height`, `top`, `left` triggers layout recalculation every frame — use the `layout` prop
  instead, which Motion internally converts to a transform under the hood via the FLIP
  technique.
- Don't wrap something in `motion.div` if it never actually animates — it's not free (adds a
  render subscription). Plain `<div>` for static layout.
- For very long lists, animate only the items entering/leaving the viewport, not the whole
  list on every data refresh — key stability (`key={stableId}`, not `key={index}`) matters
  even more once `AnimatePresence`/`layout` are involved, since Motion uses key identity to
  know what's the "same" element across renders.

## Anti-patterns to avoid

- Linear easing on UI transitions (`ease: "linear"`) — reads as robotic; use `ease-out` for
  entrances, `ease-in` for exits, or switch to a spring.
- Animating more than 1-2 elements' worth of attention per view at once — simultaneous
  competing motion reads as chaotic, not lively.
- A conditionally-rendered element with `initial`/`animate` but no `AnimatePresence` wrapper —
  the `exit` prop silently does nothing without it.
- Modals/sheets that just snap open with no `AnimatePresence`/exit motion — the missing close
  animation is one of the most common "this app feels unfinished" tells.
- Blocking interaction during an animation (e.g., disabling a button until its own animation
  finishes) — animations should be interruptible; the user's next input takes priority.

---

## API verificada contra el repo clonado (motion v13.4.6, commit fba53e4, 2026-09-29)

Fuente: `~/.claude/skills-src/motion/packages/framer-motion/src/index.ts`. Si el proyecto tiene otra versión instalada, revisa `node_modules/motion/package.json` o `node_modules/framer-motion/package.json` antes de usar algo de esta lista.

- Componentes: `motion`, `m` (con `LazyMotion` + `domAnimation`/`domMax`/`domMin` para bajar peso), `AnimatePresence` (`mode="wait" | "popLayout" | "sync"`), `LayoutGroup`, `MotionConfig` (usa `reducedMotion="user"`), `Reorder`.
- Hooks de valores: `useMotionValue`, `useTransform`, `useSpring`, `useFollowValue`, `useMotionTemplate`, `useVelocity`, `useTime`, `useScroll`, `useMotionValueEvent`, `useWillChange`.
- Hooks de control: `useAnimate`, `useAnimateMini`, `useInView`, `usePageInView`, `useReducedMotion`, `useAnimationFrame`, `useCycle`, `usePresence`/`useIsPresent`, `usePresenceData`.
- Utilidades: `animate`, `stagger`, `delay`, `arc` (trayectorias en arco).
- Obsoletos (no usar en código nuevo): `useViewportScroll`, `useElementScroll`, `AnimateSharedLayout`, `useDeprecatedAnimatedState`, `useDeprecatedInvertedScale`.
- Import: en proyectos nuevos `import { motion } from "motion/react"`; si el proyecto ya tiene `framer-motion`, sigue con ese import y no mezcles los dos.
- Next.js App Router: los componentes con `motion.*` llevan `"use client"`; para no romper el SSR usa `motion/react-client` (`import * as motion from "motion/react-client"`) en componentes servidor.
