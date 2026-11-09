
---
title: "Head Components"
description: ""
summary: ""
date: 2024-03-05T09:43:29-05:00
lastmod: 2024-03-05T09:43:29-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "head-8edb4f9eeaa998af90946f96a65ea892"
weight: 150
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This document outlines components created to improve the management of HTML head content and configuration in applications that integrate Htmx with Razor components.

## RzHeadOutlet

`RzHeadOutlet` replaces Blazor's `HeadOutlet` in the `<head>` of your root layout. It renders:

1. Blazor's `HeadOutlet`, so page titles (`RzPageTitle`, `PageTitle`) and `<HeadContent>` work as usual, and
2. Rizzy's `<meta name="htmx-config">` tag (`HtmxConfigHeadOutlet`), which carries your [htmx configuration]({{<ref "/docs/htmx/configuration.md">}}), the antiforgery token and the Rizzy version.

Place it **before** the htmx script: htmx reads the meta tag once, when its script loads.

```razor {title="AppLayout.razor"}
<head>
    <meta charset="utf-8" />
    <base href="/" />
    <RzHeadOutlet />
    <script src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.1/dist/htmx.min.js" integrity="sha384-Qp9rdC8H7EqOoX+nR0P3RPG2Noji+qdwJlGpfzwQJsfOpp3sGwIdSP9xO3+UlEhn" crossorigin="anonymous"></script>
    <script src="_content/Rizzy/js/rizzy.js"></script>
</head>
```

The rendered meta tag looks like this:

```html
<meta name="htmx-config" content='{"mode":"same-origin","antiforgery":{"formFieldName":"__RequestVerificationToken","headerName":"RequestVerificationToken","requestToken":"..."},"rizzyVersion":"6.0.0"}'>
```

{{< callout context="note" title="Why not HeadContent?" icon="info-circle" >}}
Rizzy 5 added this tag through `<HeadContent>`. Blazor shows only the most recently rendered `<HeadContent>`, so any page with its own `<HeadContent>` silently replaced Rizzy's tag, and htmx lost its configuration and antiforgery token. `RzHeadOutlet` renders the tag directly, so pages can use `<HeadContent>` freely.
{{< /callout >}}

If the tag is missing, rizzy.js logs a console warning that names `RzHeadOutlet`.

### HtmxConfigHeadOutlet

`HtmxConfigHeadOutlet` is the component that renders the meta tag; `RzHeadOutlet` includes it. Use it directly only if you build your own head outlet, and render it once, before the htmx script.

## RzPageTitle

The `RzPageTitle` component enables dynamic updating of the page's title tag (`<title>`) based on the application's routing or state changes. It is designed to work with both traditional and Htmx-driven requests. This component detects if the request is made through Htmx and adjusts its page title rendering to enable Htmx to apply the new title after the request is swapped in place.

### Usage

Use the `RzPageTitle` component within Razor pages or components to specify the title of the page.

```razor
<RzPageTitle>
    Your Page Title Here
</RzPageTitle>
```

If it detects an HTMX request, it outputs `<title>Your Page Title Here</title>` directly, which HTMX natively processes to update the document title without a full reload. On standard requests, it falls back to Blazor's standard `PageTitle` component.

## Standard Blazor Head Components

Rizzy is fully compatible with standard Blazor head manipulation components. You should use the standard components provided by `Microsoft.AspNetCore.Components.Web` to inject other head content like meta tags and external style sheets.

- **`HeadOutlet`**: rendered for you by `RzHeadOutlet`; don't add a second one.
- **`HeadContent`**: Wrap your `<link>`, `<meta>`, or `<script>` tags inside this component in your individual views.

```razor
<HeadContent>
    <link href="custom-styles.css" rel="stylesheet" />
    <meta name="description" content="Your page description here" />
</HeadContent>
```