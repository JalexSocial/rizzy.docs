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

This component is designed to wrap the application's layout within an `HtmxLayout` component. It facilitates the dynamic rendering of layouts and content, making it essential for applications that require flexibility in their layout rendering.

### Configuration

To integrate `HtmxApp` into an application, it is configured during the Rizzy setup process as follows:

```csharp
builder.AddRizzy(config =>
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

This component differentiates between full page requests and HTMX requests. For full page requests, it renders the specified layout. For HTMX requests, aimed at loading dynamic content without a full page refresh, it alters the rendering behavior to avoid rendering the entire layout.

### Implementation Details

`HtmxLayout` includes two internal classes, `EmptyLayout` and `MinimalLayout`, to support its conditional rendering functionality. Based on whether the request is an HTMX request and if the component is the root component, it chooses the appropriate rendering approach.

- **For HTMX Requests:** It applies a minimal or no layout to quickly load dynamic content.
- **For Full Page Requests:** It renders the complete layout as specified by the generic type `T`.

This behavior ensures efficient content loading and rendering, supporting the application's responsiveness and performance.
