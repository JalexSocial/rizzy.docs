---
title: "Getting Started"
description: ""
summary: ""
date: 2024-02-05T12:11:27-05:00
lastmod: 2024-07-28T10:00:00-05:00 # Updated timestamp
draft: false
menu:
  docs:
    htmx:
      parent: ""
      identifier: "configuration-9be46cbb530cd63819776bc374ed5c77"
weight: 100
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This document provides a comprehensive guide on setting up and configuring HTMX within your application using Rizzy.

To add the `Rizzy.Htmx` NuGet package to your project, follow these steps:

## Installation

### **Install the NuGet Package**

You can add the `Rizzy.Htmx` NuGet package using either Visual Studio or the .NET CLI.

### **Using Visual Studio**
1. Open your project in Visual Studio.
2. Right-click on the **Dependencies** node in the Solution Explorer.
3. Select **Manage NuGet Packages**.
4. In the **NuGet Package Manager**, search for `Rizzy.Htmx`.
5. Click **Install**.

### **Using the .NET CLI**
If you prefer using the command line, navigate to your project directory and run the following command:

```bash
dotnet add package Rizzy.Htmx
```

## Customizing HTMX Configuration

{{< callout context="note" title="Note" icon="info-circle" >}}
The configuration portion or Rizzy was constructed based on HTMX head configuration. You can find more information about HTMX head configuration on the official [Htmx documentation site](https://htmx.org/docs/#config).
{{< /callout >}}

### Adding HTMX Configuration in Program.cs

In `Program.cs`, you can add custom HTMX configurations using the `AddHtmx()` method. This configures the *default* `HtmxConfig` object. You can also add named configurations for your app if needed (though less common). Here's an example:

```csharp {title="Program.cs"}
using Rizzy.Htmx;

// Add HTMX Configuration Services
builder.Services.AddHtmx(config =>
{
    // Example: Set the default swap delay for all HTMX swaps
    config.DefaultSwapDelay = TimeSpan.FromMilliseconds(100);

    // Example: Enable global view transitions (HTMX 2.0+)
    // config.GlobalViewTransitions = true;

    // Note: config.SelfRequestsOnly defaults to true in Rizzy
    // config.SelfRequestsOnly = true;
});
```

### Setting Configuration in HTML

To include configurations inside the `<head>` tag of your HTML document (usually in your main layout file like `AppLayout.razor`), use the `<HtmxConfigHeadOutlet />` component. This component renders a `<meta name="htmx-config" ...>` tag containing the serialized JSON of your `HtmxConfig` object (either the default one configured in `Program.cs` or a named one if specified).

```html {title="AppLayout.razor"}
<head>
    ...
    <HtmxConfigHeadOutlet />
    ...
</head>
```

## HTMX Configuration Properties

Here is a description of the HTMX configuration properties that can be customized via `HtmxConfig` in Rizzy.

{{< callout context="note" title="Rizzy Defaults" icon="info-circle" >}}
A Rizzy Default of `unset` means Rizzy does not set a specific value by default for that configuration property. In these cases, HTMX's own default value will apply unless you explicitly configure it in `Program.cs` using `AddHtmx(config => ...)`.
{{< /callout >}}

| Property                 | Rizzy Default | HTMX Default   | Description                                                                                          |
|--------------------------|---------------|----------------|------------------------------------------------------------------------------------------------------|
| HistoryEnabled           | `unset`       | `true`         | Enables history tracking (pushing URLs automatically via `hx-boost` or `hx-push-url`).              |
| HistoryCacheSize         | `unset`       | `10`           | Sets the size of the history cache (number of pages stored).                                       |
| RefreshOnHistoryMiss     | `unset`       | `false`        | Determines whether to refresh the page on history misses instead of making an AJAX request.        |
| DefaultSwapStyle         | `unset`       | `innerHTML`    | Sets the default swap style (e.g., `innerHTML`, `outerHTML`).                                        |
| DefaultSwapDelay         | `unset`       | `0ms`          | Sets the default delay between receiving a response and swapping content.                           |
| DefaultSettleDelay       | `unset`       | `20ms`         | Sets the default delay between swapping content and settling it (processing scripts, etc.).       |
| IncludeIndicatorStyles   | `unset`       | `true`         | Specifies whether to include the default CSS for indicator styles.                                  |
| IndicatorClass           | `unset`       | `htmx-indicator` | Sets the class added to elements while a request is active (when using `hx-indicator`).              |
| RequestClass             | `unset`       | `htmx-request` | Sets the class added to the element making the request while the request is active.                |
| AddedClass               | `unset`       | `htmx-added`   | Sets the class added to newly added elements during the settle phase.                               |
| SettlingClass            | `unset`       | `htmx-settling`| Sets the class added to target elements during the settling phase.                                 |
| SwappingClass            | `unset`       | `htmx-swapping`| Sets the class added to target elements during the swap phase.                                     |
| AllowEval                | `unset`       | `true`         | Specifies whether to allow `eval()` for features like trigger filters (use `false` for stricter CSP). |
| AllowScriptTags          | `unset`       | `true`         | Specifies whether to process `<script>` tags found in AJAX responses.                               |
| InlineScriptNonce        | `unset`       | `''`           | Sets the nonce to add to inline scripts injected by HTMX (use with CSP).                          |
| InlineStyleNonce         | `unset`       | `''`           | Sets the nonce to add to inline styles injected by HTMX (use with CSP).                           |
| GenerateScriptNonce      | `false`       | N/A            | Rizzy specific: If true, uses `IRizzyNonceProvider` to set `InlineScriptNonce` automatically.    |
| GenerateStyleNonce       | `false`       | N/A            | Rizzy specific: If true, uses `IRizzyNonceProvider` to set `InlineStyleNonce` automatically.     |
| AttributesToSettle       | `unset`       | `["class", "style", "width", "height"]` | Specifies attributes to settle (copy from old to new elements) during the settling phase. |
| UseTemplateFragments     | `unset`       | `false`        | Specifies whether to use HTML `<template>` tags for parsing content (not IE11 compatible).          |
| WsReconnectDelay         | `unset`       | `"full-jitter"`| Sets the WebSocket reconnect delay strategy (e.g., `"full-jitter"`, `"1s"`).                       |
| WsBinaryType             | `unset`       | `"blob"`       | Sets the type of binary data received over WebSocket (`"blob"` or `"arraybuffer"`).                 |
| DisableSelector          | `unset`       | `[hx-disable], [data-hx-disable]` | Sets the selector for disabling HTMX processing on elements or their children.              |
| WithCredentials          | `unset`       | `false`        | Specifies whether to allow cross-site Access-Control requests with credentials (cookies, auth headers). |
| Timeout                  | `unset`       | `0`            | Sets the request timeout in milliseconds (0 means no timeout).                                        |
| ScrollBehavior           | `unset`       | `smooth`       | Sets the scroll behavior (`smooth` or `auto`) for boosted links on page transitions.               |
| DefaultFocusScroll       | `unset`       | `false`        | Specifies whether the focused element should be scrolled into view by default after a swap.          |
| GetCacheBusterParam      | `unset`       | `false`        | Specifies whether to include a cache-busting parameter (`_={timestamp}`) in GET requests.         |
| GlobalViewTransitions    | `unset`       | `false`        | Specifies whether to use the View Transition API (if available) when swapping content globally.    |
| MethodsThatUseUrlParams  | `unset`       | `['get']`      | Specifies HTTP methods whose parameters should be encoded in the URL instead of the request body. |
| SelfRequestsOnly         | `true`        | `false`        | Rizzy specific default: If true, allows only AJAX requests to the same domain. HTMX allows cross-origin. |
| IgnoreTitle              | `unset`       | `false`        | Specifies whether to ignore the `<title>` tag found in new content during swaps.                   |
| ScrollIntoViewOnBoost    | `unset`       | `true`         | Specifies whether the target of a boosted element is scrolled into view after the request.        |


## Conclusion

By following this documentation, you can effectively install Rizzy.Htmx and configure HTMX behavior within your ASP.NET Core application according to your requirements. Remember to place the `<HtmxConfigHeadOutlet />` in your layout to apply the configuration.
