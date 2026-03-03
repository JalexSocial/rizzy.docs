
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

## HtmxConfigHeadOutlet

The `HtmxConfigHeadOutlet` component is critical for rendering Rizzy's server-side HTMX configurations directly into your HTML document as a `<meta>` tag. This makes the configuration available to the HTMX client library automatically.

### Usage

1. Include the `HtmxConfigHeadOutlet` component within the `<head>` tag of your application's main layout file (e.g., `AppLayout.razor`).
2. It automatically resolves the `HtmxConfig` options from dependency injection and renders them. It also handles rendering anti-forgery tokens (if configured).

```razor
<head>
    ...
    <HtmxConfigHeadOutlet />
</head>
```

When rendered, the component will output a meta tag similar to this:
```html
<meta name="htmx-config" content='{"selfRequestsOnly":true,"antiforgery":{"cookieName":"HX-XSRF-TOKEN","formFieldName":"__RequestVerificationToken","headerName":"RequestVerificationToken","requestToken":"..."}}'>
```

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

- **`HeadOutlet`**: Add this to the `<head>` of your layout to serve as the destination for head content changes.
- **`HeadContent`**: Wrap your `<link>`, `<meta>`, or `<script>` tags inside this component in your individual views.

```razor
<HeadContent>
    <link href="custom-styles.css" rel="stylesheet" />
    <meta name="description" content="Your page description here" />
</HeadContent>
```