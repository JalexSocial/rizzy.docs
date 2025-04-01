---
title: "Styling Philosophy"
description: "Learn how RizzyUI components are styled using Tailwind CSS utility classes and design tokens, and how you can customize their appearance."
summary: "Understand RizzyUI's utility-first styling approach with Tailwind CSS, the use of CSS custom properties (design tokens) for theming, and how to safely add your own custom styles using TwMerge."
date: 2024-07-28T10:15:00-05:00 # Adjust date as needed
lastmod: 2024-07-28T10:15:00-05:00 # Adjust date as needed
draft: false
menu:
  docs:
    parent: "concepts"
    identifier: "rizzyui-concepts-styling"
weight: 10
toc: true
seo:
  title: "Styling Philosophy in RizzyUI | Rizzy Documentation"
  description: "Explore how RizzyUI uses Tailwind CSS utilities and design tokens for consistent styling, and learn how to merge custom classes effectively."
---

## Styling in RizzyUI: Tailwind First, Tokens Underneath

Styling UI components can sometimes feel like wrestling a beast. One library uses BEM, another uses CSS Modules, and suddenly you're juggling multiple methodologies. RizzyUI takes a clear stance: we embrace **Tailwind CSS** and its **utility-first** approach.

### [Why Tailwind CSS?](#why-tailwind-css)

If you've used Tailwind, you know the drill: instead of writing custom CSS like `.my-button { background-color: blue; padding: 8px 16px; }`, you apply utility classes directly in your markup: `<button class="bg-blue-500 px-4 py-2">`.

RizzyUI uses this approach internally for all its components. Why?

*   **Consistency:** All components are built using the same system.
*   **Customization:** It's easier to override or extend styles by adding or changing Tailwind classes.
*   **No CSS Bloat:** Tailwind generates only the CSS classes you actually use in your project (including those used by RizzyUI components, assuming your `tailwind.config.js` is set up correctly).
*   **Direct Mapping:** Changes in the component's markup directly reflect the styling, making debugging easier.

### [Design Tokens: The Power of CSS Variables](#design-tokens-the-power-of-css-variables)

Okay, so we use Tailwind classes. But how do we handle theming (like light/dark mode or different color schemes)? If we hardcoded `bg-blue-500` everywhere, changing the primary color would be a nightmare.

That's where **Design Tokens** (implemented as CSS Custom Properties, aka CSS Variables) come in. RizzyUI defines a set of semantic variables that control the appearance of components. The `<RizzyThemeProvider />` (discussed more in [Theming](./theming.md)) injects the *values* for these variables based on the selected theme.

Tailwind classes in RizzyUI components often reference these variables instead of fixed values (e.g., `bg-primary` uses `var(--color-primary)`). When the theme or mode changes, the variable values update, and components styled with these semantic classes automatically adapt.

Here's a breakdown of the core design tokens used by RizzyUI:

| CSS Variable                 | Description                                                          | Example Tailwind Usage        |
| :--------------------------- | :------------------------------------------------------------------- | :---------------------------- |
| **Surface & Text Colors**    |                                                                      |                               |
| `--color-surface`            | The primary background color for most components and page areas.     | `bg-surface`                  |
| `--color-on-surface`         | Default text color used on `--color-surface`.                        | `text-on-surface`             |
| `--color-on-surface-strong`  | Stronger/higher contrast text color on `--color-surface` (e.g., headings). | `text-on-surface-strong`  |
| `--color-on-surface-muted`   | Dimmed/less important text color on `--color-surface` (e.g., captions). | `text-on-surface-muted`   |
| `--color-surface-alt`        | An alternate background color for contrast (e.g., card headers, hover). | `bg-surface-alt`              |
| `--color-surface-tertiary`   | A tertiary background, often used for code blocks or distinct sections. | `bg-surface-tertiary`         |
| `--color-on-surface-tertiary`| Text color used on `--color-surface-tertiary`.                     | `text-on-surface-tertiary`    |
| **Brand/Accent Colors**      |                                                                      |                               |
| `--color-primary`            | The main brand or primary action color.                              | `bg-primary`, `text-primary`  |
| `--color-on-primary`         | Text/icon color used on `--color-primary` background.                | `text-on-primary`             |
| `--color-secondary`          | The secondary brand or action color.                                 | `bg-secondary`, `text-secondary`|
| `--color-on-secondary`       | Text/icon color used on `--color-secondary` background.              | `text-on-secondary`           |
| **Outline/Border Colors**    |                                                                      |                               |
| `--color-outline`            | Default color for borders, dividers, and outlines.                   | `border-outline`              |
| `--color-outline-strong`     | A stronger/more prominent border color.                              | `border-outline-strong`       |
| **Status Colors**            |                                                                      |                               |
| `--color-danger`             | Color indicating errors or destructive actions.                      | `bg-danger`, `text-danger`    |
| `--color-on-danger`          | Text/icon color used on `--color-danger` background.                 | `text-on-danger`              |
| `--color-info`               | Color indicating informational messages.                             | `bg-info`, `text-info`        |
| `--color-on-info`            | Text/icon color used on `--color-info` background.                   | `text-on-info`                |
| `--color-warning`            | Color indicating warnings or caution.                                | `bg-warning`, `text-warning`  |
| `--color-on-warning`         | Text/icon color used on `--color-warning` background.                | `text-on-warning`             |
| `--color-success`            | Color indicating success or confirmation.                            | `bg-success`, `text-success`  |
| `--color-on-success`         | Text/icon color used on `--color-success` background.                | `text-on-success`             |
| **Layout Tokens**            |                                                                      |                               |
| `--borderWidth`              | Default border thickness used by components (e.g., "1px").           | `border` (uses width)         |
| `--borderRadius`             | Default corner roundness used by components (e.g., "6px").           | `rounded-theme`               |
| **Code Highlighting**        | (Used internally by `<Markdown>`/`<CodeViewer>`)                     | (Within `.prose` styles)      |
| `--highlight-bg`             | Background color for code blocks.                                    | `prose ... pre`               |
| `--highlight-color`          | Default text color within code blocks.                               | `prose ... code`              |
| `--highlight-comment`        | Color for code comments.                                             | `.hljs-comment`               |
| `--highlight-keyword`        | Color for language keywords (e.g., `public`, `class`, `if`).         | `.hljs-keyword`               |
| `--highlight-attribute`      | Color for attributes (e.g., HTML attributes, C# attributes).         | `.hljs-attribute`             |
| `--highlight-symbol`         | Color for symbols, constants, or tags.                               | `.hljs-symbol`, `.hljs-tag`   |
| `--highlight-namespace`      | Color for namespaces or module names.                                | `.hljs-namespace`             |
| `--highlight-variable`       | Color for variables.                                                 | `.hljs-variable`              |
| `--highlight-literal`        | Color for literals (e.g., `true`, `false`, `null`, numbers).         | `.hljs-literal`, `.hljs-number`|
| `--highlight-punctuation`    | Color for punctuation (e.g., brackets, commas).                      | `.hljs-punctuation`           |
| `--highlight-deletion`       | Color indicating deleted lines in diffs.                             | `.hljs-deletion`              |
| `--highlight-addition`       | Color indicating added lines in diffs.                               | `.hljs-addition`              |

**Note on Light/Dark Mode:** The `<RizzyThemeProvider />` defines these variables within `:root` for light mode and redefines them within `:root:where(.dark, .dark *)` for dark mode. This allows Tailwind utility classes like `bg-surface` to automatically adapt based on whether the `dark` class is present on the `<html>` element.

The **`<RizzyThemeProvider />`** component (discussed more in [Theming](./theming.md)) injects the *values* for these variables into your page's `:root`.

Then, Tailwind classes in RizzyUI components often reference these variables instead of fixed values. For example, a primary button's class might internally resolve to something like `bg-[var(--color-primary)] text-[var(--color-on-primary)]`.

**What does this mean for you?** You don't usually need to worry about the variables directly. You just use semantic Tailwind classes configured in RizzyUI's theme system, like `bg-primary`, `text-on-surface`, `rounded-theme`, `border-outline`. When the theme changes (e.g., switching to dark mode), the *values* of the CSS variables update, and all components styled with those semantic classes automatically reflect the new theme!

### [Customizing Styles: Adding Your Own Classes](#customizing-styles-adding-your-own-classes)

Since RizzyUI components render standard HTML elements, you can always add your own Tailwind classes (or even custom CSS classes) using the `class` attribute:

```html
<Button Variant="ButtonVariant.Primary" class="mt-4 !py-3 custom-shadow">
  My Custom Button
</Button>
```

**But wait, won't my classes conflict with the component's internal classes?** Good question! RizzyUI components internally use a utility called **TwMerge** (Tailwind Merge).

*   **What is TwMerge?** It's a small utility that intelligently merges multiple Tailwind class strings, resolving conflicts based on Tailwind's logic. For example, if a component internally has `px-4` and you add `px-6`, `TwMerge` ensures `px-6` wins because it's the last specified padding utility for the x-axis. If you add `mt-4` and the component has `py-2`, both are kept because they apply to different properties (margin-top vs. padding-y).
*   **How RizzyUI uses it:** The base `RizzyComponent` automatically merges any class you provide via `AdditionalAttributes` (which captures the `class` attribute) with the component's internal base and variant styles.

This means you can usually add your own utility classes (like margins `m-4`, specific widths `w-full`, or even overrides like `!py-3` for important padding) without needing to manually figure out which internal classes to remove. `TwMerge` handles the sensible merging for you.

{{< callout context="tip" title="Tip" icon="info-circle" >}}
While you *can* override base styles (like `bg-primary`) by adding your own background class (e.g., `bg-red-500`), it's generally better to customize colors through the [Theming](./theming.md) system for consistency. Use the `class` attribute primarily for layout adjustments (margins, padding, width, flex/grid) or minor style tweaks.
{{< /callout >}}

### [Conclusion](#conclusion)

RizzyUI's styling is built on the foundation of **Tailwind CSS** for utility-first application and **CSS Custom Properties (Design Tokens)** for powerful, consistent theming. Components define their base styles and variants using semantic tokens (like `bg-primary`), which are resolved by the theme provider. You can easily customize layout or add specific tweaks by passing standard Tailwind classes via the `class` attribute, and `TwMerge` intelligently handles potential conflicts. This approach aims for a balance between pre-built consistency and flexible customization.
