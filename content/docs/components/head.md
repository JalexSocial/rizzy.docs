---
title: "Head"
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

This document outlines three components created to improve management of HTML head content in applications that integrate Htmx with Razor components. These components, namely `RzHeadOutlet`, `RzPageTitle`, and `RzHeadContent`, correspond to Blazor's standard components, offering parallel functionality specifically adapted for use in Htmx-enhanced Razor applications.

Below is a table mapping each Rz component to its Blazor counterpart:

| Rizzy Component | Blazor Component |
|-----------------|------------------|
| RzHeadOutlet    | HeadOutlet       |
| RzPageTitle     | PageTitle        |
| RzHeadContent   | HeadContent      |

## RzHeadOutlet

The `RzHeadOutlet` component serves as a container for dynamically rendering content within the HTML `<head>` tag. It is designed to work in conjunction with `RzHeadContent` and `RzPageTitle` components to insert or update metadata, such as title tags and other head elements, at runtime.

### Usage

1. Include the `RzHeadOutlet` component within the `<head>` tag of your application's main layout file (e.g., `_Layout.cshtml` for MVC or `MainLayout.razor` for Blazor).

2. The `RzHeadOutlet` component does not require any parameters. It automatically renders content provided by `RzHeadContent` and `RzPageTitle` components elsewhere in the application.

```html
<head>
    ...
    <RzHeadOutlet />
</head>
```

## RzPageTitle

The `RzPageTitle` component enables dynamic updating of the page's title tag (`<title>`) based on the application's routing or state changes. It is designed to work with both traditional and Htmx-driven requests. This component detects if the request is made through Htmx and adjusts its page title rendering to enable Htmx to apply the new title after the request is swapped in place.

### Usage

1. Use the `RzPageTitle` component within Razor pages or components to specify the title of the page.

2. Provide the title content as a child content of the `RzPageTitle` component.

```razor
<RzPageTitle>
    Your Page Title Here
</RzPageTitle>
```

## RzHeadContent

The `RzHeadContent` component allows for the inclusion of additional content within the `<head>` section of the HTML document dynamically. This is particularly useful for adding or updating metadata, such as meta tags, links (e.g., stylesheets), and scripts, based on the application's context or routing.

### Usage

1. Wrap the content intended for the `<head>` section within an `RzHeadContent` component. This can be placed anywhere within your Razor components or pages.

2. The content provided to `RzHeadContent` will be rendered in the location of the `RzHeadOutlet` within your application's layout.

```razor
<RzHeadContent>
    <link href="custom-styles.css" rel="stylesheet" />
    <meta name="description" content="Your page description here" />
</RzHeadContent>
```

### Planned Enhancements

Starting with Htmx 2.0, `RzHeadContent` is expected to gain additional capabilities to better support dynamic content rendering in scenarios involving Htmx requests, aligning its functionality more closely with that of `RzPageTitle`.

## Conclusion

The `RzHeadOutlet`, `RzPageTitle`, and `RzHeadContent` components provide a structured and dynamic approach to managing the content of the HTML head section in applications leveraging Htmx with Razor components. By using these components, developers can easily update the page title and other metadata in response to application state changes or routing events, enhancing the flexibility and responsiveness of their applications.
