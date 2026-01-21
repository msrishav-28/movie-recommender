# VISUAL DNA: The Digital Theater System
**Version:** 1.0.0 (The "Elite" Pivot)
**Target Aesthetic:** Editorial Noir / Cinematic Engineering / Modernist Tech
**Primary Directive:** "Every pixel must feel like a high-budget film artifact."

---

## 1. The Core Philosophy (The "Soul")
The interface is not a page; it is a **Portal**. 
- It has **Mass**. (Interactions feel weighted, magnetic, physical).
- It has **Depth**. (Layers exist on Z-axis: Background < Glass < Content < Overlay).
- It has **Atmosphere**. (Lighting, Grain, Blur, Refraction).
- It is **Confident**. (Massive typography, extreme negative space, "Lights Out" focus).

---

## 2. Color System (The "Void" Palette)

### **Primary Backgrounds**
| Token | Hex | Description | Usage |
| :--- | :--- | :--- | :--- |
| `void-black` | `#050505` | The infinite dark. | **Global Background.** Never use pure black (#000000). |
| `void-deep` | `#0A0A0A` | Subtle separation. | Secondary sections (if absolutely needed). |
| `glass-base` | `rgba(255, 255, 255, 0.03)` | Frosted glass base. | For floating docks, navigation. |

### **The "Power" Accents (Neon & Laser)**
*Use these sparingly. They represent energy sources, lasers, or active states.*
| Token | Hex | Description | Usage |
| :--- | :--- | :--- | :--- |
| `klein-blue` | `#002FA7` | International Klein Blue. | **Primary Action.** (Play Button, Active Tab). High energy. |
| `electric-teal` | `#00D9FF` | Cyberpunk Cyan. | **AI/Tech Indicators.** (Match Score, AI Analysis). |
| `cinema-gold` | `#FFB800` | Golden Hour. | **Awards/Ratings.** (Star ratings, Oscar wins). |
| `signal-red` | `#DC2626` | Recording Light. | **Errors / Live Status.** (Only for "Live" or critical alerts). |

### **Text Hierarchy (Opacity System)**
*Never use gray hex codes. Use White + Opacity for perfect contrast on OLED.*
- **Headlines:** `#FFFFFF` (100% White)
- **Body Primary:** `rgba(255, 255, 255, 0.9)`
- **Body Secondary:** `rgba(255, 255, 255, 0.6)`
- **Metadata/Tech:** `rgba(255, 255, 255, 0.4)`
- **Dividers:** `rgba(255, 255, 255, 0.1)`

---

## 3. Typography System (The "Cast")

### **A. The Headline (The "Voice of God")**
- **Font:** `Manrope` (ExtraBold 800) OR `Bebas Neue` (Regular).
- **Character:** Geometric, Modern, Industrial.
- **Rules:**
  - **Tracking:** Tight (`-0.04em` or `tracking-tighter`).
  - **Leading:** Aggressive (`0.85` or `0.9`). Headlines should feel "stacked" and solid.
  - **Case:** UPPERCASE for Hero text. Sentence case for Section Headers.
  - **Scale:** `12vw` (Hero), `4rem` (Section).

### **B. The Body (The "Narrator")**
- **Font:** `Satoshi` (Variable) or `Geist Sans`.
- **Character:** Clean, Swiss-style, Neutral.
- **Rules:**
  - **Weights:** Light (300) for large paragraphs, Regular (400) for standard reading.
  - **Leading:** Relaxed (`1.6`).
  - **Tracking:** Normal (`0`).

### **C. The Metadata (The "Director's Monitor")**
- **Font:** `JetBrains Mono` or `Space Mono`.
- **Character:** Technical, Code-like, Precision.
- **Usage:** "Release Date", "Runtime", "Match Score", "Coordinates".
- **Rules:**
  - **Size:** Small (`text-xs` or `10px`).
  - **Case:** UPPERCASE.
  - **Tracking:** Wide (`0.1em` or `tracking-widest`).

---

## 4. Atmospheric Engineering (Texture & Light)

### **A. The "Film Grain" Overlay**
A persistent noise texture that kills the "flat digital" look.
```css
.film-grain {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background-image: url('/assets/noise-light.png'); /* 256x256 grayscale noise */
  opacity: 0.04; /* 4% visibility */
  pointer-events: none;
  mix-blend-mode: overlay;
}
```

### **B. The "Lens" (Glassmorphism)**
*Not the cheap Dribbble glass. This is "Optical Glass".*
- **Blur:** `backdrop-filter: blur(24px)` (Heavy blur).
- **Border:** `border: 1px solid rgba(255, 255, 255, 0.08)`.
- **Highlight:** `box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.05)`.
- **Noise:** Subtle noise texture blended into the background of the glass itself.

### **C. Volumetric Lighting (Glows)**
Do not use CSS box-shadows for glows. Use **Radial Gradients** in the DOM.
- **Spotlights:** Large, low-opacity gradients (`rgba(0, 47, 167, 0.15)`) fixed behind hero elements to simulate stage lighting.
- **Refraction:** When interactive elements (like the search bar) are hovered, a `linear-gradient` wipes across the border (shimmer).

---

## 5. Interaction Physics (The "Feel")

### **A. Magnetic Cursor ("Focus Ring")**
- **Default:** A small white dot (`4px`).
- **Hover (Text):** Expands to a transparent circle (`32px`) with `mix-blend-mode: difference`.
- **Hover (Action):** Morphs into a **Bracket `[ ]`** (Focus Reticle) that snaps to the element.

### **B. Magnetic Buttons**
Buttons do not sit still. They stick to the cursor within a 20px radius.
- **Physics:** `Spring(stiffness: 150, damping: 15)`.
- **Feel:** Heavy, tactile, expensive.

### **C. "Lights Out" Hover (The Grid)**
When a user hovers over a Movie Card:
1.  **Target:** Scales up (`1.05`), Opacity `1.0`, Z-Index `10`.
2.  **Siblings:** Opacity drops to `0.4`, Saturation drops to `0%` (Grayscale).
3.  **Result:** The user feels like the "spotlight" is on their selection.

### **D. Scroll Physics (Lenis)**
Native scroll is banned. Use **Lenis** for momentum scrolling.
- **Lerp:** `0.1` (Smooth, weighted feel).
- **Orientation:** Vertical only.

---

## 6. Layout Grids (The "Editorial" Structure)

### **A. The Hero (Asymmetrical)**
Never center-align everything. Use the "Rule of Thirds".
- **Left:** Massive Typography (Anchored).
- **Right:** Negative Space / 3D Element interaction zone.

### **B. The Masonry (The "Flow")**
- **Columns:**
  - Mobile: 1 Column.
  - Tablet: 2 Columns.
  - Desktop: 4 Columns.
- **Gap:** `gap-4` (Tight) or `gap-8` (Spacious).
- **Rhythm:** Mix Portrait (Posters) with Landscape (Stills) to create visual rhythm.

---

## 7. Motion Choreography (Timing)

### **A. Entrance (Stagger)**
Nothing appears all at once.
- **Header:** Slides up (`y: 100%` -> `0%`).
- **Cards:** Staggered fade-in (`delay: index * 0.05s`).
- **Curve:** `[0.22, 1, 0.36, 1]` (Custom Bezier - "Quintic Out").

### **B. Transitions (The "Cut")**
- **Duration:** `0.6s` to `0.8s`. (Slower than standard web transitions).
- **Style:** No cross-fades. Use **Morphs** (layoutId) or **Curtain Wipes** (screen goes black, then reveals).

---

## 8. Specific Component Directives

### **The Search Bar (The "Command Line")**
- **Look:** Not a box. A generic line or a floating capsule.
- **Font:** `Manrope` (Large, 24px).
- **Cursor:** Blinking block `█` (Cyberpunk feel).
- **State:** When active, the rest of the UI dims to `opacity-20`.

### **The Movie Card (The "Monolith")**
- **Base:** Pure Image. Rounded corners (`rounded-lg` or `rounded-none` for brutalist).
- **Hover:**
  - Image zooms slightly (`scale-110`) inside the container (masking).
  - Title slides up from bottom (masked reveal).
  - "Match %" badge glows `Electric Teal`.

### **The Navigation Dock (The "Floater")**
- **Position:** Fixed bottom center (Desktop & Mobile).
- **Look:** Frosted Glass Capsule.
- **Icons:** Minimal line icons (`Lucide`).
- **Interaction:** Icons scale up (`scale-125`) on hover (macOS Dock style).

---

**End of Visual DNA.**
*This document serves as the absolute source of truth for all visual decision-making.*
