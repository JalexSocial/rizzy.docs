---
title: "Overview"
description: "Understand the fundamental ideas behind RizzyUI's design and functionality."
summary: "Learn about the core concepts driving RizzyUI, including its styling philosophy, theming system, approach to interactivity, and commitment to accessibility."
date: 2024-07-28T10:10:00-05:00 # Adjust date as needed
lastmod: 2024-07-28T10:10:00-05:00 # Adjust date as needed
draft: false
menu:
  docs:
    parent: "concepts" # Parent is the RizzyUI root
    identifier: "rizzyui-concepts-overview"
weight: 5 # Position after Setup
toc: true
seo:
  title: "RizzyUI Core Concepts | Rizzy Documentation"
  description: "Explore the foundational principles of RizzyUI: styling with Tailwind, theming with CSS variables, interactivity via Alpine.js, and accessibility features."
---

Alright, so you've got RizzyUI installed and configured (or you're thinking about it!). Now, let's peek under the hood a bit. Understanding the *why* behind RizzyUI's design choices will make using it much smoother and help you customize things effectively.

Think of this section as the conceptual foundation. We're not diving deep into *every* component parameter here (that's what the [Components](../components/) section is for!), but rather exploring the main pillars that hold RizzyUI together:

1.  **[Styling Philosophy](../styling-philosophy):** How do components get their looks? We'll talk about Tailwind CSS, design tokens (CSS variables), and how you can add your own styles without breaking things.
2.  **[Theming](../theming):** How can you change the overall appearance (colors, borders, dark mode) easily and consistently across all components? This covers the `<RizzyThemeProvider />` and creating custom themes.
3.  **[Client-Side Interactivity](../client-side-interactivity):** How do things like dropdowns open or modals appear without Blazor's full interactive modes? We'll touch on the role of Alpine.js.
4.  **[Accessibility (A11y)](../accessibility):** How does RizzyUI ensure components are usable by everyone, including those using assistive technologies?

Grasping these core concepts will give you the context needed to leverage RizzyUI effectively in your server-rendered ASP.NET applications. Let's dive in, starting with how components are styled.