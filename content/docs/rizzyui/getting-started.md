---
title: "Getting Started"
description: "Get the big picture on integrating RizzyUI into your ASP.NET Core project."
summary: "Understand the key steps and components involved in setting up RizzyUI, from NuGet packages to Tailwind configuration and service registration."
date: 2024-07-28T10:00:00-05:00 # Adjust date as needed
lastmod: 2024-07-28T10:00:00-05:00 # Adjust date as needed
draft: false
menu:
  docs:
    parent: "rizzyui" # Assuming a setup sub-section
    identifier: "rizzyui-setup-overview"
weight: 10 # First item in setup
toc: true
seo:
  title: "RizzyUI Getting Started | Rizzy Documentation"
  description: "Learn the essential parts of setting up the RizzyUI component library in your ASP.NET Core application, including Tailwind CSS, themes, and JavaScript."
---

So, you're building modern web UIs with ASP.NET Core, maybe using Rizzy and HTMX for those slick partial updates, and you've heard about **RizzyUI**. It promises pre-built, themeable components using Blazor syntax, styled with Tailwind CSS, and sprinkled with just enough Alpine.js magic for interactivity, all without needing a full client-side framework. Sounds good, right? But how do you actually *integrate* this library into your project? What are the moving parts?

In this overview, we'll take a bird's-eye look at the setup process. Think of this as the map before you dive into the detailed turn-by-turn directions found in our [Installation](./installation.md) and [Configuration](./configuration.md) guides.

## [Setup Process](#why-bother-with-setup-its-more-than-just-nuget)
<br/>
<p>
<img src="/images/rizzyui-overview.svg" class="img-fluid" alt="RizzyUI Setup">
</p>
<br/>
Unlike adding a simple utility library, getting RizzyUI humming involves a few key pieces working together. It's not complex, but understanding *why* each step is needed helps immensely:

1.  **Add Core Components (`RizzyUI` NuGet):** This is the foundation – it brings in all the `.razor` components and their C# logic. Pretty standard stuff.
2.  **Setup Tailwind CSS:** RizzyUI components don't ship with pre-compiled CSS. They rely on **Tailwind CSS** utility classes. This means *your* project needs to run Tailwind to scan RizzyUI's component markup (and your own) and generate the necessary CSS file. This gives you ultimate control and keeps the final CSS lean.
3.  **Theme Provider:** Consistency is key. RizzyUI uses CSS custom properties (design tokens like `--color-surface`, `--color-primary`) for all its styling. The Theme Provider component (`<RizzyThemeProvider>`) injects these variables into your page's `<head>`, making sure all components look cohesive and enabling easy theme switching (including light/dark modes).
4.  **The Interactivity Layer (Alpine.js via `rizzyui.js`/`rizzyui-csp.js`):** For things like dropdowns opening, accordions collapsing, or modals showing, RizzyUI uses small, targeted bits of JavaScript powered by **Alpine.js**. The provided RizzyUI JavaScript file bundles Alpine.js and the necessary component logic, ensuring interactivity works out-of-the-box without you writing the JS.
5.  **Wiring It Up (`AddRizzyUI()`):** Like most ASP.NET Core libraries, RizzyUI needs its services registered in your `Program.cs`. This sets up essential helpers and makes things like theme configuration available.

Skipping a step, like forgetting to configure Tailwind or missing the Theme Provider, will likely result in components that look unstyled or plain wrong. So, while it involves a few parts, the setup ensures everything plays nicely together.

## [The Setup Journey: Key Milestones](#the-setup-journey-key-milestones)

Getting RizzyUI ready typically follows these steps:

1.  **Install Packages:** Add the `RizzyUI` NuGet package to your project.
2.  **Configure Tailwind:** Set up Tailwind CSS, making sure its `tailwind.config.js` knows where to find RizzyUI's components so it can scan their classes.
3.  **Build & Include CSS:** Run the Tailwind CLI build process (often in `watch` mode during development) and include the generated CSS file in your main layout.
4.  **Register Services:** Call `builder.Services.AddRizzyUI()` in your `Program.cs`, optionally configuring defaults like the application theme.
5.  **Add Theme Provider:** Place the `<RizzyThemeProvider />` component within the `<head>` of your main application layout (e.g., `AppLayout.razor`).
6.  **Include JavaScript:** Add a script tag for either `/_content/RizzyUI/dist/rizzyui.js` or `/_content/RizzyUI/dist/rizzyui-csp.js` (for stricter Content Security Policy environments) to your layout, usually near the end of the `<body>`.

Don't worry, we won't leave you hanging here. Each of these steps is covered in detail in the following guides:

*   **[Installation Guide](./installation.md):** Covers NuGet, Tailwind setup, and CSS integration.
*   **[Configuration Guide](./configuration.md):** Details service registration, theme provider usage, and JavaScript inclusion.

## [Conclusion](#conclusion)

Setting up RizzyUI involves coordinating the core library, Tailwind CSS for styling, a theme provider for consistency, and a touch of JavaScript for interactivity. While it might seem like a few steps compared to just adding a CSS file, this approach provides a powerful, customizable, and maintainable foundation for building your UIs with Razor Components.

With this overview in mind, you're ready to dive into the specifics. Head over to the [Installation Guide](./installation.md) to get started with adding the necessary packages and configuring Tailwind CSS. Let's get those components rendering!