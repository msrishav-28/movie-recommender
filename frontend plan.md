# Complete Frontend Specification for CineAesthete Platform
## Comprehensive UI/UX Design & Implementation Guide (Descriptive Format)

---

## EXECUTIVE SUMMARY

This document provides complete specifications for building CineAesthete's frontend - a cutting-edge movie discovery platform featuring the world's first aesthetic/vibe-based search system. The frontend must deliver an ultra-modern, immersive cinematic experience with glassmorphism effects, 3D interactions, smooth 120fps animations, and an intelligent component architecture built on Next.js 14 with App Router, React 18, TypeScript, and Tailwind CSS.

***

## 1. DESIGN SYSTEM FOUNDATION

### 1.1 Design Token Architecture

**Color System Philosophy:**
The color system follows a dark-mode-first approach optimized for cinematic content viewing. The primary background uses deep cinematic blacks (not pure black) at hex value 0A0E13 to provide depth while preventing OLED burn-in. Secondary surfaces progress through increasingly lighter shades (131921, 1C2633, 2A3544) creating natural visual hierarchy. Each surface color has corresponding hover states that are 8-12% lighter.

**Glassmorphism Implementation:**
Three tiers of glass effects are defined: light (5% white opacity), medium (8% white opacity), and heavy (12% white opacity). Each tier includes hover states with increased opacity. All glass surfaces use 24-pixel backdrop blur as the standard, with 32-pixel blur for prominent elements and 16-pixel blur for subtle overlays. The glass system includes proper fallbacks for browsers without backdrop-filter support, using solid backgrounds with reduced opacity.

**Text Hierarchy System:**
Text colors follow a strict opacity-based hierarchy: primary text at 98% white (F8F9FA), secondary at 72% white (B8BFC7), tertiary at 44% white (6C7580), and disabled at 26% white (404854). This creates natural reading flow and proper information hierarchy without requiring manual color adjustments.

**Accent Color Strategy:**
Primary accent uses Netflix red (E50914) for critical actions and CTAs, creating immediate recognition and urgency. Secondary cyan (00D9FF) highlights interactive elements and provides cool contrast. Tertiary golden (FFB800) indicates premium features and quality ratings. Each accent has defined hover states (10% lighter) and active states (10% darker), plus light variants at 10% opacity for subtle backgrounds.

**Semantic Color Application:**
Success green (00FF88) uses neon aesthetic for positive feedback. Warning orange matches tertiary golden for consistency. Error red (FF4757) differs from primary red to avoid confusion. Info blue (5D9CEC) provides neutral information highlights. All semantic colors include corresponding light backgrounds and glow effects.

**Border and Divider System:**
Default borders use 10% white opacity, increasing to 20% on hover and 50% on focus. Focus borders specifically use cyan color for WCAG compliance. Error borders use error red at 50% opacity. Disabled borders reduce to 5% opacity creating proper visual weight differentiation.

**Shadow and Elevation Philosophy:**
Six elevation levels create depth hierarchy: none (flat), extra-small (2px offset), small (8px offset), medium (16px), large (32px), extra-large (64px), and 2xl (96px). Each level uses layered shadows with multiple offsets for realistic depth perception. Shadow colors use pure black at varying opacities (12%, 16%, 24%, 32%, 40%) corresponding to elevation level.

**Glow Effect System:**
Glow effects simulate ambient light from interactive elements. Primary glow uses red at 40% opacity with 20-pixel blur radius, intensifying to 60% opacity on interaction. Secondary cyan glow follows same pattern. Success glow uses green. All glows support pulsing animation on active states with opacity ranging 40-80% over 2-second cycles.

### 1.2 Typography Scale System

**Font Family Strategy:**
Three font families create typographic hierarchy. Display font uses Inter Variable for titles and headings, providing weight range 300-900 with smooth interpolation. Body font uses SF Pro Display for optimal reading on Apple devices with Inter fallback. Cinematic font uses Bebas Neue for hero titles creating strong visual impact. Monospace uses JetBrains Mono Variable for code and technical metadata.

**Fluid Typography Implementation:**
All text sizes use CSS clamp function for responsive scaling. Extra-small text clamps between 12-14 pixels (0.75-0.875rem). Small text scales 14-16px. Base text (primary body) scales 16-18px. Large text scales 18-20px. Extra-large scales 20-24px. 2xl scales 24-32px. 3xl scales 32-48px. 4xl scales 48-80px. 5xl scales 64-128px. 6xl scales 80-160px for hero displays.

**Weight Distribution:**
Light weight (300) used for supporting text creating elegance. Regular (400) for standard body copy. Medium (500) for subtle emphasis. Semibold (600) for labels and UI elements. Bold (700) for headings. Extrabold (800) for subheadings. Black (900) for display titles and maximum impact.

**Line Height Specification:**
None (1.0) for display titles creating tight dramatic effect. Tight (1.25) for large headings. Snug (1.375) for medium headings. Normal (1.5) for body text ensuring readability. Relaxed (1.625) for large body text. Loose (2.0) for increased breathing room in dense content.

**Letter Spacing Philosophy:**
Tighter (-0.05em) for very large display text maintaining cohesion. Tight (-0.02em) for headings. Normal (0) for body text. Wide (0.05em) for small text improving legibility. Wider (0.1em) for uppercase labels. Widest (0.2em) for dramatic uppercase displays.

**Typography Style Definitions:**
Display styles use cinematic font family with black weight, uppercase transformation, and wide letter spacing for maximum drama on hero sections. Heading styles (H1-H6) use display font with bold to semibold weights, tight to normal line heights, and subtle negative letter spacing. Body styles use body font with regular weight and normal to relaxed line heights optimized for reading. Caption and label styles use medium weight with uppercase transformation and wide letter spacing for UI elements. Link styles inherit font size while adding medium weight, underline decoration with transparent initial color, and offset underline. Code styles use monospace font with slight size reduction (0.9em), padding, glass background, and cyan color.

**Text Modifiers:**
Gradient text applies linear gradient from primary to secondary text color with background-clip text for shimmer effects. Ellipsis utilities truncate text with single-line, two-line, or three-line variants using webkit-line-clamp. All typography maintains proper contrast ratios for WCAG AA compliance in both dark and light modes.

### 1.3 Spacing and Layout System

**8-Point Grid Foundation:**
Base unit of 4 pixels (0.25rem) creates consistent spacing. All spacing values are multiples of 4 up to 16px, then multiples of 8 up to 64px, then multiples of 16 up to 256px, ensuring perfect pixel alignment and mathematical harmony. Fractional values (0.5, 1.5, 2.5, 3.5) provide fine-tuning for specific use cases like icon spacing.

**Container Width System:**
Seven container sizes accommodate different content needs: extra-small (320px) for mobile, small (640px) for small tablets, medium (768px) for tablets, large (1024px) for small desktops, extra-large (1280px) for standard desktops, 2xl (1536px) for large screens, 3xl (1920px) for ultra-wide displays. Content max-width restricts readable content to 1800px preventing excessive line lengths. Reading width specifically limits text to 680px for optimal reading comprehension.

**Grid System Configuration:**
Twelve-column grid provides maximum flexibility for layouts. Default gap uses 24-pixel spacing (space-6 token). Small gap variant uses 16 pixels for tighter layouts. Large gap uses 32 pixels for prominent separation. All grid layouts respond fluidly to viewport changes with automatic column wrapping.

**Border Radius Scale:**
None (0) for sharp geometric elements. Extra-small (4px) for tight corners on small elements. Small (6px) for buttons and inputs. Medium (8px) for cards and containers. Large (12px) for prominent panels. Extra-large (16px) for modals and overlays. 2xl (24px) for hero sections. 3xl (32px) for maximum roundness. Full (9999px) for perfect circles and pills.

### 1.4 Elevation and Depth System

**Shadow Architecture:**
Each shadow uses multiple layers with different offsets and blur radii creating realistic depth. Extra-small shadow uses 1-pixel vertical offset with 2-pixel blur at 5% opacity for subtle lift. Small shadow combines 2-pixel and 1-pixel offsets with 8-pixel and 2-pixel blurs at 12% and 8% opacities. Medium shadow uses 4-pixel and 2-pixel offsets with 16-pixel and 8-pixel blurs at 16% and 8% opacities. Large shadow uses 8-pixel and 4-pixel offsets with 32-pixel and 16-pixel blurs at 24% and 12% opacities. Extra-large uses 16-pixel and 8-pixel offsets with 64-pixel and 32-pixel blurs at 32% and 16% opacities. 2xl shadow uses 24-pixel and 12-pixel offsets with 96-pixel and 48-pixel blurs at 40% and 20% opacities for maximum elevation.

**Inner Shadow System:**
Standard inner shadow uses 2-pixel inset with 4-pixel blur at 6% opacity for subtle depth. Large inner shadow uses 4-pixel inset with 8-pixel blur at 12% opacity for pronounced depth. Inner shadows simulate recessed surfaces like pressed buttons or input fields.

**Z-Index Layering:**
Base layer (0) for standard content flow. Dropdown layer (1000) for select menus and dropdowns. Sticky layer (1100) for persistent navigation. Fixed layer (1200) for scroll-independent elements. Modal backdrop (1300) for overlay backgrounds. Modal layer (1400) for dialog content. Popover layer (1500) for contextual overlays. Tooltip layer (1600) ensuring tooltips appear above all. Notification layer (1700) for toast messages. Max layer (9999) reserved for critical overlays like cookie consent.

### 1.5 Transition and Animation System

**Duration Scale Philosophy:**
Instant (100ms) for immediate feedback like button presses. Fast (200ms) for simple property changes like color or opacity. Normal (300ms) as default for most transitions balancing speed and smoothness. Slow (500ms) for complex animations involving multiple properties. Slower (800ms) for dramatic effects requiring user attention. Slowest (1200ms) for cinematic transitions between major states.

**Easing Function Library:**
Linear provides constant rate for infinite loops and scrolling. Ease-in starts slowly accelerating to create anticipation, using cubic-bezier(0.4, 0, 1, 1). Ease-out starts quickly decelerating to create settling, using cubic-bezier(0, 0, 0.2, 1). Ease-in-out combines both for natural motion, using cubic-bezier(0.4, 0, 0.2, 1). Smooth variant uses cubic-bezier(0.76, 0, 0.24, 1) for refined transitions. Expo variant uses cubic-bezier(0.87, 0, 0.13, 1) for dramatic acceleration. Back easing overshoots target creating playful bounce, using cubic-bezier(0.34, 1.56, 0.64, 1). Elastic easing creates spring-like oscillation using cubic-bezier(0.68, -0.55, 0.265, 1.55).

**Transition Presets:**
Default transition animates all properties over 300ms with ease-in-out. Fast transition uses 200ms with ease-out for snappy feedback. Colors transition specifically targets color, background-color, and border-color properties over 200ms. Transform transition applies to transform property over 300ms with back easing for playful movement. Opacity transition focuses on opacity over 200ms for fade effects.

**GPU Acceleration Strategy:**
All animated elements should use translateZ(0) or will-change property forcing GPU rendering. Transform and opacity are preferred animation properties as they don't trigger layout recalculation. Avoid animating width, height, top, left properties which cause expensive reflows. Use transform scale instead of width/height changes. Use transform translate instead of position changes.

### 1.6 Breakpoint System

**Mobile-First Philosophy:**
Extra-small (320px) targets smallest smartphones. Small (640px) covers standard smartphones in portrait. Medium (768px) handles tablets in portrait and large phones in landscape. Large (1024px) serves tablets in landscape and small laptops. Extra-large (1280px) targets standard desktop monitors. 2xl (1536px) serves large desktop displays. 3xl (1920px) accommodates ultra-wide and 4K displays.

**Responsive Behavior Patterns:**
Typography scales fluidly using clamp preventing abrupt size changes. Spacing adjusts proportionally at each breakpoint maintaining visual rhythm. Grid columns reduce on smaller screens: 12 columns on desktop, 6 on tablet, 4 on large mobile, 2 on small mobile. Navigation transforms from horizontal to hamburger menu below medium breakpoint. Component sizes reduce one step at mobile breakpoints (large becomes medium, medium becomes small). Touch targets increase to minimum 44x44 pixels on mobile for accessibility.

***

## 2. COMPONENT LIBRARY SPECIFICATIONS

### 2.1 Button Component System

**Variant Definitions:**
Primary variant uses solid primary color background with white text, designed for main CTAs requiring maximum attention. Secondary variant uses solid secondary color for alternative actions of moderate importance. Tertiary variant uses solid tertiary golden color for premium features and special actions. Ghost variant provides transparent background with border for subtle secondary actions. Glass variant implements glassmorphic effect with backdrop blur for modern aesthetic integration. Outline variant shows only border with transparent background for tertiary actions. Text variant removes all background and borders for inline actions and links. Gradient variant applies linear gradient from primary to secondary colors for premium features. Danger variant uses error red for destructive actions requiring user caution.

**Size Specifications:**
Extra-small (28px height) for compact interfaces and dense layouts, using 12-14px font size. Small (32px height) for secondary actions in normal layouts, using 14-16px font size. Medium (40px height) as default for primary actions, using 16-18px font size. Large (48px height) for prominent CTAs and hero sections, using 18-20px font size. Extra-large (56px height) for maximum impact on landing pages, using 20-24px font size. Icon-only buttons use square aspect ratio at specified height.

**State Behaviors:**
Default state shows base colors with subtle shadow. Hover state increases brightness by 10%, scales to 102%, and adds medium shadow within 200ms transition. Active state reduces brightness by 10% and scales to 98% providing tactile feedback. Focus state adds 2-pixel cyan outline at 2-pixel offset meeting accessibility requirements. Disabled state reduces opacity to 50% and prevents pointer events. Loading state shows spinner animation while making button non-interactive and hiding content.

**Interactive Features:**
Ripple effect creates expanding circle from click point, scaling from 0 to 4x over 600ms with fade to transparent. Effect originates at exact cursor position providing precise feedback. Glow effect adds ambient light around button intensifying on hover, pulsing subtly on active state. Haptic feedback triggers 10ms vibration on supported devices. Full-width option makes button span container width for mobile layouts or form submissions.

**Icon Integration:**
Left icon appears before text with 8-pixel gap, using 1.2em size relative to text. Right icon appears after text with same specifications. Icon-only mode centers icon without text using square button. Icons inherit button color and maintain proper alignment. Loading spinner replaces content while preserving button dimensions.

**Accessibility Requirements:**
Minimum contrast ratio 4.5:1 for text against background. Touch target minimum 44x44 pixels on mobile devices. Focus indicator clearly visible using cyan outline. Keyboard navigation fully supported with Enter and Space triggering. Loading state announces to screen readers. Disabled state properly communicated to assistive technology. ARIA labels required for icon-only buttons.

### 2.2 Movie Card Component System

**Card Structure:**
Poster container uses 2:3 aspect ratio (portrait orientation) matching standard movie posters. Container provides loading skeleton while image loads. High-resolution poster image fills container with object-fit cover preventing distortion. Lazy loading triggers when card enters viewport reducing initial page load. Progressive loading shows blur placeholder transitioning to full image.

**3D Tilt Effect:**
Mouse position tracked relative to card center creating parallax. X-axis rotation ranges -7 to +7 degrees based on vertical mouse position. Y-axis rotation ranges -7 to +7 degrees based on horizontal mouse position. Rotation uses spring physics with 300 stiffness and 30 damping for natural feel. Effect resets smoothly to 0,0 on mouse leave. Perspective set to 1000 pixels for realistic depth. Transform-style preserve-3d maintains depth hierarchy.

**Hover Overlay System:**
Gradient overlay fades in from 0 to 100% opacity over 300ms. Gradient flows from 20% black at top through 40% at middle to 90% at bottom creating natural depth. Overlay contains quick actions and information panel. Glassmorphic elements within overlay maintain visibility through backdrop blur. Overlay respects card border radius for polish.

**Quick Actions Interface:**
Three circular buttons positioned in center: play trailer, add to watchlist, view details. Each button uses 40-pixel diameter (36px on mobile) ensuring touch accessibility. Buttons use heavy glass effect with backdrop blur for visibility over any poster. Hover scales button to 110% with increased glow within 200ms. Icons use 20-pixel size with proper stroke width. Button layout uses flex gap for consistent spacing. Actions prevent event propagation avoiding card click when button clicked.

**Information Panel:**
Genre chips display up to 2 genres using pill-shaped badges. Each chip uses light glass effect with 4px padding horizontal, 2px vertical. Font size uses extra-small scale with medium weight. Runtime information shows clock icon with minute value. Information uses tertiary text color for hierarchy. Panel positioned at bottom of overlay with proper padding.

**Match Score Badge:**
Appears in top-right corner for aesthetic search results. Uses heavy glass with backdrop blur ensuring readability. Percentage value displays in bold with "Match" label. Background color uses success light with success text color. Badge includes subtle glow effect matching success color. Border radius uses full rounding creating pill shape.

**Card Footer:**
Fixed height section below poster containing title and metadata. Background uses default surface color with top border creating separation. Title uses semibold weight at small text size. Title truncates to 2 lines using webkit-line-clamp maintaining card height consistency. Year displays in tertiary text color creating hierarchy. Rating shows star icon with value in tertiary golden color. Footer padding matches card padding for alignment.

**Responsive Behavior:**
Large cards (280px width) on desktop reduce to 220px on tablet, 180px on mobile. Medium cards (220px) reduce to 180px on mobile. Small cards (160px) maintain size on mobile. Action buttons reduce from 40px to 36px diameter on mobile. Footer padding reduces by one spacing unit on mobile. Touch targets expand to 44px minimum on mobile despite visual size.

**Entrance Animation:**
Cards animate in sequentially using stagger effect. Initial state: opacity 0, translateY 20px creating appear-from-below effect. Animate to opacity 1, translateY 0 over 400ms. Delay calculation: index multiplied by 50ms creates wave effect. Animation uses ease-out for natural settling. Intersection observer triggers animation when card enters viewport.

**Performance Optimization:**
GPU acceleration forced using translateZ(0) preventing janky animations. Will-change property applied to transform and opacity during hover. Image loading uses next/image for automatic optimization. Poster dimensions specified preventing layout shift. Priority loading for above-fold cards improves perceived performance.

### 2.3 Glass Container Component

**Visual Properties:**
Background uses rgba white or black at 5%, 8%, or 12% opacity based on variant. Backdrop filter applies blur at 24px (default), 16px (light), or 32px (heavy). Border uses 1-pixel solid white at 10% opacity creating defined edge. Border radius inherits from parent or uses specified value. Box shadow optional adding depth when elevated.

**Fallback Strategy:**
Feature detection checks backdrop-filter support in browser. Unsupported browsers receive solid background at higher opacity. Light variant fallback uses 12% opacity solid. Medium variant uses 16% opacity. Heavy variant uses 20% opacity. Fallback maintains visual hierarchy while ensuring content readability.

**Padding System:**
Small padding uses 12-pixel inset for compact content. Medium padding uses 16-pixel inset as default. Large padding uses 24-pixel inset for spacious layouts. Extra-large padding uses 32-pixel inset for hero sections. Padding responsive, reducing one step on mobile breakpoints.

**Nesting Behavior:**
Nested glass containers increase blur intensity by 8 pixels. Nested containers increase opacity by 4% preventing complete transparency. Maximum nesting depth recommended at 3 levels. Deeper nesting may cause performance issues on lower-end devices.

**Accessibility Considerations:**
Content contrast maintained at minimum 4.5:1 against glass background. Text uses primary color (98% white) ensuring readability. Interactive elements increase opacity on hover improving discoverability. Focus indicators use solid color preventing transparency issues.

### 2.4 Input Component System

**Input Types:**
Text input accepts alphanumeric characters with optional patterns. Email input validates email format client-side. Password input toggles visibility with eye icon. Search input includes clear button and search icon prefix. Number input provides increment/decrement buttons. Textarea expands vertically based on content.

**Visual States:**
Default state shows medium border with secondary text color. Focus state increases border to 2 pixels using cyan color with glow effect. Error state uses error red border with shake animation and error message. Success state uses success green border with checkmark icon. Disabled state reduces opacity to 50% with not-allowed cursor. Loading state shows spinner in suffix position.

**Label System:**
Label positioned above input with 8-pixel gap. Font uses small size with medium weight. Required fields show red asterisk after label. Optional fields show "(optional)" in tertiary color. Label animations: shrink and move up on focus for floating label variant.

**Helper Text:**
Positioned below input with 4-pixel gap from input bottom. Uses extra-small font in tertiary color. Changes to error color when input has error. Maximum length: 80 characters preventing excessive height. Icon optional prefixing helper text for visual context.

**Error Messaging:**
Error text replaces helper text when validation fails. Uses error color with alert icon prefix. Shake animation draws attention: oscillate X position ±10px over 500ms. Multiple errors show first error only preventing UI overflow. Error clears on input change providing immediate feedback.

**Character Counter:**
Positioned in bottom-right corner when maxLength specified. Shows current/maximum character count format. Color transitions: tertiary (safe) → warning (80%) → error (100%). Updates in real-time as user types. Warning threshold at 80% capacity prepares user.

**Prefix and Suffix:**
Prefix icon positioned at input start with 12-pixel padding. Suffix icon positioned at input end with 12-pixel padding. Icons use secondary text color matching placeholder. Interactive suffixes (clear, toggle visibility) increase size on hover. Clear button appears only when input has value.

**Autofill Styling:**
Browser autofill overrides prevented using !important. Autofill background matches input background. Autofill text color uses primary text color. Transition delays removal of autofill styling creating smooth appearance.

**Accessibility:**
ARIA labels provided for all inputs describing purpose. Error messages linked using aria-describedby. Invalid state communicated with aria-invalid attribute. Required fields marked with aria-required. Disabled inputs use aria-disabled attribute. Placeholder never sole descriptor meeting WCAG standards.

### 2.5 Modal Component System

**Modal Types:**
Center modal appears in viewport center with backdrop overlay. Fullscreen modal covers entire viewport for immersive experiences. Drawer modal slides from side (left, right) for navigation or forms. Bottom sheet modal slides from bottom for mobile-optimized interactions. Popover modal positions relative to trigger element for contextual actions.

**Size Variants:**
Small modal (400px width) for confirmations and alerts. Medium modal (600px width) for forms and standard content. Large modal (800px width) for detailed content and multi-step processes. Extra-large modal (1200px width) for complex interfaces requiring space. Full modal uses 100% viewport width/height for maximum content area.

**Backdrop System:**
Overlay uses primary background at 95% opacity creating strong focus. Backdrop blur applies at 8 pixels creating depth separation. Click outside closes modal unless closeOnOutsideClick disabled. Escape key closes modal meeting accessibility standards. Backdrop prevents body scroll while modal open.

**Animation Patterns:**
Fade-in animation: opacity 0 to 1 over 300ms with ease-out. Scale-in animation: scale 0.9 to 1 combined with fade. Slide-up animation: translateY 40px to 0 for bottom sheets. Slide-from-side animation: translateX ±100% to 0 for drawers. Exit animations reverse entrance with 200ms duration.

**Header Section:**
Fixed at modal top with bottom border separator. Contains title using H3 heading style. Close button positioned top-right corner. Optional subtitle in secondary text below title. Header uses sticky position remaining visible during content scroll.

**Content Section:**
Scrollable container with custom scrollbar styling. Padding matches spacing system (24px default). Maximum height calculated: viewport height minus header/footer. Overflow handling: auto for scrolling, hidden for fixed height. Content maintains proper spacing using spacing tokens.

**Footer Section:**
Fixed at modal bottom with top border separator. Contains action buttons right-aligned. Primary action positioned rightmost. Secondary actions positioned left of primary. Cancel action positioned leftmost or left-aligned. Footer padding matches content padding for consistency.

**Focus Management:**
Focus trap activated on modal open preventing tab outside. Initial focus set to first focusable element or primary action. Tab order follows visual order left-to-right, top-to-bottom. Shift-Tab navigates backwards through elements. Focus returns to trigger element on modal close.

**Scroll Lock:**
Body scroll disabled when modal opens preventing background interaction. Scroll position saved before lock and restored after. Mobile handling prevents scroll behind modal on iOS Safari. Nested modals stack scroll locks properly.

**Responsive Behavior:**
Desktop modals maintain specified widths with margins. Tablet modals expand to 90% viewport width. Mobile modals expand to 100% width becoming fullscreen. Bottom sheet modals preferred on mobile for ergonomics. Drawer modals slide from bottom on mobile instead of side.

### 2.6 Dropdown/Select Component

**Single Select Mode:**
Displays selected option value or placeholder. Click opens dropdown menu with all options. Selected option marked with checkmark icon. Click option updates selection and closes dropdown. Keyboard navigation: Arrow up/down to highlight, Enter to select.

**Multi-Select Mode:**
Displays count of selected items or individual chips. Options show checkbox for independent selection. Selected options remain visible in dropdown. Apply button required to confirm selections. Clear all button resets all selections.

**Search Functionality:**
Search input appears at dropdown top. Filters options in real-time as user types. Highlights matching text within options. Shows "No results" message when no matches. Clears on dropdown close for fresh search next time.

**Virtualized Rendering:**
Renders only visible options plus buffer for performance. Calculates visible range based on scroll position. Option height standardized (40px default) for calculation. Supports thousands of options without performance degradation. Smooth scrolling maintained using CSS transforms.

**Visual Design:**
Trigger button matches input component styling. Dropdown menu uses elevated surface with large shadow. Options use medium height (40px) with 12px horizontal padding. Hover state applies surface hover color. Selected option uses primary color with light background. Dividers separate option groups with 1-pixel border.

**Positioning System:**
Dropdown positions below trigger by default. Positions above trigger if insufficient space below. Horizontal alignment matches trigger width by default. Minimum width matches trigger preventing narrower dropdown. Maximum height limits to viewport with scroll.

**Keyboard Interactions:**
Space/Enter opens dropdown and toggles selection. Arrow Down opens dropdown if closed, moves to next option if open. Arrow Up moves to previous option or closes if at first. Home key jumps to first option. End key jumps to last option. Escape closes dropdown canceling changes. Type-ahead focuses option matching typed characters.

**Loading State:**
Spinner displays in dropdown while options fetch. Skeleton rows shown maintaining dropdown height. Options disable while loading preventing interaction. Error message shows if loading fails with retry option.

**Empty State:**
"No options available" message displays when options array empty. Custom empty state content supported for branded experience. Maintains dropdown minimum height preventing collapse.

**Accessibility:**
ARIA combobox role applied to trigger element. ARIA-expanded attribute indicates dropdown state. ARIA-selected marks selected options. ARIA-activedescendant tracks focused option. Screen reader announces selection changes. Required/Invalid states properly communicated.

### 2.7 Tooltip Component

**Positioning Options:**
Top position centers tooltip above target with bottom arrow. Bottom position centers below target with top arrow. Left position aligns to target left with right arrow. Right position aligns to target right with left arrow. Auto position calculates optimal placement based on viewport space.

**Trigger Behaviors:**
Hover trigger shows tooltip on mouse enter, hides on mouse leave. Focus trigger shows on keyboard focus, hides on blur. Click trigger toggles tooltip visibility on click. Manual trigger requires programmatic show/hide control.

**Timing Configuration:**
Enter delay: 200ms before showing on hover preventing accidental triggers. Leave delay: 100ms before hiding allowing cursor readjustment. Close delay: 0ms for click triggers providing immediate response.

**Visual Styling:**
Background uses heavy glass effect with backdrop blur. Text uses small font size with medium weight. Maximum width: 280px preventing excessive tooltip width. Padding: 8px vertical, 12px horizontal for comfortable spacing. Border radius: medium (8px) for soft appearance. Box shadow: medium elevation for clear separation.

**Arrow Implementation:**
Arrow size: 8x8 pixels creating clear direction indicator. Arrow position: centered on tooltip edge pointing to target. Arrow uses pseudo-element matching tooltip background. Arrow maintains position when tooltip adjusts for viewport edges.

**Content Types:**
Plain text: simple string with automatic word wrap. Rich content: React components for complex tooltips. Maximum content height: 400px with scroll for excessive content. Icon support: prefix icon for visual context.

**Viewport Handling:**
Tooltip repositions automatically when near viewport edges. Maintains 8-pixel clearance from viewport boundaries. Flips to opposite position if space insufficient. Adjusts arrow position maintaining pointer to target. Handles scroll events updating position or hiding.

**Accessibility:**
ARIA role tooltip identifies element type. ARIA-describedby links tooltip to target. Screen readers announce tooltip content on focus. Keyboard focus shows tooltip same as hover. Escape key dismisses tooltip meeting standards. Touch devices show on tap with dismiss button.

### 2.8 Toast/Notification Component

**Notification Types:**
Success type uses success green with checkmark icon. Error type uses error red with alert icon. Warning type uses warning orange with warning icon. Info type uses info blue with information icon. Default type uses glass effect with neutral appearance.

**Position Variants:**
Top-right position: 24px from top, 24px from right for primary attention. Top-center position: centered horizontally for maximum visibility. Bottom-right position: 24px from bottom, 24px from right for subtle feedback. Bottom-center position: centered bottom for mobile-optimized placement.

**Visual Design:**
Background uses surface color with appropriate semantic color accent. Border uses 1-pixel left border in semantic color for type indication. Icon positioned left with semantic color matching type. Message text uses primary text color with small font size. Action button uses text variant aligned right. Close button uses ghost variant positioned top-right. Shadow uses large elevation separating from content.

**Auto-Dismiss:**
Default duration: 4000ms for standard messages. Success duration: 3000ms for quick acknowledgment. Error duration: 6000ms for important information. Warning duration: 5000ms for cautionary messages. Pause on hover prevents premature dismissal. Resume countdown on mouse leave.

**Progress Bar:**
Horizontal bar at toast bottom indicating time remaining. Width animates from 100% to 0% over duration. Color matches semantic color for visual consistency. Progress pauses on hover with main auto-dismiss. Resets on duration change.

**Queue Management:**
Maximum concurrent: 3 toasts preventing screen overflow. New toasts queue when maximum reached. Oldest toast dismisses when new toast added to queue. Toasts stack vertically with 12-pixel gap. Toasts animate in pushing existing toasts up/down.

**Animation Pattern:**
Enter animation: slide from right + fade in over 300ms. Exit animation: slide to right + fade out over 200ms. Stack movement: smooth transition over 200ms when toast added/removed. Uses spring easing for natural motion.

**Action Integration:**
Action button triggers custom callback when clicked. Common actions: Undo, View, Retry, Dismiss. Action closes toast automatically unless configured otherwise. Action uses text button variant matching toast type.

**Accessibility:**
ARIA role alert for immediate announcements. ARIA-live assertive for critical errors. ARIA-live polite for success/info messages. Screen readers announce message immediately. Focus management: focus action button for keyboard users. Close button keyboard accessible using Enter/Space.

---

## 3. PAGE ARCHITECTURE & LAYOUT PATTERNS

### 3.1 Homepage Layout Structure

**Hero Section Design:**
Full viewport height section creating immediate visual impact. Parallax background with three layers: backdrop image moving slowest at 0.2 speed, mid-layer gradient at 0.5 speed, foreground content static. Featured movie backdrop uses high-quality image from TMDb at 1920x1080 minimum resolution. Gradient overlay creates readability: radial gradient from transparent center to solid background at edges. Content container centers vertically and horizontally using flexbox. Glass container holds all content with heavy blur creating separation from background.

**Hero Content Organization:**
Movie title displays using display-2 style (5xl font size) with cinematic font family. Title animates in: fade from 0 to 1 opacity + translate from 40px below + font-weight morph from 300 to 900 over 800ms. Tagline appears below title in italic with secondary color and xl font size. Metadata bar shows rating, runtime, year with icons horizontally arranged, 24px gap between items. Action buttons group horizontally with 16px gap: primary "Watch Trailer" with play icon and glow effect, glass "Add to Watchlist" with plus icon. Scroll indicator animates at section bottom: chevron bouncing up-down 10px infinitely over 1.5s duration.

**Value Proposition Section:**
Three-column grid on desktop, single column on mobile. Each feature card uses medium glass container with xl border radius. Card contains icon at top (64px size with primary color gradient), heading using h3 style, description paragraph using body style, "Learn More" link using text link style. Cards animate on scroll: stagger entrance with 100ms delay between cards, fade-in-up animation over 400ms. Hover effect: lift by 8px with large shadow, icon rotates 5 degrees, transition over 300ms with back easing.

**Aesthetic Search Showcase:**
Full-width section with gradient mesh background animated using three.js or CSS. Background colors shift between primary, secondary, tertiary over 10s infinite loop. Content centers in container with max-width 1200px. Search prompt displays above input: heading "Describe your perfect movie vibe" with gradient text, magic wand icon animated pulsing. Large glass search bar (800px wide on desktop, full-width mobile, 64px height) with AI indicator icon and sparkle animation. Example query bubbles float around search bar: 15-20 bubbles with random positions, each clickable, slow floating animation using Perlin noise for organic movement. Bubbles use glass light background, hover increases size to 110% with glow effect.

**Trending Movies Section:**
Section header with gradient underline animation. Horizontal scroll carousel using momentum physics: friction 0.92, snap to center. Movie cards arranged with 24px gap, padding left/right 48px for edge fade. Gradient fade edges: 120px width, fading from background color to transparent. Scroll indicators as arrows positioned absolutely at left/right edges: hover increases size, click scrolls by viewport width with smooth animation. Cards use standard movie card component at medium size with 3D tilt enabled.

**How It Works Section:**
Three-step process displayed as horizontal timeline on desktop, vertical on mobile. Each step contains: large number badge (1, 2, 3) with primary color gradient background, icon representing action (search, discover, watch), heading describing step, paragraph explaining process. Connector lines between steps: dashed line in tertiary color, animated dash offset creates flowing effect. Steps animate sequentially on scroll: appear from left with 200ms stagger. Background uses subtle grid pattern with glass containers.

**Social Proof Section:**
Statistics displayed as four-column grid on desktop, two-column on tablet, single on mobile. Each stat card shows: large number (count-up animation on scroll), label below number, relevant icon. Numbers use display-3 font with gradient text. Count-up animation triggers when section enters viewport: animates from 0 to target over 2s with ease-out. Testimonial carousel below statistics: three testimonials visible on desktop, one on mobile, auto-play every 5s, manual navigation with dots. Each testimonial contains: user avatar (circular, 64px), quote text, user name and role, star rating.

**Final CTA Section:**
Full-width section with primary color gradient background. Content centers with max-width 800px. Large heading: "Start Discovering Your Next Favorite Film" using display-3 style. Supporting text paragraph below heading. Primary CTA button (xl size with glow): "Get Started Free". Secondary text below: "No credit card required" with tertiary color. Trust badges row: app store badges, rating, user count.

### 3.2 Movie Detail Page Architecture

**Hero Section Layout:**
Full-width parallax section with three-layer background. Backdrop image positioned with parallax effect. Gradient overlays: left-to-right fade on left side for readability, bottom-to-top fade for footer text. Content grid: poster left (500px width on desktop), info panel right (flexible width). Poster uses 3D floating animation: subtle rotation on scroll (±5 degrees), vertical float 20px range over 3s infinite, shadow follows float creating depth.

**Information Panel Structure:**
Title stack at top: main title using h1 style, original title below in secondary color and xl font if different, tagline in italic with cyan color. Metadata bar: year, rating, runtime, language with icons and separators. Overall rating display: large circular progress (200px diameter), percentage inside circle, star icon at center, label "Overall Rating" below. Multi-dimensional ratings: four smaller radial charts (plot, acting, cinematography, soundtrack), arranged 2x2 grid, each 100px diameter with label and value.

**Action Buttons Row:**
Primary button: "Watch Trailer" with play icon, large size, glow effect. Secondary buttons: "Add to Watchlist" (plus icon), "Rate Movie" (star icon), "Share" (share icon). Buttons arranged horizontally with 12px gap, wrap on mobile. Streaming availability section below actions: "Available on" label, service logos horizontally arranged (48px size each), tooltip shows service name and type (subscription/rent/buy) on hover.

**Sentiment Analysis Dashboard:**
Glass container with heavy blur and large radius. Grid layout: overall sentiment score left (large number with label), emotion radar chart center (canvas element, 200px size), sentiment distribution right (three progress bars for positive/neutral/negative). What People Loved/Disliked sections: two columns, each containing extracted phrases from reviews with background highlight matching sentiment, bullet list format. Expandable "Read Full Analysis" link reveals detailed sentiment breakdown.

**Synopsis Section:**
Heading: "Overview" using h2 style. Plot summary paragraph: body style, max 4 lines initially with "Read More" expansion. Genre tags below synopsis: clickable chips with glass background, horizontal arrangement with wrap. Keywords/themes as smaller chips below genres. Content truncates on mobile for space efficiency.

**Aesthetic Frames Gallery:**
Heading: "Visual Journey" with subtitle explaining feature. Horizontal scroll carousel with momentum: friction 0.95, snap to each frame. Frame cards 400px width on desktop, 280px mobile, 16:9 aspect ratio. Each frame contains: high-res screenshot, timestamp overlay top-left, color palette strip bottom (5 dominant colors, 40px height each showing hex and percentage on hover), visual tags as floating chips (rain, night, neon, etc). Lightbox opens on frame click: fullscreen overlay, large image, swipe navigation, close button, escape key support. "Find Similar Aesthetic" button below carousel: secondary button with sparkles icon.

**Cast & Crew Section:**
Tab navigation: Cast / Crew / Director. Horizontal scroll for person cards. Person card design: circular avatar 120px, name below in semibold, role/character below name in tertiary color. Hover reveals filmography: glass overlay, mini poster grid showing top 5 films, fade-in animation 300ms. "View Full Cast" link at end of scroll expands to full cast page.

**Videos Section:**
Tab navigation: Trailers / Teasers / Behind the Scenes / Clips. Video thumbnails in grid: 3 columns desktop, 2 tablet, 1 mobile. Each thumbnail 16:9 aspect ratio with play button overlay. Click opens video modal: fullscreen player, YouTube/Vimeo embed, close button, related videos sidebar on desktop.

**Reviews Section:**
Section header with "Write Review" CTA button (opens review modal). Sort dropdown: Most Helpful, Most Recent, Highest Rated, Lowest Rated. Review cards: user avatar left, content right, rating stars top, date below rating, review text with expand/collapse for long reviews, helpful counter with upvote button, sentiment badge (positive/neutral/negative) top-right. Load more button or infinite scroll pagination.

**Similar Movies Section:**
Tab navigation: Similar Movies / Same Director / Same Genre / Aesthetic Matches. Horizontal carousel for each tab. Movie cards use standard component at small size. Each section lazy loads preventing initial page bloat.

**Technical Details Accordion:**
Expandable sections: Budget & Revenue, Production Companies, Countries, Languages, Release Dates. Each section uses glass container expanding on click. Content formatted as key-value pairs with proper typography hierarchy. External links to IMDb/TMDb as small pills.

**Floating Action Bar:**
Sticky bar at bottom when scrolling past hero. Contains primary actions: Watch Trailer, Toggle Watchlist, Rate Movie, Share. Glass background with backdrop blur. Slides in from bottom when activated. Hides when scrolling up, shows when scrolling down. Mobile-optimized with larger touch targets.

### 3.3 Browse/Search Results Page

**Page Header:**
Title "Explore Movies" or "Search Results for [query]" using h1 style. Result count below title in tertiary color. Quick stats: total movies, filters applied. Filter toggle button on mobile (hamburger icon) opens drawer.

**Filter Panel Layout:**
Sidebar on desktop (280px width), drawer on mobile (slides from left). Glass container with medium blur. Scrollable content with custom scrollbar. Sections: Genre (multi-select chips), Year Range (dual-handle slider showing min/max), Rating (minimum stars slider), Runtime (range slider in minutes), Language (searchable dropdown), Streaming Services (checkbox grid with logos), Mood Tags (aesthetic filters as chips). Apply button sticky at bottom, Reset button next to Apply. Active filter count badge on filter button showing number applied.

**Results Grid:**
Responsive grid: 6 columns desktop (1920px+), 5 columns large desktop (1536px+), 4 columns desktop (1280px), 3 columns tablet (768px), 2 columns mobile (640px). Grid gap 24px. Movie cards use standard component at medium size. Masonry layout option for varied card heights when available.

**Sort & View Options:**
Toolbar above grid: sort dropdown left (Trending, Top Rated, Recently Added, Release Date, Title A-Z), view toggle right (grid/list icons). Active filters display between sort and view: removable chips showing applied filters, click X removes filter, click chip edits filter.

**Empty State:**
Displayed when no results match filters. Illustration (movie reel with magnifying glass). Message: "No movies found matching your filters". Suggestion text: "Try adjusting your filters or search terms". Reset button to clear all filters. Alternative suggestions: "You might like" section with recommended movies.

**Infinite Scroll:**
Loads 24 movies initially. Intersection observer triggers next batch when user scrolls to 80% of page. Loading indicator: skeleton cards matching grid layout, shimmer effect. Smooth insertion of new cards without layout shift. "Back to Top" button appears after scrolling past viewport, positioned bottom-right, glass background, click scrolls to top with smooth animation.

**Performance Optimizations:**
Virtual scrolling for very large result sets (1000+ movies). Image lazy loading with intersection observer. Skeleton loading states during fetch. Debounced filter updates (300ms) preventing excessive API calls. URL query parameters for shareable filtered views. Browser back/forward navigation preserves filter state and scroll position.

### 3.4 Dashboard Layout

**Welcome Header:**
Personalized greeting: "Welcome back, [Username]" with current time-based modifier (Good morning/afternoon/evening). Quick stats row: Movies Watched (count-up number), Watchlist Items, Reviews Written, Following. Stats use glass cards with icon and label. "Continue Watching" carousel if applicable: shows partially watched movies with progress bar overlay on poster.

**Recommendation Feed Layout:**
Multiple feed sections stacked vertically. Each section contains: heading with icon (For You, Trending This Week, Hidden Gems, Because You Loved [Movie], Aesthetic Picks,

# Complete Frontend Specification - Missing Elements & Comprehensive Details

## CRITICAL AREAS NOT YET COVERED

### 1. STATE MANAGEMENT ARCHITECTURE

**Global State Strategy:**
The application uses Zustand for lightweight global state management combined with React Query for server state. Global state divides into clear domains: user state (authentication status, profile data, preferences), UI state (theme, sidebar open/closed, modal visibility), cart state for premium features, and notification state. Each state slice lives in separate store files preventing monolithic state objects.

**User State Management:**
User authentication state persists in localStorage with automatic rehydration on page load. The store tracks current user object, authentication token, loading state, and error state. Actions include login, logout, update profile, and refresh token. Token refresh happens automatically before expiration using interceptors. Logout clears all user-related state and redirects to homepage.

**UI State Patterns:**
Theme state manages dark/light mode preference with system preference detection as default. The state persists to localStorage and applies on mount before paint preventing flash of wrong theme. Modal state uses stack pattern allowing multiple nested modals with proper focus management. Sidebar state tracks open/closed with animation state preventing premature DOM removal. Toast notification state uses queue system with maximum 3 concurrent toasts.

**Server State with React Query:**
Movie data caching uses React Query with stale-while-revalidate strategy. Cache time set to 5 minutes for movie listings, 30 minutes for movie details (changes rarely). Background refetch occurs on window focus and network reconnection. Optimistic updates for user actions (rating, watchlist) with rollback on error. Query invalidation cascades related queries maintaining consistency.

**Form State Management:**
React Hook Form handles all form state for performance. Validation runs on blur for better UX than on-change. Error messages appear immediately on blur, clear on focus. Async validation debounces by 300ms preventing excessive API calls. Form reset clears all fields and errors atomically. Dirty state prevents accidental navigation away from unsaved changes.

**Search State Handling:**
Search query lives in URL parameters enabling shareable searches. Debounced search input waits 300ms after typing stops before triggering search. Search history stores in localStorage with maximum 10 recent searches. Search suggestions fetch from API with abort on new keystroke. Filter state synchronizes with URL allowing browser back/forward navigation.

**Watchlist State Synchronization:**
Watchlist state mirrors server state with optimistic updates. Adding movie shows immediately in UI while API call runs in background. API failure reverts optimistic update and shows error toast. Watchlist count updates reactively across all components displaying it. Removal confirmation modal prevents accidental deletion.

**Real-time State Updates:**
WebSocket connection maintains for real-time notifications. Connection state tracked (connecting, connected, disconnected, error). Automatic reconnection with exponential backoff on disconnect. Message handling updates relevant state slices. Unread notification count increments on message receipt.

### 2. ANIMATION & MOTION SYSTEM DEEP DIVE

**Page Transition Animations:**
Route changes trigger coordinated exit and enter animations. Exit animation: current page fades out (opacity 1 to 0) and scales down (1 to 0.95) over 200ms. Content waits for exit completion before mounting new route. Enter animation: new page fades in (opacity 0 to 1) and translates up (20px to 0) over 400ms with 100ms delay after exit. Scroll position resets to top on route change unless back navigation.

**Scroll-Triggered Animations:**
Intersection Observer watches elements for viewport entry. Elements below fold start invisible (opacity 0, translateY 20px). On intersection at 20% threshold, elements animate visible over 400ms. Stagger effect for lists: each item delays by index × 50ms creating wave. Animation plays once per element, doesn't repeat on re-enter. Reduced motion media query disables animations respecting user preference.

**Micro-interactions Catalog:**
Button press: scale 0.98 with 100ms duration on active state. Checkbox check: checkmark draws from left-to-right over 300ms with elastic easing. Toggle switch: handle slides with spring physics (stiffness 300, damping 30). Radio button select: inner dot scales from 0 to 1 with bounce. Input focus: border thickness increases 1px to 2px, color shifts cyan with 200ms transition. Loading spinner: rotate 360 degrees over 1s infinite linear.

**Hover Animations:**
Card hover: elevates 8px (translateY), shadow intensifies, scale increases 1.02, all over 300ms with ease-out-back. Button hover: brightness increases 110%, shadow adds, slight scale 1.02. Link hover: underline draws from left to right over 200ms. Icon hover: rotates 15 degrees or bounces depending on context. Image hover: scale 1.08 inside fixed container creating zoom effect.

**Loading Animations:**
Skeleton screens use shimmer effect: linear gradient -45 degrees, light band moves left to right over 2s infinite. Pulse animation: opacity oscillates 0.5 to 1 over 1.5s infinite. Spinner variations: circular (border-top rotates), dots (three dots bounce sequentially), bar (progress bar fills). Skeleton matches content layout exactly preventing layout shift on load.

**Exit Animations:**
Modal dismissal: scale from 1 to 0.9, opacity 1 to 0 over 200ms, backdrop fades 300ms. Toast removal: slides right 100% and fades over 200ms. Dropdown close: scale-y from 1 to 0 from origin top over 150ms. Drawer close: translateX to starting position (±100%) over 300ms with ease-in.

**Gesture Animations:**
Swipe gestures on carousels: follow finger with physics, momentum continues after release, snap to nearest item. Pull-to-refresh: content translates down following finger, loading indicator appears, threshold at 80px triggers refresh. Long press: scale down 0.95 over 200ms, haptic feedback, scale returns on release. Pinch zoom on images: scale follows gesture, constraints minimum 1x maximum 3x.

**Parallax Scroll Effects:**
Background images move slower than foreground creating depth. Hero backdrop scrolls at 0.2x scroll speed. Mid-layer elements at 0.5x speed. Foreground content at 1x speed. Parallax disabled on mobile due to performance. Transform3d forces GPU acceleration. Will-change property set during scroll.

**Data-Driven Animations:**
Chart animations trigger on viewport entry. Line charts: path draws from 0% to 100% stroke-dashoffset over 1s. Bar charts: bars grow from 0 height to full over 800ms with stagger. Pie charts: segments animate from 0 to target angle sequentially. Number count-ups: increment from 0 to target over 2s using requestAnimationFrame.

**Performance Considerations:**
GPU-accelerated properties preferred: transform, opacity. Layout-triggering properties avoided: width, height, top, left. Will-change applied during animation only. Transform3d forces GPU layer creation. Animations throttle to 60fps maximum. Complex animations pause when tab inactive. Reduced motion media query respected throughout.

### 3. COMPREHENSIVE ACCESSIBILITY STANDARDS

**Keyboard Navigation Implementation:**
Tab order follows visual order: left-to-right, top-to-bottom. All interactive elements reachable via keyboard. Skip link at page top jumps to main content. Focus trap in modals prevents tabbing outside. Escape key closes overlays (modals, dropdowns, tooltips). Enter/Space activates buttons and toggles. Arrow keys navigate lists and menus. Home/End jump to first/last item. Custom keyboard shortcuts documented in help section.

**Focus Management System:**
Focus indicators clearly visible: 2px solid cyan outline, 2px offset from element. Outline never removed without alternative indicator. Focus order logical and predictable. Focus returns to trigger element on modal close. Focus sets to first interactive element on page load. Focus moves to error field on form submission failure. Focus visible indicator meets 3:1 contrast ratio.

**Screen Reader Optimization:**
Semantic HTML throughout: header, nav, main, aside, footer, article, section. ARIA labels on icon buttons: "Add to watchlist", "Close modal". ARIA live regions announce dynamic content: toasts use aria-live="assertive" for errors, "polite" for success. ARIA expanded indicates collapsible state. ARIA-describedby links inputs to helper text. ARIA-invalid on error fields. ARIA-hidden on decorative elements. Skip links enable content bypass. Landmark roles when semantic HTML insufficient.

**Color Contrast Requirements:**
Normal text (under 18pt) requires 4.5:1 contrast ratio. Large text (18pt+ or 14pt bold+) requires 3:1 ratio. UI components require 3:1 contrast with adjacent colors. Focus indicators require 3:1 contrast with background. Color never sole indicator of information. Success/error messages include icons. Links distinguishable without color (underline or weight).

**Text Accessibility:**
Minimum font size 14px (0.875rem) preventing strain. Line height minimum 1.5 for body text improving readability. Line length maximum 680px (70-80 characters) optimizing reading. Text resizable to 200% without loss of content or functionality. Font smoothing optimized for screen rendering. Justified text avoided preventing rivers of whitespace.

**Interactive Element Accessibility:**
Touch targets minimum 44x44 pixels on mobile per WCAG 2.5.5. Adequate spacing between targets preventing mis-taps. Clickable area larger than visible button. Disabled buttons properly indicated with aria-disabled. Loading buttons announce state to screen readers. Button labels descriptive avoiding "Click here".

**Form Accessibility:**
Labels visible and properly associated with inputs. Required fields indicated with text and asterisk. Error messages specific and actionable. Error announcements via aria-live. Field types match input (email, tel, url). Autocomplete attributes aid form filling. Fieldsets group related inputs. Legends describe fieldset purpose.

**Media Accessibility:**
Images include descriptive alt text. Decorative images use empty alt. Complex images have long descriptions. Videos include captions and transcripts. Audio descriptions available for video content. Media players keyboard accessible. Volume controls available. Auto-play avoided or pausable.

**Motion and Animation Accessibility:**
Prefers-reduced-motion respected throughout. Essential animations only when motion reduced. No automatically playing videos in reduced motion. Parallax effects disabled in reduced motion. Transitions simplified or instant. Carousel auto-play stoppable. Infinite animations pausable.

**Language and Reading Level:**
Language attribute set on HTML element. Language changes marked with lang attribute. Content written at appropriate reading level. Complex terms explained on first use. Abbreviations expanded with abbr element. Idioms and jargon avoided or explained.

**ARIA Patterns Implementation:**
Combobox pattern for select components. Accordion pattern for expandable sections. Tabs pattern for tabbed interfaces. Dialog pattern for modals. Menu pattern for navigation menus. Tooltip pattern for contextual information. Alert pattern for important messages. Progress bar pattern for loading states.

### 4. PERFORMANCE OPTIMIZATION STRATEGIES

**Code Splitting Strategy:**
Route-based splitting: each page route in separate bundle loaded on demand. Component-based splitting: heavy components (charts, editors) lazy loaded. Vendor splitting: React, libraries in separate bundle cached long-term. Dynamic imports use React.lazy with Suspense boundaries. Critical CSS inlined in HTML head. Non-critical CSS loaded asynchronously. JavaScript modules load with async or defer attributes.

**Image Optimization Pipeline:**
Next.js Image component automatic optimization. Responsive images with srcset for different viewports. WebP format with JPEG/PNG fallback. Lazy loading on images below fold. Blur placeholder while loading. Priority loading for above-fold images. Image CDN serves optimized versions. Maximum width constraints prevent oversized downloads.

**Bundle Size Optimization:**
Tree shaking eliminates unused code. Lodash replaced with individual lodash-es imports. Moment.js replaced with date-fns (smaller). Icon libraries import only used icons. CSS unused styles purged with PurgeCSS/Tailwind. Compression enabled: Brotli for modern browsers, Gzip fallback. Source maps excluded from production. Environment-specific code removed via webpack.DefinePlugin.

**Caching Strategy:**
Static assets cache with versioned URLs: 1 year cache time. API responses cache with SWR strategy: cache time 5 minutes, revalidate in background. Service worker caches critical assets for offline. Browser cache headers properly configured. CDN cache for global performance. Cache invalidation on deployment via URL versioning.

**Loading Strategy:**
Critical path optimized: HTML → Critical CSS → Critical JS. Above-fold content renders first (time-to-first-byte < 200ms target). Below-fold content loads after initial render. Third-party scripts defer or async load. Font loading optimized with font-display: swap. Preload critical resources in HTML head. Prefetch likely next pages on link hover.

**Runtime Performance:**
Virtual scrolling for large lists (1000+ items). Debouncing expensive operations (search, resize handlers). Throttling high-frequency events (scroll, mouse move). Memoization of expensive calculations with useMemo. Component memoization with React.memo. UseCallback for function identity stability. Lazy initialization for expensive state. Web Workers for heavy computation offloading main thread.

**Network Optimization:**
GraphQL for efficient data fetching (only requested fields). Request batching combines multiple API calls. Request deduplication prevents duplicate simultaneous calls. Connection pooling reuses HTTP connections. HTTP/2 multiplexing for parallel requests. Compression reduces payload size. WebSocket for real-time reducing polling overhead.

**Rendering Optimization:**
Server-side rendering for SEO and initial paint. Static generation for pages without dynamic data. Incremental static regeneration updates static pages. Client-side hydration optimized avoiding mismatches. Partial hydration only interactive components. Islands architecture for mixed static/dynamic content.

**Monitoring and Metrics:**
Core Web Vitals tracking: LCP (Largest Contentful Paint < 2.5s), FID (First Input Delay < 100ms), CLS (Cumulative Layout Shift < 0.1). Time to Interactive < 3.8s on mobile. First Contentful Paint < 1.8s. Real User Monitoring captures actual user experience. Synthetic monitoring tests from global locations. Performance budgets enforced in CI/CD: bundle size < 200KB gzipped, total page weight < 1.5MB.

### 5. ERROR HANDLING & EDGE CASES

**API Error Handling:**
Network errors show retry button with exponential backoff. 401 Unauthorized triggers automatic token refresh then retry. 403 Forbidden redirects to forbidden page. 404 Not Found shows custom error page with suggestions. 500 Server Error displays friendly message with support contact. Timeout errors (> 30s) show retry option. Rate limit errors (429) show wait timer before retry allowed.

**Form Validation Errors:**
Required field validation on blur showing "This field is required". Format validation shows specific error: "Please enter valid email address". Length validation specifies limits: "Password must be at least 8 characters". Custom validation shows domain-specific errors: "Username already taken". Multiple errors show first error only preventing overwhelming user. Error clears immediately on field change providing feedback.

**Image Loading Errors:**
Failed poster images show placeholder with movie title and broken image icon. Retry button attempts reload. Fallback to lower resolution if available. Graceful degradation to text-only if no images load. Alt text always provided for screen readers. Loading spinner shows while image loads. Blur placeholder prevents layout shift.

**Video Player Errors:**
Playback errors show specific messages: "Video unavailable in your region", "Format not supported", "Network error". Retry button for network failures. Quality selector allows manual quality reduction. Fullscreen fallback if native fullscreen fails. Keyboard controls documented and always available.

**Search Edge Cases:**
No results shows empty state with search suggestions. Misspellings show "Did you mean...?" suggestions. Too many results warns and suggests filtering. Search timeout (> 5s) shows partial results with retry option. Special characters escaped preventing injection. Very long queries truncated with warning.

**Authentication Edge Cases:**
Session expiration shows modal requiring re-login preserving current action. Multiple tabs logout synchronizes via broadcast channel. Remember me persists session 30 days. Forgot password rate limits prevents abuse. Email verification link expiration handled gracefully. OAuth failures redirect to login with error message.

**Payment Processing Errors:**
Card declined shows specific reason if provided. Payment timeout shows status checking mechanism. Duplicate payment detection prevents double charging. Currency conversion errors fallback to USD. Three-strike lockout on repeated failures. Support contact prominent on errors.

**Offline Scenarios:**
Connection loss shows banner: "You are offline. Some features unavailable". Cached content displays with "Viewing cached version" indicator. Queue user actions for retry when online. Service worker caches critical pages. Offline page shows when no cache available. Connection restoration removes offline banner and syncs queued actions.

**Edge Case Data:**
Empty states throughout: empty watchlist, no search results, no reviews, no recommendations. Loading states prevent layout shift. Long text truncates gracefully with expand option. Very long titles wrap or ellipsis with tooltip. Missing optional data handled gracefully (no tagline, no runtime). Null/undefined values never break UI. Date formatting handles all locales. Numbers format with proper separators.

**Browser Compatibility Issues:**
Backdrop-filter fallback for unsupported browsers. Grid layout fallback for IE11. Flexbox bugs worked around. CSS custom properties fallback values. JavaScript polyfills loaded conditionally. Feature detection before usage. Progressive enhancement approach. Graceful degradation where enhancement impossible.

### 6. LOADING STATES & SKELETON SCREENS

**Skeleton Design Principles:**
Skeletons match final content layout exactly preventing layout shift. Use glass-light background with shimmer animation. Pulse between 0.5 and 1 opacity over 1.5s. Rectangular shapes with rounded corners matching components. Circular shapes for avatars. Height matches actual content height. Width matches container constraints.

**Page-Level Skeletons:**
Homepage skeleton: hero section with title rectangle and button shapes, carousel with 6 movie card skeletons. Browse page skeleton: filter sidebar with rectangles for each filter section, grid of movie card skeletons matching grid columns. Movie detail skeleton: large rectangle for poster, text lines for title and info, smaller rectangles for buttons, frame gallery skeleton.

**Component-Level Skeletons:**
Movie card skeleton: rectangular poster area 2:3 ratio, two text lines below for title, small circle and line for rating. Review card skeleton: circular avatar left, three text lines right, star shapes for rating. Person card skeleton: circular avatar, two text lines for name and role. List item skeleton: rectangular thumbnail left, two text lines right.

**Data-Fetching States:**
Initial load shows skeleton. Refetch shows existing content with subtle loading indicator (top progress bar or spinner overlay). Background refetch shows no indicator (stale-while-revalidate). Pagination shows skeleton rows at end while loading more. Infinite scroll shows skeleton cards at scroll bottom.

**Optimistic UI Patterns:**
Add to watchlist shows immediately in UI, reverts if API fails. Rate movie updates rating display instantly, syncs in background. Post review shows in list immediately with "Posting..." indicator. Delete item removes from UI immediately, restores if API fails. Edit profile updates immediately, reverts changes on error.

**Transition Loading States:**
Route change shows top progress bar moving 0-90% during load, completing to 100% on mount. Modal content loading shows spinner in center while content fetches. Lazy-loaded component shows fallback until code bundle loads. Tab change shows loading indicator in tab content area. Search results transition through loading state preventing jarring appearance.

### 7. FORM PATTERNS & VALIDATION

**Input Validation Rules:**
Email: RFC 5322 compliant regex, checks for @ and domain. Password: minimum 8 characters, must contain uppercase, lowercase, number, special character. Username: 3-20 characters, alphanumeric plus underscore/hyphen, availability check on blur debounced 500ms. URL: valid URL format with protocol. Phone: international format support with country code dropdown.

**Real-Time Validation Timing:**
Required field: validates on blur, shows error immediately. Format validation: validates on blur after first character typed. Async validation: debounces 500ms after typing stops before API check. Password strength: updates in real-time with visual meter. Confirmation fields: validates on blur checking match with original.

**Error Message Patterns:**
Generic: "This field is required". Specific: "Email must be in format: user@example.com". Actionable: "Password must contain at least one uppercase letter". Contextual: "This username is already taken. Try username123". Friendly tone avoiding technical jargon. Positive framing when possible.

**Success Feedback:**
Valid fields show checkmark icon in suffix position. Success message appears: "Email verified successfully". Form submission success shows toast notification. Redirect happens after brief success message (1.5s). Success state uses success color consistently.

**Multi-Step Form Pattern:**
Progress indicator shows current step and total steps. Back button returns to previous step preserving values. Next button validates current step before proceeding. Step data saves to session storage preventing loss. Final step shows review of all inputs before submission. Edit buttons on review page return to specific step.

**Autosave Functionality:**
Form saves to localStorage every 30s while user typing. Draft indicator shows "Draft saved at [time]". Draft loads automatically on return to form. Clear draft option available. Draft expires after 7 days. Conflict resolution if form changes while user away.

**File Upload Patterns:**
Drag-and-drop zone with visual feedback on dragover. File picker fallback for click to upload. Preview shows after selection (image thumbnail or filename). Progress bar during upload showing percentage. Cancel button aborts upload. Error handling: file too large, wrong format, upload failure. Multiple file upload shows list with individual progress bars.

### 8. SEARCH FUNCTIONALITY DEEP DIVE

**Search Input Behavior:**
Focus highlights input with cyan border and glow. Placeholder text: "Search movies, actors, directors..." Autocomplete dropdown appears after 2 characters typed. Dropdown shows suggestions: movies (with poster thumbnail), people (with avatar), genres. Arrow keys navigate suggestions, Enter selects. Escape closes dropdown. Clear button (X) appears when text present.

**Search Suggestions Algorithm:**
Fuzzy matching allows typos using Levenshtein distance. Title matching prioritized over other fields. Popular movies ranked higher in suggestions. Recently viewed movies appear in suggestions. Search history influences suggestion ranking. Maximum 10 suggestions shown preventing overwhelming. Mix of movies (5), people (3), genres (2) for variety.

**Search Results Layout:**
Results header shows query and count: "Showing 142 results for 'inception'". Filter panel on left: type (movies/people), genre, year, rating. Sort dropdown on right: Relevance, Rating, Release Date, Popularity. Results use card grid matching browse page. Load more pagination or infinite scroll. No results shows suggestions and spell check.

**Search Performance:**
Query debounced 300ms after last keystroke. Previous request aborted when new query starts. Results cache for 5 minutes in React Query. Instant results from cache on repeated search. Background refetch on cache hit for freshness. Loading indicator shows while fetching: ghost results or spinner.

**Advanced Search Features:**
Quote phrases for exact match: "the dark knight". Exclude terms with minus: "batman -animated". Filter by field: "actor:tom hanks" OR "director:nolan". Year range: "2010..2020". Rating range: "rating:8+". Combine filters with AND/OR logic. Help panel explains advanced syntax.

**Search History:**
Last 10 searches stored in localStorage. History dropdown shows on input focus. Click history item performs search immediately. Delete button removes individual history items. Clear all button removes entire history. History syncs across tabs using storage events.

**Voice Search:**
Microphone icon in search bar opens voice input. Speech-to-text converts audio to query. Real-time transcription shows as speaking. Language detection automatic. Voice commands: "search for movies", "show action movies from 2020". Error handling for microphone permission denied or not supported.

### 9. USER AUTHENTICATION FLOWS

**Registration Flow:**
Email/password signup: email field with validation, password with strength meter, confirm password. Social login options: Google, Facebook, Apple with icons. Terms of service checkbox required. CAPTCHA after 3 failed attempts. Email verification sent immediately. Verification link valid 24 hours. Account creation redirects to onboarding.

**Login Flow:**
Email and password fields with show/hide password toggle. Remember me checkbox persists session 30 days. Forgot password link opens password reset flow. Social login options. Loading state during authentication. Error messages: "Invalid credentials", "Account locked", "Email not verified". Successful login redirects to previous page or dashboard.

**Password Reset Flow:**
Email input for account identification. Email sent with reset link valid 1 hour. Reset link opens page with new password input. Password requirements clearly listed. Confirmation password field validates match. Success redirects to login with success message. Expired link shows message with option to request new link.

**Two-Factor Authentication:**
Optional 2FA setup in settings: TOTP app (authenticator) or SMS. QR code for TOTP app setup. Backup codes generated (10 codes). 2FA required on login after setup: 6-digit code input. Remember device checkbox skips 2FA for 30 days. Lost device recovery via backup codes or support contact.

**Session Management:**
JWT tokens store in httpOnly cookie for security. Access token valid 15 minutes. Refresh token valid 7 days. Token refresh automatic before expiration using interceptor. Concurrent login limit: 3 devices, oldest session invalidated. Logout endpoint invalidates refresh token. Logout all devices option available.

**OAuth Integration:**
Google OAuth: requests email and profile scopes. Redirect to Google, then callback with code. Code exchanges for tokens on backend. User data creates or links account. Error handling: user cancels, missing permissions, network error. Account linking: email match links to existing account.

### 10. SOCIAL FEATURES IMPLEMENTATION

**Follow System:**
Follow button on user profiles toggles state. Optimistic update shows followed immediately. API failure reverts state with error toast. Following count updates reactively. Followers list modal shows all followers with avatars. Following list shows who user follows. Mutual follows indicated with special badge. Unfollow confirmation prevents accidents.

**Activity Feed:**
Feed shows: movies rated, reviews posted, lists created, users followed. Each activity type has distinct card design. User avatar and name link to profile. Movie mentions link to movie page. Timestamp shows relative time: "2 hours ago". Load more button or infinite scroll. Real-time updates via WebSocket (new activities appear with animation).

**Review System:**
Review modal: rating stars (1-5), optional text area with rich text editor. Multi-dimensional ratings: plot, acting, cinematography, soundtrack (each 1-5). Spoiler toggle warns readers. Character count shows (max 5000 characters). Preview before posting. Edit option available after posting. Delete confirmation prevents accidents.

**Review Interactions:**
Like button with heart icon toggles liked state. Like count shows next to button. Comment button opens nested comment thread. Share button opens share modal (Twitter, Facebook, copy link). Report button for inappropriate content. Edit history link shows all versions with timestamps.

**Lists Feature:**
Create list modal: name input (required), description textarea, privacy toggle (public/private). Add movies via search in modal. Drag to reorder movies in list. Personal notes per movie in list. Collaborative lists: invite users via email, permissions (view/edit). List sharing generates unique URL. Like and follow lists by other users.

**Notifications System:**
Notification bell icon in header with unread count badge. Dropdown shows recent notifications (last 10). Each notification: user avatar, action description, timestamp, mark read button. Notification types: new follower, review like, list followed, mention, reply. Click notification navigates to relevant page and marks read. Settings control notification preferences (email, push).

**Social Sharing:**
Share modal shows platforms: Twitter, Facebook, WhatsApp, copy link. Pre-filled text includes movie title and user's rating. OpenGraph meta tags optimize link previews. Twitter card with large image. Facebook share shows poster and description. Copy link button with clipboard icon, toast confirms copied.

### 11. RESPONSIVE DESIGN SYSTEM DETAILS

**Mobile Navigation:**
Hamburger menu icon (three lines) in header on mobile. Tap opens drawer from left with backdrop. Drawer contains: navigation links, user menu, theme toggle. Swipe right closes drawer. Backdrop tap closes drawer. Drawer width 280px (80% viewport max). Header remains fixed during scroll. Bottom tab bar on mobile for quick access (home, search, watchlist, profile).

**Touch Interactions:**
Touch targets minimum 44x44px ensuring easy tapping. Adequate spacing between targets (8px minimum) prevents mis-taps. Tap feedback: brief scale down (0.95) on active state. Long press triggers context menus. Swipe gestures: left/right on carousels, up/down for refresh/dismiss. Pinch zoom on images. Pull-to-refresh on main content areas.

**Responsive Typography:**
Heading sizes reduce 1-2 levels on mobile (H1 becomes H2 size). Line height increases on mobile for comfortable reading. Letter spacing adjusts for smaller screens. Font size minimum 14px on mobile. Adjustable text size respects user settings (browser zoom).

**Responsive Images:**
Poster images 160px width on mobile, 220px tablet, 280px desktop. Backdrop images use mobile-specific crops focusing on subject. Lazy loading essential on mobile for data savings. WebP format preferred with JPEG fallback. Loading="lazy" attribute on images below fold.

**Layout Breakpoints:**
320px (small mobile): single column, stacked components. 640px (mobile): 2-column grid, larger touch targets. 768px (tablet): 3-column grid, sidebar optional. 1024px (desktop): 4+ columns, sidebar visible. 1280px+ (large desktop): maximum 6 columns, increased spacing.

**Mobile-Specific Components:**
Bottom sheet modals instead of center modals on mobile. Pull indicator at bottom sheet top for dismissal. Swipeable tabs for easier navigation. Collapsible sections accordion-style saving space. Simplified navigation reducing options. Floating action button for primary action. Sticky footer with key actions always accessible.

**Performance on Mobile:**
Reduced animations on low-end devices detected via device memory API. Smaller images served to mobile browsers. Fewer items in initial page load. Lazy loading more aggressive on mobile. Service worker caches essential assets for offline. Progressive enhancement ensures base functionality without JavaScript.

**Orientation Handling:**
Portrait: content stacks vertically, single column. Landscape: content flows horizontally where appropriate, grid expands. Video player switches fullscreen automatically in landscape. Keyboard appearance adjusts layout pushing content up. Screen orientation lock available for video playback.

### 12. THEME SYSTEM IMPLEMENTATION

**Theme Detection:**
System preference detected using prefers-color-scheme media query. User preference overrides system saved in localStorage. Theme loads before paint preventing flash using blocking script. Theme class added to HTML element ('dark' or 'light'). CSS custom properties updated based on theme class.

**Theme Toggle:**
Toggle button in header shows sun/moon icon. Click cycles through: light → dark → system. System mode shows auto icon. Current theme saved immediately to localStorage. Theme applies instantly without page reload. All components reactive to theme changes. Smooth transition (300ms) on theme change for color properties.

**Light Mode Specifications:**
Background colors lighter: primary #FAFBFC, secondary #F3F4F6, tertiary #E5E7EB. Text colors inverted: primary #0A0E13 (dark), secondary #4B5563, tertiary #9CA3AF. Borders darker: 10-20% black instead of white. Shadows more prominent for definition. Glass effect uses black at low opacity. Accent colors maintain for consistency and brand recognition.

**Dark Mode Optimization:**
True blacks avoided using dark grays preventing OLED burn-in. Contrast ratios maintained meeting WCAG standards. Images don't need inversion. Videos maintain original colors. Code blocks use dark theme syntax highlighting. Chart colors adjusted for dark background visibility.

**Theme-Specific Assets:**
Logo: light variant for dark mode, dark variant for light mode. Icons: adjust stroke color based on theme. Illustrations: theme-specific versions where appropriate. Background patterns: opacity adjusted per theme. Marketing materials: separate light/dark versions.

**Accessibility in Theming:**
Both themes meet WCAG AA contrast requirements minimum. Focus indicators visible in both themes. Error states clearly visible regardless of theme. Disabled states properly indicated. Theme preference persists per user account. Respect prefers-contrast high for increased contrast mode.

This comprehensive specification now covers every aspect of the frontend implementation including state management, animations, accessibility, performance, error handling, loading states, forms, search, authentication, social features, responsive design, and theming - leaving no detail unaddressed for a production-ready implementation.

