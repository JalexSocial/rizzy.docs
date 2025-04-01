---
title: "Accessibility (A11y)"
description: "Learn about RizzyUI's commitment to accessibility and the features implemented to support users of assistive technologies."
summary: "Discover how RizzyUI incorporates accessibility best practices, including semantic HTML, ARIA attributes, keyboard navigation, and focus management, to create inclusive user interfaces."
date: 2024-07-28T10:30:00-05:00 # Adjust date as needed
lastmod: 2024-07-28T10:30:00-05:00 # Adjust date as needed
draft: false
menu:
  docs:
    parent: "concepts"
    identifier: "rizzyui-concepts-accessibility"
weight: 40
toc: true
seo:
  title: "Accessibility in RizzyUI | Rizzy Documentation"
  description: "Understand RizzyUI's approach to web accessibility (A11y), covering semantic HTML, ARIA roles and attributes, keyboard support, focus management, and color contrast."
---

## Accessibility (A11y) in RizzyUI: Building for Everyone

Creating web applications that are usable by everyone, regardless of their abilities or the assistive technologies they use, isn't just a good idea – it's essential. RizzyUI is designed with accessibility (often abbreviated as A11y) as a core consideration. While perfect accessibility often requires careful implementation specific to your application's context, RizzyUI components aim to provide a solid, accessible foundation out of the box.

This page outlines some of the key accessibility features and practices incorporated into RizzyUI.

### [Semantic HTML: The Foundation](#semantic-html-the-foundation)

Whenever possible, RizzyUI components render standard, semantic HTML elements. This means using:

*   `<button>` for interactive controls that perform actions.
*   `<a>` for navigation links.
*   `<input>`, `<label>`, `<select>`, etc., for form elements.
*   `<nav>`, `<aside>`, `<main>`, `<article>` for page structure (in layout components like `<Sidebar>`).
*   Headings (`<h1>` - `<h4>` via `<Heading>`) used appropriately.

Using the correct semantic element provides inherent accessibility benefits, as screen readers and browsers understand their purpose and intended behavior.

### [ARIA Attributes: Adding Clarity](#aria-attributes-adding-clarity)

Sometimes, standard HTML isn't enough to convey the state or purpose of complex UI components. That's where ARIA (Accessible Rich Internet Applications) attributes come in. RizzyUI components leverage ARIA attributes where appropriate:

*   **`role`:** Defines the purpose of an element (e.g., `role="alert"`, `role="dialog"`, `role="menu"`, `role="tab"`).
*   **`aria-label` / `aria-labelledby`:** Provides accessible names for elements, especially important for icon-only buttons or complex controls. Many components have parameters like `AriaLabel` or automatically link labels.
*   **`aria-describedby`:** Links elements to descriptions (e.g., associating form help text with an input).
*   **`aria-expanded`:** Indicates whether a collapsible element (like an Accordion section or Dropdown) is currently open or closed.
*   **`aria-controls`:** Links a control (like a Tab) to the element it manages (the TabPanel).
*   **`aria-current`:** Indicates the currently active item in a set (e.g., the active BreadcrumbItem).
*   **`aria-hidden`:** Hides decorative elements (like icons that purely supplement text) from screen readers.

These attributes help assistive technologies understand the structure, state, and purpose of RizzyUI components, providing a better experience for users.

### [Keyboard Navigation: Beyond the Mouse](#keyboard-navigation-beyond-the-mouse)

Not everyone uses a mouse. RizzyUI components are designed to be navigable and operable using only a keyboard:

*   **Logical Tab Order:** Components render elements in a way that generally follows a logical tab order.
*   **Focusable Elements:** Buttons, links, form inputs, and interactive elements are naturally focusable.
*   **Specific Key Interactions:** Interactive components managed by Alpine.js often implement standard keyboard patterns:
    *   **Dropdowns/Menus:** Arrow keys (Up/Down) navigate items, Enter/Space selects, Escape closes.
    *   **Tabs:** Arrow keys (Left/Right) switch tabs, Enter/Space activates.
    *   **Accordions:** Enter/Space toggles the focused section.
    *   **Modals/Dialogs:** Escape closes the dialog.
*   **Focus Indicators:** Components use Tailwind's `focus-visible:` utilities to provide clear visual indicators when an element receives keyboard focus, without cluttering the UI for mouse users.

### [Focus Management: Guiding the User](#focus-management-guiding-the-user)

Proper focus management is crucial, especially in dynamic interfaces:

*   **Focus Trapping:** Components like Modals and sometimes Dropdowns (when opened via keyboard) implement focus trapping. This means when the component is open, the Tab key cycles only through the interactive elements *within* that component, preventing focus from accidentally escaping to the background page content.
*   **Returning Focus:** When a component like a Modal or Dropdown is closed, focus is typically returned to the element that originally opened it, providing a seamless experience.

### [Color Contrast and Theming](#color-contrast-and-theming)

RizzyUI's theming system uses CSS variables. While the default themes (`ArcticTheme`, etc.) are designed with accessibility considerations in mind regarding contrast ratios between text (`--color-on-surface`) and backgrounds (`--color-surface`), **it is crucial to verify contrast ratios if you create a custom theme.**

*   **Default Themes:** Aim for WCAG AA compliance for text contrast.
*   **Custom Themes:** Use online contrast checkers or browser developer tools to ensure your chosen color combinations meet accessibility standards (generally 4.5:1 for normal text, 3:1 for large text).

### [Screen Reader Text and Labels](#screen-reader-text-and-labels)

*   **`sr-only`:** Decorative icons or elements that don't add information for screen reader users are sometimes hidden using Tailwind's `sr-only` class equivalent where appropriate, or marked with `aria-hidden="true"`.
*   **Labels:** Components often have parameters like `AriaLabel` or `AssistiveLabel` to provide clear, concise descriptions for controls, especially icon-only buttons (`<DarkmodeToggle />`). Form components (`<TextField>`, `<CheckboxGroupField>`) emphasize the importance of using `<FieldLabel>` for proper association.

### [Ongoing Commitment](#ongoing-commitment)

Accessibility is an ongoing process. RizzyUI aims to follow best practices, but the specific context of your application matters. We encourage developers to test their applications with accessibility tools and provide feedback or report issues if they encounter A11y problems with RizzyUI components.

By building on a foundation of semantic HTML, ARIA attributes, keyboard support, and careful focus management, RizzyUI strives to help you create web applications that are usable and enjoyable for the widest possible audience.
