
---
title: "Content"
description: ""
summary: ""
date: 2024-03-05T09:42:17-05:00
lastmod: 2024-03-05T09:42:17-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "content-4f598ca54b2e54189085d00396d92ebb"
weight: 100
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This guide introduces the `RzView` component, which is specifically designed to integrate with Htmx for content rendering within ASP.NET applications. This component is used internally by Rizzy to render Blazor components as full pages or partial HTML fragments in response to requests, often initiated by HTMX.

{{< callout context="caution" title="Caution" icon="alert-triangle" >}}
It is not typical that you will need to invoke the `RzView` component directly in your markup. This documentation is provided simply to describe how Rizzy intends to function under the hood when rendering your views.
{{< /callout >}}

## RzView

`RzView` is a Razor component that acts as the primary container for rendering your components. Its behavior is controlled by the `Mode` parameter, which accepts values from the `RzViewMode` enum (`Page` or `Partial`). `RzView` is utilized by the `RzController` methods or the `IRizzyService` to handle the rendering lifecycle.

### Key Features
- Dynamically renders Razor components as full pages or partial fragments.
- Automatically handles ASP.NET Core `ModelState` cascading to enable form validation.
- Automatically injects out-of-band (OOB) swap content via the `HtmxSwapContent` component.

### Page Mode (`RzViewMode.Page`)
When rendering as a full page, `RzView` applies the configured root component (e.g., your `AppLayout`) and automatically resolves the appropriate inner layout.
- If the component being rendered has a `@layout` attribute, that layout will be applied to the page. 
- If it doesn't, then the default layout specified in the Rizzy configuration (`RizzyConfig.DefaultLayout`) will be applied. See [Getting Started](/docs/introduction/getting-started/#configuration).
- Automatically includes `<HtmxConfigHeadOutlet>` to render the HTMX configuration meta tag into the document head.

### Partial Mode (`RzViewMode.Partial`)
When rendering as a partial view (often via HTMX AJAX requests), `RzView` bypasses the configured root component entirely.
- It skips automatic layout resolution and instead renders the component through an `EmptyLayout`.
- This makes it ideal for embedding dynamic content within other views or returning targeted HTML fragments without inheriting the parent's layout shell.

## Special Notes

Both `IRizzyService` and `RzController` provide methods like `View<T>` and `PartialView<T>` which internally use `RzView` with the corresponding mode to render your Blazor components. They handle setting up the render context, evaluating parameters via the fluent builder, and passing the `ModelState`.