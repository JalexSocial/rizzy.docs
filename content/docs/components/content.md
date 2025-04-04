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

This guide introduces two Razor components specifically designed to integrate with Htmx for content rendering within ASP.NET applications. These components are `RzPage` and `RzPartial`. Both are used by Rizzy to render Blazor components as full pages or partial HTML fragments in response to requests, often initiated by HTMX.

{{< callout context="caution" title="Caution" icon="alert-triangle" >}}
It is not typical that you will need to invoke either of these two components directly. This documentation is provided simply to describe how they
are intended to function.
{{< /callout >}}

## RzPage

`RzPage` is a Razor component that acts as a page container.  It cascades the `RzViewContext` value across the component tree it encompasses. `RzPage` is typically not used directly and is instead utilized by the RzController View&lt;T&gt; method or the RizzyService View&lt;T&gt; method.

### Key Features
- Dynamically renders Razor components as full pages.
- Wraps a component of your choice inside the Rizzy-configured [RootComponent](/docs/introduction/getting-started/#configuration).
- Supports dynamic layout selection based on attributes or Rizzy application configuration.

### Usage
- Configuration involves specifying `ComponentType`, `ComponentParameters`, and providing a `ViewContext` for the component being rendered.
- If the component that is provided by ComponentType has a @layout attribute, that layout will be applied to the page. If it doesn't, then the default layout specified in the Rizzy configuration will be applied. See [Getting Started](/docs/introduction/getting-started/#configuration).

## RzPartial

Similar to `RzPage`, `RzPartial` is designed for rendering Razor components as partial views. It follows the same dynamic rendering principles but defaults to using an `EmptyLayout`, making it ideal for embedding within other views or components without inheriting the parent's layout.

### Key Features
- Renders Razor components as partial views without a layout.
- Suitable for dynamic content loading and updating within existing pages.

### Usage
- Like `RzPage`, `RzPartial` is rendered through services or controllers, specifying `ComponentType` and `ComponentParameters`.
- Primarily used for injecting dynamic content into specific sections of a page, enhancing modularity and reusability of components.

## Special Notes

Both `RizzyService` and `RzController` provide methods like `View<T>` and `PartialView<T>` which internally use RzPage or RzPartial to render Blazor components. They handle passing parameters, cascading ModelState (in `RzController`), and setting up the render context. They also provide helpers like `CurrentActionUrl`.
