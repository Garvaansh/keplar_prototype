# Exoplanet AI Analyzer - Design Guidelines

## Design Approach

**Selected Approach**: Custom Thematic Design with Data Visualization Focus
**Justification**: This scientific tool requires both strong visual identity (space/astronomy theme) and exceptional data clarity. We'll enhance the cosmic aesthetic while ensuring charts and controls remain highly functional.

**Key Design Principles**:
1. **Cosmic Immersion**: Deep space atmosphere with layered depth and stellar elements
2. **Data Clarity First**: Visual hierarchy that prioritizes information comprehension
3. **Responsive Feedback**: Immediate visual response to user interactions
4. **Scientific Precision**: Clean, accurate data representation with professional polish

## Core Design Elements

### A. Color Palette

**Dark Mode Foundation** (Primary):
- **Background Deep Space**: 8 8% 6% (rich dark blue-black)
- **Surface Panels**: 220 15% 12% (elevated dark slate)
- **Elevated Cards**: 220 18% 15% (lighter panels for hierarchy)

**Accent & Status Colors**:
- **Primary Cyan Glow**: 186 100% 50% (electric cyan for highlights)
- **Confirmed (Success)**: 142 71% 45% (vibrant green)
- **Candidate (Warning)**: 38 92% 50% (bright amber)
- **False Positive (Error)**: 0 84% 60% (strong red)
- **Secondary Purple**: 270 70% 60% (nebula accent, use sparingly)

**Text Hierarchy**:
- **Primary Text**: 210 40% 98% (near white)
- **Secondary Text**: 217 33% 70% (soft blue-gray)
- **Tertiary/Labels**: 215 20% 55% (muted gray-blue)

### B. Typography

**Font Stack**:
- **Primary**: Inter (UI elements, data, labels)
- **Display**: Poppins (headings, emphasis)
- **Monospace**: JetBrains Mono via Google Fonts (numerical data, coordinates)

**Type Scale**:
- **Hero/H1**: text-5xl/6xl font-poppins font-bold
- **Section Headers**: text-3xl/4xl font-poppins font-semibold
- **Card Titles**: text-xl/2xl font-poppins font-medium
- **Body**: text-base font-inter
- **Data Labels**: text-sm font-inter font-medium
- **Numerical Data**: text-lg font-mono tracking-wide

### C. Layout System

**Spacing Primitives**: Use Tailwind units of 2, 4, 6, 8, 12, 16, 24
- **Component Padding**: p-6 to p-8 for cards
- **Section Spacing**: gap-8 to gap-12 for grids
- **Page Margins**: px-4 md:px-8 lg:px-16

**Grid Structure**:
- **Dashboard Layout**: Grid with sidebar (280px) + main content area
- **Card Grid**: grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6
- **Chart Containers**: Full width with max-w-7xl constraint

### D. Component Library

**Enhanced Controls**:
- **Parameter Sliders**: Custom styled with glowing track, large thumb with value tooltip, gradient fill showing current value
- **Range Inputs**: Track shows gradient from min (dark) to max (cyan glow), active thumb has pulsing shadow-glow effect
- **Buttons**: Solid fills for primary actions with glow hover states, outline variants for secondary with backdrop-blur

**Visualization Cards**:
- **Chart Containers**: Backdrop-blur glass effect (bg-space-gray/30 backdrop-blur-xl), border with subtle glow (border border-cyan-500/20)
- **Data Panels**: Elevated cards with shadow-2xl, gradient borders using before/after pseudo-elements
- **Status Indicators**: Large classification badges with icon, animated glow pulse, and confidence bar

**Navigation & Headers**:
- **Top Bar**: Fixed header with blur background, logo left, status indicators right
- **Parameter Panel**: Sticky sidebar with scrollable controls, section dividers with gradient lines

**Advanced Chart Styling**:
- **Light Curve**: Gradient area fill (from cyan to transparent), glowing line stroke, animated data points
- **Feature Importance**: Horizontal bars with gradient fills, icons for each feature, percentage labels
- **Planet Stats**: Radial progress rings for key metrics, with animated fills and center values

### E. Visual Effects & Animations

**Background Enhancements**:
- **Starfield**: Animated CSS background with multiple layers of twinkling stars (small, medium, large particles)
- **Nebula Gradient**: Subtle animated radial gradient overlay with purple/cyan hues, 30% opacity
- **Grid Pattern**: Faint coordinate grid lines (1px, 5% opacity) for scientific aesthetic

**Interactive Animations**:
- **Hover States**: Scale-105 transform, brightness increase, glow intensity up
- **Parameter Changes**: Smooth 300ms transitions on all value updates
- **Classification Update**: 500ms fade transition with scale-in effect for new predictions
- **Chart Animations**: Stagger entrance animations for data points, smooth curve interpolation

**Glow & Shadow System**:
- **Card Glow**: Multi-layer box-shadow with matching color and cyan base
- **Text Glow**: text-shadow for headings and important values
- **Button Glow**: Animated shadow spread on hover
- **Data Point Glow**: SVG filter for chart elements

## Images & Visual Assets

**No hero image needed** - this is a dashboard/tool application, not a landing page. Instead, implement:

1. **Background Texture**: Abstract space photography as subtle background (20% opacity), showing deep field stars or nebula
2. **Icon System**: Use Lucide React icons throughout - Telescope, Orbit, Zap (for AI), TrendingUp, Activity for various sections
3. **Placeholder Graphics**: For "no data" states, use cosmic illustrations (rocket, satellite) with encouraging copy

## Responsive Behavior

**Breakpoints**:
- **Mobile (< 768px)**: Single column, collapsible parameter panel, stacked charts
- **Tablet (768-1024px)**: Two-column grid, sliding drawer for controls
- **Desktop (> 1024px)**: Full sidebar + multi-column content, side-by-side comparisons

**Touch Optimization**:
- Slider thumbs: min-h-12 min-w-12 for easy touch
- Buttons: min-h-11 with adequate spacing (gap-4)
- Charts: Tap-to-highlight for data points

## Micro-Interactions

1. **Slider Interaction**: Real-time value preview above thumb, haptic-style snap to significant values
2. **Prediction Badge**: Pulsing glow when classification changes, confidence bar fills with animation
3. **Chart Tooltips**: Backdrop-blur card with detailed metrics, arrow pointer, fade-in on hover
4. **Loading States**: Shimmer effect on cards, animated dots for AI processing indicator