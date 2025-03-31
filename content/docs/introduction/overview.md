---
title: "Overview"
description: ""
summary: ""
date: 2024-02-05T12:06:30-05:00
lastmod: 2024-02-05T12:06:30-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "overview-d93d15301c0c12c7496db4ce3d157080"
weight: 10
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Rizzy is a lightweight library that enhances Asp.net MVC applications by seamlessly integrating Razor components for UI development and working with HTMX for progressive enhancement. With Rizzy, you can use composable Razor components to create dynamic and interactive user interfaces while ensuring a smooth user experience through HTMX.

<img src="/images/rizzy-wide-banner.png" class="img-fluid" alt="Rizzy Banner">

RizzyUI (optional) provides a full starter suite of Tailwind-based UI components, built with Alpine.js, that provide client-side interactivity without needing to write the components yourself or implement them in Blazor.

<p> </p>

## Leverage the Best of Both Worlds: Robust MVC/API Structure meets Modern Blazor UI Components

Remember the power and structure of ASP.NET Core (MVC or Minimal APIs)? The clear separation of concerns, the robust routing and model binding, the mature ecosystem for handling business logic, security, and data access? It's a solid foundation many .NET developers know and trust.

Now, think about building modern UIs. Razor Components (Blazor) offer a productive, component-based approach using C# for everything – logic, markup, composition. Building reusable, encapsulated UI pieces feels natural and leverages your existing .NET skills, often avoiding the context switch to heavy JavaScript frameworks.

**So, why choose between them? Rizzy lets you combine their strengths.**

Imagine using ASP.NET Core's reliable request pipeline to handle your core application logic, routing, and security, but **rendering your views using the power and reusability of Razor Components.**

**But wait, doesn't that mean full page reloads for every interaction?** Not with Rizzy. By integrating HTMX seamlessly behind the scenes, Rizzy allows those server-rendered Razor Components to drive dynamic, partial page updates.

**Here's why this combination is compelling:**

1.  **Productivity Boost:** Write your UI *and* backend logic primarily in C#. Reuse Blazor components across your application, simplifying UI development and maintenance compared to managing separate HTML templates and complex JavaScript.
2.  **Leverage Existing Skills & Ecosystem:** Continue using the familiar, powerful features of ASP.NET Core for your application's core structure, authentication, validation, and data handling. Benefit from the vast .NET ecosystem.
3.  **Simplified Interactivity:** Achieve dynamic partial updates (like SPAs) without writing mountains of JavaScript or adopting complex client-side frameworks. Let HTMX (managed by Rizzy) handle the AJAX, while Blazor handles rendering the HTML fragments.
4.  **Maintainability:** Keep your UI logic closer to your backend logic within the .NET ecosystem. Using strongly-typed components often leads to more maintainable and refactorable code than manipulating HTML strings or managing disparate client-side scripts.
5.  **Progressive Enhancement:** Start with a solid, server-rendered foundation (great for SEO and initial load) and layer dynamic behavior on top where needed, using the same Blazor components for both initial render and HTMX updates.

**In essence, Rizzy offers a "sweet spot":** keep the robust, scalable backend architecture you already know, but build your UIs with the modern, productive component model of Blazor, and get dynamic, interactive user experiences without getting bogged down in JavaScript complexity. It's about leveraging C# and .NET end-to-end, for both structure *and* interactive UI rendering.

---

## How Rizzy Achieves This Integration

Rizzy provides a lightweight set of tools and components that bridge these technologies. Just as developers use value objects to prevent misusing primitive types, Rizzy provides abstractions that streamline how you handle dynamic updates:

-   **Robust Request and Response Handling:**
    With classes like `HtmxRequest` and `HtmxResponse` (accessible via HttpContext extensions), the library automatically detects HTMX-specific headers, parses triggers, and helps you easily set response parameters (e.g., push URL, redirect, refresh, trigger client events). This simplifies managing the request lifecycle while ensuring consistency.

-   **Flexible Swap Strategies:**
    Similar to choosing between `innerHTML` and `outerHTML` in traditional DOM manipulation, Rizzy offers a variety of swap styles (such as `innerHTML`, `beforebegin`, `afterend`, etc.) through its `SwapStyle` enum and fluent `SwapStyleBuilder`. This allows for fine-grained control over how content is replaced or updated.

-   **Security-First Approach:**
    Rizzy seamlessly integrates with ASP.NET Core anti-forgery mechanisms and offers CSP nonce generation support. By leveraging configuration options such as `HtmxAntiforgeryOptions` and the `IRizzyNonceProvider`, it helps safeguard your interactive endpoints.

-   **Component Rendering Integration:**
    Provides base controllers (`RzController`, `RzControllerWithViews`) and service methods (`IRizzyService`) to easily render Blazor components as full `IResult` responses from your MVC actions or Minimal API endpoints.

-   **Enhanced Forms:**
    Offers `RzInput*` components that work with Blazor's `EditForm` but generate markup compatible with standard client-side validation libraries often used in MVC/HTMX scenarios, along with handling `[SupplyParameterFromForm]`.

---

## Beyond the Core: Client-Side Interactivity

While Rizzy focuses on server-rendered components enhanced with HTMX, you might still need richer client-side interactivity. For this, combining Rizzy/HTMX with a lightweight JavaScript library like **Alpine.js** is a popular pattern.  For that we have RizzyUI as an off-the-shelf option.

Alpine.js allows you to handle tasks such as complex event handling, local state management within a component fragment, and DOM manipulation directly within your HTML markup, complementing the server-driven updates from HTMX. Rizzy even includes helpers like `SerializeAsAlpineData` to simplify passing server-side model data into Alpine components. (*See Extensions section for more details*).

---

## Wrapping Up

Rizzy empowers developers to build highly interactive web applications with less boilerplate and more consistency. By abstracting the intricacies of HTMX integration into well-defined components and configuration settings, it allows you to focus on what matters most: delivering a seamless user experience leveraging your existing .NET skills. Whether you’re enhancing an existing MVC application or starting a new project with Minimal APIs, Rizzy offers a clear path toward more dynamic and maintainable web development.
