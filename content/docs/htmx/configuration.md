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

This document provides a comprehensive guide on setting up and configuring HTMX within your application using Rizzy.  HTMX 4 introduces a number of changes to configuration keys and attribute behavior, so this guide focuses on the updated API.

To add the `Rizzy.Htmx` NuGet package to your project, follow these steps:

## Installation

### **Install the NuGet Package**

You can add the `Rizzy.Htmx` NuGet package using either Visual Studio or the .NET CLI.

### **Using Visual Studio**
1. Open your project in Visual Studio.
2. Right‑click on the **Dependencies** node in the Solution Explorer.
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
The configuration portion of Rizzy is based on HTMX 4’s head configuration.  You can find more information about HTMX configuration on the official [HTMX documentation site](https://four.htmx.org/docs/features/configuring).
{{< /callout >}}

### Adding HTMX Configuration in `Program.cs`

In `Program.cs`, you can add custom HTMX configurations using the `AddHtmx()` method.  The example below demonstrates a few of the new configuration properties:

```csharp {title="Program.cs"}
using Rizzy.Htmx;

// Add HTMX Configuration Services
builder.Services.AddHtmx(config =>
{
    // Example: set the default settle delay for all swaps (TimeSpan)
    config.DefaultSettleDelay = TimeSpan.FromMilliseconds(100);

    // Example: enable view transitions (requires browsers that support the View Transition API)
    config.Transitions = true;

    // Example: restrict cross‑origin requests (similar to SelfRequestsOnly)
    config.Mode = "same-origin";

    // Example: allow only the rizzy‑streaming extension to run
    config.Extensions = "rizzy-streaming";
});
```

### Setting Configuration in HTML

To include configurations inside the `<head>` tag of your HTML document (usually in your main layout file like `AppLayout.razor`), use the `<HtmxConfigHeadOutlet />` component.  This component renders a `<meta name="htmx-config" ...>` tag containing the serialized JSON of your `HtmxConfig` object (either the default one configured in `Program.cs` or a named one if specified).

```html {title="AppLayout.razor"}
<head>
    ...
    <HtmxConfigHeadOutlet />
    ...
</head>
```

## HTMX Configuration Properties

The table below lists the key configuration properties available in `HtmxConfig` and how they map to HTMX 4.  A Rizzy default of `unset` means Rizzy does not set a specific value by default; in these cases, HTMX's own default value will apply unless you explicitly configure it in `Program.cs` using `AddHtmx(config => ...)`.

| Property                 | Rizzy Default | HTMX 4 Default   | Description |
|--------------------------|---------------|------------------|-------------|
| **History**             | `unset`       | `true`           | Enables history tracking (pushing URLs automatically via `hx-boost` or `hx-push-url`). |
| **DefaultSwap**         | `unset`       | `innerHTML`      | Sets the default swap style (e.g., `innerHTML`, `outerHTML`, `innerMorph`, etc.). |
| **DefaultSettleDelay**  | `unset`       | `1ms`            | Sets the default delay between swapping content and settling it (processing scripts, etc.). |
| **IncludeIndicatorCSS** | `unset`       | `true`           | Specifies whether to include the default CSS for HTMX indicator styles. |
| **IndicatorClass**      | `unset`       | `htmx-indicator` | Sets the class added to elements while a request is active (when using `hx-indicator`). |
| **RequestClass**        | `unset`       | `htmx-request`   | Sets the class added to the element making the request while the request is active. |
| **DefaultTimeout**      | `unset`       | `60000ms`        | Sets the number of milliseconds a request can take before automatically being terminated (`0` means no timeout). |
| **DefaultFocusScroll**  | `unset`       | `false`          | When `true`, the focused element is scrolled into view by default after a swap; can also be controlled via the `focus-scroll` swap modifier. |
| **Transitions**         | `unset`       | `false`          | If set to `true`, HTMX will use the View Transition API when swapping content globally. |
| **Mode**                | `unset`       | `same-origin`    | Controls cross‑origin request mode (`same-origin`, `cors`, or `no-cors`). Replaces the `SelfRequestsOnly` setting from HTMX 2. |
| **ImplicitInheritance** | `unset`       | `false`          | Enables implicit inheritance of HTMX attributes when `true`.  In HTMX 4 attribute inheritance is explicit by default. |
| **NoSwap**              | `unset`       | `[]` (swaps all) | Array or range of HTTP status codes that should **not** be swapped (e.g., `[204, 304, '4xx', '5xx']`). |
| **MorphIgnore**         | `unset`       | `["data-htmx-powered"]` | Attributes to ignore when morphing during `innerMorph` and `outerMorph` swaps. |
| **MorphScanLimit**      | `unset`       | `10`             | Sibling scan limit used during morph operations. |
| **MorphSkip**           | `unset`       | `null`           | CSS selector for elements whose contents should not be morphed. |
| **MorphSkipChildren**   | `unset`       | `null`           | CSS selector for elements whose children should not be morphed. |
| **Extensions**          | `unset`       | `null`           | Comma‑separated list of allowed extension names.  Use this to restrict which HTMX extensions may run (e.g., `"rizzy-streaming"`). |
| **Prefix**              | `unset`       | `null`           | Custom attribute prefix.  HTMX 4 no longer supports `data-hx-` implicitly; set this to `"data-hx-"` if you wish to continue using the `data-hx-` prefix. |
| **LogAll**              | `unset`       | `false`          | Enables logging of all HTMX lifecycle events to the browser console. Useful for debugging. |
| **GenerateScriptNonce** | `false`       | N/A              | Rizzy‑specific: If `true`, uses an `IRizzyNonceProvider` to set `inlineScriptNonce` automatically for CSP compliance. |
| **GenerateStyleNonce**  | `false`       | N/A              | Rizzy‑specific: If `true`, uses an `IRizzyNonceProvider` to set `inlineStyleNonce` automatically for CSP compliance. |

Properties that existed in HTMX 2 such as `DefaultSwapDelay`, `IncludeIndicatorStyles`, `HistoryCacheSize`, `SelfRequestsOnly`, `DisableSelector`, and `WithCredentials` have either been renamed or removed in HTMX 4.  For example, you no longer use `hx-disable` to skip HTMX processing—use the `hx-ignore` attribute instead.  Similarly, the `hx-ext` attribute has been removed; extensions are enabled by including their scripts and, if desired, whitelisting them via the `Extensions` property shown above.

## Conclusion

By following this documentation, you can install Rizzy.Htmx and configure HTMX 4 behavior within your ASP.NET Core application according to your requirements.  Remember to place the `<HtmxConfigHeadOutlet />` in your layout to apply the configuration, and to update any deprecated attributes (for example, replace `hx-disable` with `hx-ignore` and remove any `hx-ext` usage) when migrating existing markup to HTMX 4.