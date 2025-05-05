---
title: "RizzyUI Overview"
description: ""
summary: ""
date: 2025-04-01T08:30:55-04:00
lastmod: 2025-04-01T08:30:55-04:00
draft: false
weight: 5
toc: true
menu:
  docs:
    parent: "rizzyui" # Assuming a setup sub-section
    identifier: "rizzyui-overview"
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

RizzyUI is a component library for applications using Rizzy and HTMX. It provides pre-built Blazor components (like buttons, forms, cards) styled with Tailwind CSS and using Alpine.js for client-side interactions, designed to work within Rizzy's server-side rendering model and HTMX's partial update mechanism.

## What Are We Trying To Achieve Here?

Why build *another* component library? RizzyUI focuses on a specific niche with these goals in mind:

1.  **Great Developer Experience:** Provide components that feel intuitive to use within a SSR context. Reduce the boilerplate needed to build common UI patterns.
2.  **Visual Consistency & Theming:** Use a robust theming system built on CSS custom properties (design tokens). Easily switch between light/dark modes or even create your own themes that apply consistently across all components.
3.  **Targeted Interactivity:** Handle common client-side interactions (toggles, dropdowns, etc.) efficiently using Alpine.js, keeping the component footprint small and avoiding the need for heavier client-side frameworks for simple UI behaviors.
4.  **SSR & HTMX Compatibility:** Ensure components render correctly on the server and function as expected when subjected to HTMX partial updates and swaps.

## [How Does RizzyUI Fit with Rizzy and HTMX?](#how-does-rizzyui-fit-with-rizzy-and-htmx)

It helps to understand the roles:

*   **ASP.NET Core (MVC):** Your application's backbone, handling routing, logic, data access, security.
*   **Rizzy:** The bridge that allows your ASP.NET Core app to render **Blazor Components** server-side as HTML responses with HTMX.
*   **HTMX:** The client-side library (added via a simple script tag) that makes requests to your server (often triggered by `hx-get`, `hx-post` attributes) and swaps the returned HTML fragments into the page.
*   **RizzyUI:** Provides the actual **Blazor Components** (`<Button>`, `<Card>`, `<TextField>`, etc.) that Rizzy renders and HTMX swaps. These components are styled with Tailwind and use Alpine.js for their client-side sprinkle of interactivity.

Think of it like this: Rizzy tells ASP.NET *how* to use Blazor for rendering, HTMX tells the browser *how* to dynamically update the page, and RizzyUI gives you the pre-fabricated *parts* to render and update.

## [Is RizzyUI For You?](#is-rizzyui-for-you)

RizzyUI is likely a great fit if you are:

*   An **ASP.NET Core developer** using MVC or Minimal APIs.
*   Using **Rizzy** to leverage **Blazor Components for server-side rendering**.
*   Using **HTMX** for partial page updates and dynamic interactions.
*   Looking for a set of **pre-built, themeable UI components** that work well in this SSR/HTMX environment.
*   Comfortable with (or willing to set up) **Tailwind CSS** for styling.
*   Preferring **minimal client-side JavaScript**, using something lightweight like **Alpine.js** only where needed for UI behaviors.

If you're building a Blazor Server or Blazor WebAssembly application with full client-side interactivity managed by the Blazor runtime, RizzyUI might not be the primary choice, as its interactivity model is different (Alpine.js vs. Blazor's C# event handling).

## [Where to Go Next?](#where-to-go-next)

Ready to get started or learn more? Here are the main sections:

{{< link-card
  title="Setup"
  description="Install RizzyUI, configure Tailwind, and set up services."
  href="../setup/overview/"
  target="_self"
>}}
{{< link-card
  title="Core Concepts"
  description="Understand styling, theming, interactivity, and accessibility."
  href="../concepts/overview/"
  target="_self"
>}}
{{< link-card
  title="Components"
  description="Explore the available UI components and how to use them."
  href="../components/"
  target="_self"
>}}