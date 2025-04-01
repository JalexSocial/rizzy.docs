---
title: "Overview"
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
    identifier: "rizzyui-setup-overview"
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
## Welcome to RizzyUI!

So, you've embraced the **Rizzy** way of life – using the power of **Blazor Components** for server-side rendering within your trusty ASP.NET Core application, perhaps supercharging it with **HTMX** for those smooth, partial page updates. It's a great setup! But now you need actual UI building blocks – buttons, cards, forms, navbars – that look good, work seamlessly in this SSR/HTMX environment, and don't force you into writing heaps of custom CSS or JavaScript.

That's precisely where **RizzyUI** steps in.

## [What is RizzyUI, Really?](#what-is-rizzyui-really)

Think of RizzyUI as your pre-built toolkit of **Blazor Components** specifically designed for the world of server-side rendering and HTMX interactions. It leverages:

*   **Blazor Components (`.razor`):** For structure and server-side logic, using the component model you already know if you've touched Blazor.
*   **Tailwind CSS:** For all styling, using a utility-first approach. Components are built with Tailwind classes, making customization familiar and powerful. (You'll need Tailwind set up in your project!)
*   **Alpine.js:** For lightweight, client-side interactivity (like dropdowns opening, modals appearing) *without* needing Blazor's SignalR or WebAssembly runtimes for *every* little thing. It keeps things fast and CSP-friendly.

In a nutshell, RizzyUI gives you ready-made UI pieces that render on the server via Rizzy and play nicely when parts of your page are swapped out by HTMX.

## [What Are We Trying To Achieve Here? (Key Goals)](#what-are-we-trying-to-achieve-here-key-goals)

Why build *another* component library? RizzyUI focuses on a specific niche with these goals in mind:

1.  **Great Developer Experience:** Provide components that feel intuitive to use within a Blazor/Rizzy context. Reduce the boilerplate needed to build common UI patterns.
2.  **Visual Consistency & Theming:** Use a robust theming system built on CSS custom properties (design tokens). Easily switch between light/dark modes or even create your own themes that apply consistently across all components.
3.  **Targeted Interactivity:** Handle common client-side interactions (toggles, dropdowns, etc.) efficiently using Alpine.js, keeping the component footprint small and avoiding the need for heavier client-side frameworks for simple UI behaviors.
4.  **SSR & HTMX Compatibility:** Ensure components render correctly on the server and function as expected when subjected to HTMX partial updates and swaps.

## [How Does RizzyUI Fit with Rizzy and HTMX?](#how-does-rizzyui-fit-with-rizzy-and-htmx)

It helps to understand the roles:

*   **ASP.NET Core (MVC/Minimal API):** Your application's backbone, handling routing, logic, data access, security.
*   **Rizzy:** The bridge that allows your ASP.NET Core app to render **Blazor Components** server-side as HTML responses.
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