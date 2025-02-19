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

Rizzy allows developers to utilize static rendered SSR Blazor components with HTMX, where client-side interactivity is provided through the use of a touch of javascript to power each component. The interactivity comes through the usage of Alpine.js. Alpine.js is a lightweight JavaScript framework designed for adding interactivity to web pages with minimal overhead. It's often described as a "minimalist" alternative to heavier frameworks like Vue.js or React, providing the ability to handle tasks such as event handling, data binding, and DOM manipulation directly within HTML. Alpine.js is particularly useful for enhancing static pages without the need for a complex build setup, making it ideal for projects that need small, reactive components with a low learning curve. It leverages declarative syntax similar to Vue, making it intuitive and easy to integrate into existing projects.

RizzyUI (optional) provides a full starter suite of Tailwind-based UI components, built with Alpine.js but created in a way to work with content security policies. This CSP-first approach requires careful consideration to each component design, as no Rizzy component contains any Alpine.js code that is actually executed inline. The result is much easier to debug.  Also, you as a developer are under no obligation to use Alpine.js CSP builds if you don't want to. Our approach was intended to address potential Alpine.js security considerations early in the process by adopting a standard of development that might exceed your own development requirements, particularly when it comes to CSP.

<img src="/images/developer1.webp" class="img-fluid">

## Key Features and Benefits

Rizzy offers several features that make it a valuable tool for developers:

- **Robust Request and Response Handling:** Rizzy automatically detects HTMX-specific headers, parses triggers, and sets response parameters (e.g., push URL, redirect, refresh). This simplifies managing the request lifecycle while ensuring consistency across the application.

- **Flexible Swap Strategies:** Rizzy provides a variety of swap styles (such as innerHTML, beforebegin, afterend, and more) through its `SwapStyle` enum and builder extensions. This allows for fine-grained control over how content is replaced or updated.

- **Security-First Approach:** Rizzy integrates with anti-forgery mechanisms and nonce generation, helping to safeguard interactive endpoints from common security vulnerabilities.


