---
title: "Theming"
description: "Learn how to manage the visual appearance of your RizzyUI application using themes, CSS variables, and the RizzyThemeProvider."
summary: "Explore RizzyUI's theming system, understand how CSS variables power light/dark modes, see built-in themes, and learn how to create and apply your own custom themes."
date: 2024-07-28T10:20:00-05:00 # Adjust date as needed
lastmod: 2024-07-28T10:20:00-05:00 # Adjust date as needed
draft: false
menu:
  docs:
    parent: "rizzyuiconcepts"
    identifier: "rizzyui-concepts-theming"
weight: 20
toc: true
seo:
  title: "Theming in RizzyUI | Rizzy Documentation"
  description: "Master RizzyUI theming: understand the role of RizzyThemeProvider, CSS design tokens, light/dark modes, built-in themes, and how to create custom themes."
---

## Theming in RizzyUI: Controlling the Look and Feel

So, you've seen how RizzyUI uses Tailwind classes that map to CSS variables (Design Tokens) for styling ([Styling Philosophy](../styling.md)). Now, let's talk about how you actually *control* the values of those variables to change the overall appearance of your application – that's **Theming**.

Theming in RizzyUI allows you to define consistent colors, borders, and radii across all components, easily switch between light and dark modes, and even create entirely custom visual styles.

### [The Conductor: `<RizzyThemeProvider />`](#the-conductor-rizzythemeprovider-)

The heart of the theming system is the `<RizzyThemeProvider />` component. You absolutely **must** place this component **inside the `<head>`** section of your main application layout (e.g., `AppLayout.razor` or `_Layout.cshtml` if integrating differently).

```html {title="AppLayout.razor (Example Head)"}
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My RizzyUI App</title>
    <base href="/" />
    <link rel="stylesheet" href="css/app.css" /> @* Your compiled Tailwind CSS *@

    <!-- Crucial: Place Theme Provider Here -->
    <RizzyThemeProvider />

    <link rel="icon" type="image/png" href="favicon.png" />
    @* Other head elements *@
</head>
```

**Why in the `<head>`?** The theme provider works by injecting a `<style>` block containing CSS Custom Property definitions (like `--color-surface: oklch(0.98 0.01 100);`). These variables need to be defined *before* the browser starts rendering the body and applying styles to your components. Placing it in the `<head>` ensures this.

### [What Does the Theme Provider Do?](#what-does-the-theme-provider-do)

1.  **Selects the Theme:** It determines which theme to use:
    *   If you pass a theme instance via the `Theme` parameter (`<RizzyThemeProvider Theme="@MyCustomTheme" />`), it uses that.
    *   Otherwise, it checks if a default theme was set during service configuration (`AddRizzyUI(config => config.DefaultTheme = ...)`).
    *   If neither is specified, it falls back to `RizzyTheme.Default` (which is currently `ArcticTheme`).
2.  **Generates CSS Variables:** It takes the chosen theme's definitions (colors, border radius, etc.) for both light and dark modes.
3.  **Injects Styles:** It creates a `<style>` tag containing CSS rules that define the variables within the `:root` scope for light mode and within `:root:where(.dark, .dark *)` for dark mode.

Here's a simplified example of the CSS it might generate (using hypothetical Oklch values for `ArcticTheme`):

```css
:root {
  --color-surface: oklch(0.98 0.01 100); /* Light Surface */
  --color-on-surface: oklch(0.4 0.03 260); /* Light Text */
  --color-primary: oklch(0.5 0.15 265); /* Light Primary */
  --color-on-primary: oklch(0.98 0.01 100); /* Light Text on Primary */
  /* ... other light mode variables ... */
  --border-radius: 6px;
  --border-width: 1px;

  /* Code Highlighting - Light */
  --highlight-bg: oklch(0.95 0.01 100);
  /* ... other highlight vars ... */
}

/* Dark Mode Overrides */
:root:where(.dark, .dark *) {
  --color-surface: oklch(0.15 0.02 260); /* Dark Surface */
  --color-on-surface: oklch(0.85 0.02 260); /* Dark Text */
  --color-primary: oklch(0.6 0.18 265); /* Dark Primary */
  --color-on-primary: oklch(0.98 0.01 100); /* Dark Text on Primary */
  /* ... other dark mode variables ... */

  /* Code Highlighting - Dark */
  --highlight-bg: oklch(0.2 0.02 260);
  /* ... other highlight vars ... */
}
```

### [Light and Dark Mode Magic](#light-and-dark-mode-magic)

RizzyUI uses the standard Tailwind approach for dark mode. The `<RizzyThemeProvider />` includes a small inline script (CSP nonce-compatible) that checks:

1.  If the user has explicitly set a preference in `localStorage` (`'light'` or `'dark'`).
2.  If not, it checks the operating system's preference (`prefers-color-scheme: dark`).
3.  Based on this, it adds or removes the `dark` class to the `<html>` element *before* the page renders.

Because the theme provider sets up CSS variables for both light (`:root`) and dark (`:root:where(.dark, .dark *)`), the browser automatically applies the correct set of variable values based on the presence of the `dark` class on the `<html>` tag. Components styled with semantic classes like `bg-surface` or `text-primary` just work™ in both modes.

### [Using Built-in Themes](#using-built-in-themes)

RizzyUI comes with a few themes ready to go:

*   `RizzyTheme.ArcticTheme` (The default)
*   `RizzyTheme.HighContrastTheme`
*   `RizzyTheme.ModernTheme`
*   `RizzyTheme.NewsTheme`

You can apply them easily:

```csharp
// In Program.cs
builder.Services.AddRizzyUI(config =>
{
    config.DefaultTheme = RizzyTheme.ModernTheme;
});

// OR directly on the provider
<RizzyThemeProvider Theme="@RizzyTheme.ModernTheme" />
```

### [Creating Your Own Theme](#creating-your-own-theme)

Want a unique look? Create a class that inherits from `RizzyTheme` and set the properties within its constructor. You'll primarily be setting the `Light` and `Dark` properties (which are `RizzyThemeVariant` objects) and the shared status colors (`Danger`, `Info`, etc.).

```csharp {title="MyCustomTheme.cs"}
using RizzyUI;

public class MyCustomTheme : RizzyTheme
{
    // Constructor takes a display name and a code name (used for CSS class if needed)
    public MyCustomTheme() : base("My Awesome Theme", "mytheme")
    {
        // --- Light Mode ---
        Light = new RizzyThemeVariant
        {
            Surface = Colors.Stone.L100, // Use RizzyUI.Colors helper
            OnSurface = Colors.Stone.L800,
            OnSurfaceStrong = Colors.Stone.L950,
            OnSurfaceMuted = Colors.Stone.L500,
            SurfaceAlt = Colors.Stone.L200,
            SurfaceTertiary = Colors.Stone.L300,
            OnSurfaceTertiary = Colors.Stone.L600,

            Primary = Colors.Teal.L700,
            OnPrimary = Colors.White,
            Secondary = Colors.Amber.L600,
            OnSecondary = Colors.Black,

            Outline = Colors.Stone.L400,
            OutlineStrong = Colors.Stone.L600,

            Code = CodeThemes.Github // Choose a code theme
        };

        // --- Dark Mode ---
        Dark = new RizzyThemeVariant
        {
            Surface = Colors.Stone.L900,
            OnSurface = Colors.Stone.L300,
            OnSurfaceStrong = Colors.Stone.L100,
            OnSurfaceMuted = Colors.Stone.L500,
            SurfaceAlt = Colors.Stone.L800,
            SurfaceTertiary = Colors.Stone.L700,
            OnSurfaceTertiary = Colors.Stone.L400,

            Primary = Colors.Teal.L500,
            OnPrimary = Colors.Black,
            Secondary = Colors.Amber.L400,
            OnSecondary = Colors.Black,

            Outline = Colors.Stone.L700,
            OutlineStrong = Colors.Stone.L500,

            Code = CodeThemes.Dracula // Choose a dark code theme
        };

        // --- Shared Status Colors ---
        Danger = Colors.Red.L600;
        OnDanger = Colors.White;
        Info = Colors.Sky.L600;
        OnInfo = Colors.White;
        Warning = Colors.Orange.L500;
        OnWarning = Colors.Black;
        Success = Colors.Green.L600;
        OnSuccess = Colors.White;

        // --- Shared Borders/Radius ---
        BorderWidth = "2px";
        BorderRadius = "8px"; // Slightly more rounded corners
    }
}
```

Then, use `MyCustomTheme` like any built-in theme:

```csharp
// Program.cs
builder.Services.AddRizzyUI(config =>
{
    config.DefaultTheme = new MyCustomTheme();
});
```

```html
<!-- OR -->
<RizzyThemeProvider Theme="@(new MyCustomTheme())" />
```

### [Conclusion](#conclusion)

RizzyUI's theming system, powered by the `<RizzyThemeProvider />` and CSS custom properties, provides a flexible and maintainable way to control your application's appearance. By defining semantic colors and other design tokens within a theme, you can ensure consistency, easily support light/dark modes, and create custom looks without modifying individual component styles. Remember to place the provider in your `<head>`, and choose between configuring a default theme or applying one directly.
