# Student Attendance Viewer - Design Guidelines

## Design Approach: Material Design System

**Rationale:** This is a utility-focused, information-dense application where clarity and efficiency are paramount. Material Design provides excellent patterns for dashboards, data display, and mobile responsiveness - perfect for students checking attendance on various devices.

**Key Principles:**
- Data clarity over decoration
- Mobile-first responsive design
- Instant information hierarchy
- Minimal cognitive load

---

## Typography

**Font Family:** Roboto (via Google Fonts CDN)

**Hierarchy:**
- Page titles: `text-3xl font-medium` (Student Dashboard, Login)
- Section headers: `text-xl font-medium` (Attendance Summary, Subject Details)
- Subject names: `text-lg font-normal`
- Data labels: `text-sm font-medium uppercase tracking-wide`
- Body text: `text-base font-normal`
- Attendance percentages: `text-2xl font-semibold` (prominent display)
- Helper text: `text-sm font-normal`

---

## Layout System

**Spacing Primitives:** Tailwind units of 2, 4, 6, and 8
- Component padding: `p-4` to `p-6`
- Section margins: `mb-6` to `mb-8`
- Card spacing: `space-y-4`
- Grid gaps: `gap-4`

**Container Structure:**
- Login page: `max-w-md mx-auto` (centered, compact)
- Dashboard: `max-w-5xl mx-auto px-4` (readable width with breathing room)
- Mobile padding: `px-4 py-6`
- Desktop padding: `px-6 py-8`

**Responsive Breakpoints:**
- Mobile-first approach (base styles for mobile)
- Tablet: `md:` breakpoint for 2-column grids
- Desktop: `lg:` breakpoint for enhanced spacing

---

## Component Library

### Login Page
**Structure:** Centered card on clean background
- Card with elevation shadow (`shadow-lg rounded-lg`)
- Logo/app title at top
- Two input fields (Student ID, Password) stacked vertically
- Full-width primary button
- Spacing: `space-y-4` between elements
- Form width: `w-full` within `max-w-md` container

### Dashboard Layout
**Header:**
- Student name/ID display: `text-lg font-medium`
- Logout button: top-right corner, text button style
- Padding: `p-4` on mobile, `p-6` on desktop

**Attendance Summary Card:**
- Overall attendance percentage: Large, prominent display (`text-4xl font-bold`)
- Status indicator below percentage
- Card design: `rounded-lg shadow-md p-6`
- Position: Top of dashboard, full-width

**Subject Cards Grid:**
- Grid layout: `grid grid-cols-1 md:grid-cols-2 gap-4`
- Each card contains:
  - Subject name (left-aligned, `font-medium`)
  - Attendance percentage (right-aligned, large)
  - Progress bar visual (horizontal bar showing percentage)
  - Classes attended/total below bar (`text-sm`)
- Card styling: `rounded-lg shadow-md p-4 md:p-6`

### Form Inputs
- Height: `h-12` for comfortable touch targets
- Border radius: `rounded-md`
- Padding: `px-4`
- Label positioning: Above input with `mb-2`
- Input states: Clear focus ring, no hover effects needed

### Buttons
- Primary button: `h-12 rounded-md px-6 font-medium`
- Full-width on mobile, auto-width on desktop where appropriate
- Login button: Full-width
- Logout button: Auto-width, minimal style

### Progress Bars
- Height: `h-2`
- Border radius: `rounded-full`
- Fill animation: Smooth transition
- Container: Full-width with background track

---

## Data Display Patterns

**Attendance Percentage Display:**
- Large numbers for quick scanning
- Color-coded context (Material Design semantic colors)
- Percentage symbol included
- Decimal precision: One decimal place (e.g., 85.5%)

**Subject List:**
- Alphabetical ordering
- Consistent card heights
- Hover state: Subtle elevation increase (`hover:shadow-lg transition-shadow`)

**Empty States:**
- When no attendance data: Centered message with icon placeholder
- Clear, friendly messaging

---

## Page-Specific Guidelines

### Login Page
- Clean, uncluttered design
- Centered vertically and horizontally
- Padding around card: `p-4` minimum
- Background: Subtle, non-distracting

### Dashboard Page
- Information hierarchy: Overall → Individual subjects
- Scannable layout for quick checks
- No unnecessary scroll on desktop for 4-6 subjects
- Mobile: Natural vertical scroll

---

## Icons
Use **Material Icons** (via CDN) for:
- Lock icon (login page, password field)
- Person icon (login page, student ID field)
- Checkmark/warning icons (attendance status indicators)
- Logout icon (header button)

---

## Animations
**Minimal, purposeful only:**
- Progress bar fill: Smooth transition on load
- Card hover: Subtle shadow elevation
- Page transitions: None (instant navigation)
- Form feedback: Simple fade-in for error messages

---

## Images
**No hero image required.** This is a functional dashboard - focus on data clarity.

**Optional branding:**
- Small school/institution logo in login card header (`h-12` to `h-16`)
- Favicon for browser tab

---

## Accessibility
- All form inputs have associated labels
- Sufficient contrast for all text (especially attendance percentages)
- Focus indicators visible and clear
- Touch targets minimum 44x44px (already covered with `h-12` inputs/buttons)
- Semantic HTML structure (proper heading hierarchy)