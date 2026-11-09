---
title: "Layout"
description: ""
summary: ""
date: 2024-03-05T09:43:49-05:00
lastmod: 2024-03-05T09:43:49-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "layout-7793c3726a94090573d888edb4fa165e"
weight: 175
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Overview

This documentation focuses on two Razor components, `HtmxApp<T>` and `HtmxLayout<T>`, which are used in ASP.NET Core web applications to manage layouts. These components are particularly useful for applications that implement dynamic content loading with HTMX.

## HtmxApp Component

### Definition

`HtmxApp<T>` acts as a root component for an application, serving primarily as a container for the application's layout. It extends `ComponentBase` and is generic, meaning it can work with any layout component derived from `LayoutComponentBase`.

### Usage

The `HtmxApp<TLayout>` component acts as the root component specified in Rizzy configuration. It wraps the application's actual layout component (e.g., AppLayout) inside an `HtmxLayout<TLayout>` component.

### Configuration

To integrate `HtmxApp` into an application, it is configured during the Rizzy setup process as follows:

```csharp
builder.Services.AddRizzy(config =>
{
    config.RootComponent = typeof(HtmxApp<AppLayout>);
    config.DefaultLayout = typeof(HtmxLayout<MainLayout>);
});
```

Here, `AppLayout` represents the root layout component of the application, which `HtmxApp` will wrap within an `HtmxLayout`.

## HtmxLayout Component

### Definition

`HtmxLayout<T>` is a layout component designed to support conditional rendering based on the type of request. It inherits from `LayoutComponentBase` and uses generics to accommodate any layout component extending `LayoutComponentBase`.

### Functionality

`HtmxLayout<TLayout>` decides per request whether to render `TLayout`:

| Request | Layout |
|---|---|
| Normal browser request | `TLayout` (the full page) |
| htmx request that targets one element (`HX-Request-Type: partial`) | No layout: just the component, ready to be swapped into the target |
| Boosted navigation that swaps the body, `hx-select`, or back/forward history restore (`HX-Request-Type: full`) | `TLayout` (htmx 4 needs the full page for these) |

Every response varies on the htmx request headers (`Vary`), so caches keep full pages and fragments apart.

When `HtmxLayout` is used through `HtmxApp<T>` (the root component) and a fragment is requested, it wraps the fragment in a minimal `<html><body>` document. This lets the Rizzy client tell where the initial HTML of a [streaming]({{<ref "/docs/htmx/streaming.md">}}) response ends.

### History (back and forward)

htmx 4 keeps no history cache: on back/forward it re-fetches the page with `HX-History-Restore-Request: true`, and Rizzy answers with the full layout. By default htmx replaces the whole `<body>`. To restore only part of the page (and keep, for example, a sidebar that polls the server), mark that element with `hx-history-elt`:

```razor {title="MainLayout.razor"}
<div class="page">
    <NavMenu />
    <article hx-history-elt>
        @Body
    </article>
</div>
```

To make back/forward reload the page instead, set `HtmxConfig.History = HtmxHistoryMode.Reload`.
