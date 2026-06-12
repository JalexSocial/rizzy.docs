---
title: "Overview"
description: ""
summary: ""
date: 2024-02-05T12:10:06-05:00
lastmod: 2024-02-05T12:10:06-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "overview-305bdd1971c9dc60178213e0c34dc450"
weight: 10
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

<img src="/images/htmx.png" class="img-fluid"/>

<p>&nbsp;</p>

HTMX enables partial page updates by fetching HTML fragments from the server in response to events. Rizzy.Htmx provides helper classes and extensions for ASP.NET Core applications using Rizzy to work with HTMX requests and responses. It simplifies reading HTMX request headers and setting HTMX response headers when rendering Blazor components server‑side. 

## What Is Rizzy.Htmx?

Rizzy.Htmx provides .NET types and extension methods to interact with the headers used by HTMX. This allows server‑side code (like MVC controllers or Minimal API endpoints rendering Blazor components) to detect if a request originated from HTMX and to send specific instructions back to HTMX via response headers (e.g., trigger client‑side events, redirect, change swap behavior).

In traditional web development, asynchronous updates and partial page refreshes can quickly become tangled, leading to code that’s hard to debug and maintain. Rizzy.Htmx addresses these challenges by encapsulating complex client‑server interactions into reusable components and configuration settings. This not only enhances the interactivity of your application but also improves the overall code quality and developer experience.

## Key Features and Benefits

Key features of Rizzy.Htmx include:

- **Robust Request and Response Handling:**  
  With classes like `HtmxRequest` and `HtmxResponse`, the library automatically detects HTMX‑specific headers, parses triggers, and sets response parameters (e.g., push URL, redirect, refresh). This simplifies managing the request lifecycle while ensuring consistency across your application.

- **Flexible Swap Strategies:**  
  Similar to choosing between `innerHTML` and `outerHTML` in traditional DOM manipulation, Rizzy.Htmx offers a variety of swap styles (such as innerHTML, beforebegin, afterend and more) through its `SwapStyle` enum and builder extensions. This allows for fine‑grained control over how content is replaced or updated.

- **Security‑First Approach:**  
  Rizzy.Htmx seamlessly integrates with anti‑forgery mechanisms and nonce generation. By leveraging configuration options such as `HtmxAntiforgeryOptions` and the accompanying nonce provider (`IRizzyNonceProvider`), it helps safeguard your interactive endpoints from common security vulnerabilities.

{{< callout context="warning" title="HTMX 4 Updates" icon="alert-circle" >}}
HTMX 4 introduced several important changes compared to the 2.x series. Keep the following in mind when building Rizzy applications:

- **Explicit Attribute Inheritance:** Attributes like `hx-target`, `hx-confirm` and others are no longer inherited down the DOM tree by default. Use the `:inherited` suffix (e.g., `hx-target:inherited="#content"`) or `:append` when you want child elements to inherit or append to parent values【381859254872383†L141-L163】.
- **Error Responses Swap by Default:** HTMX 4 swaps all HTTP responses by default, including 4xx and 5xx codes. Use the `HX-Status` response header or the `hx-status` attribute to control swap behavior for particular status codes【381859254872383†L169-L175】.
- **`hx-disable` Renamed to `hx-ignore`:** The old `hx-disable` attribute has been replaced by `hx-ignore` to skip HTMX processing on an element. The new `hx-disable` now disables form elements during requests【381859254872383†L240-L247】.
- **Morphing Swap Styles and Aliases:** HTMX 4 supports morphing diff swap styles (`innerMorph` and `outerMorph`) and provides alias values like `before`, `after`, `prepend`, and `append` for more intuitive swap positioning【989634978019296†L420-L432】.
- **Loading Extensions Without `hx-ext`:** Do not use `hx-ext` in HTMX 4. Instead, load extension scripts directly after HTMX and configure allowed extensions via the `extensions` key in your `HtmxConfig` or a `<meta name="htmx-config">` tag【381859254872383†L224-L235】.

For a complete list of changes and migration tips, see the official HTMX 4 documentation.
{{< /callout >}}

---

## A Quick Example

Imagine you’re building a dashboard where users can update portions of the page without a full reload. With Rizzy.Htmx, you can define a dynamic section that swaps its content based on an HTMX trigger. Here’s a brief sample to illustrate the concept:

```csharp
@using Rizzy.Htmx

<div id="dynamic-content">
    @* This component will be replaced dynamically 2 seconds after the button below is pushed *@
</div>

<button class="btn btn-primary" 
        hx-get="/Dashboard/UpdateSection" 
        hx-target="#dynamic-content" 
        hx-swap="@SwapStyle.outerHTML.AfterSwapDelay(TimeSpan.FromSeconds(2))">
    Refresh Section
</button>
```

In this example, a simple button initiates an HTMX request. When clicked, the request is processed server‑side, and the resulting component is swapped into the designated `<div>`. This pattern keeps your UI responsive and decoupled from the complexity of AJAX calls and manual DOM updates.

---

## Wrapping Up

Rizzy.Htmx provides strongly‑typed access to HTMX request/response headers and configuration options within an ASP.NET Core/Rizzy application. This avoids manual header parsing/setting and provides helpers for common HTMX interactions like redirects, triggers, and swap modifications when returning server‑rendered Blazor component fragments.

In upcoming sections, we’ll dive deeper into configuring these components, understanding the full lifecycle of HTMX requests, and exploring advanced topics such as custom swap strategies and event triggers. For now, this overview should provide you with a solid foundation on the value Rizzy.Htmx brings to modern ASP.NET Core applications.