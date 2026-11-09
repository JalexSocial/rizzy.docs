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

`Rizzy.Htmx` is installed with the `Rizzy` package. Install it on its own only if you use the htmx helpers without Rizzy's components:

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

`AddRizzy()` already registers htmx support with htmx's defaults. To change the configuration, call `AddHtmx()` with a delegate (before or after `AddRizzy()`; repeated calls are safe). The example below demonstrates a few of the configuration properties:

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

    // Example: enable htmx extensions; <RzScripts /> loads them and Rizzy keeps the
    // htmx.config.extensions allow-list in step (see the Extensions page)
    config.UseExtensions(HtmxExtension.Preload);
    config.RestrictExtensions = true;
});
```

### Setting Configuration in HTML

The configuration reaches the browser as a `<meta name="htmx-config" ...>` tag rendered by **`<RzHeadOutlet />`**, which you place in the `<head>` of your root layout instead of Blazor's `<HeadOutlet />`. It must come **before** the htmx script, because htmx reads the tag once, when the script loads.

```html {title="AppLayout.razor"}
<head>
    ...
    <RzHeadOutlet />
    <RzScripts />
</head>
```

`RzHeadOutlet` renders `HeadOutlet` followed by `HtmxConfigHeadOutlet`, the component that produces the tag. Besides your settings, the tag carries Rizzy's `antiforgery` settings (header name, form field name and the current request token) and `rizzyVersion`. Rizzy 5 added the tag through `<HeadContent>`, but any page with its own `<HeadContent>` replaced it; `RzHeadOutlet` cannot be overridden that way.

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
| **DefaultFocusScroll**  | `unset`       | `false`          | When `true`, the focused element is scrolled into view by default after a swap; can also be controlled via the `focusScroll` swap modifier. |
| **Transitions**         | `unset`       | `false`          | If set to `true`, HTMX will use the View Transition API when swapping content globally. |
| **Mode**                | `unset`       | `same-origin`    | Controls cross‑origin request mode (`same-origin`, `cors`, or `no-cors`). Replaces the `SelfRequestsOnly` setting from HTMX 2. |
| **ImplicitInheritance** | `unset`       | `false`          | Enables implicit inheritance of HTMX attributes when `true`.  In HTMX 4 attribute inheritance is explicit by default. |
| **NoSwap**              | `unset`       | `[204, 304]`     | HTTP status codes (or ranges such as `"4xx"`) that should **not** be swapped. htmx 4 swaps 4xx and 5xx responses by default, which Rizzy's validation support relies on (see [Validation]({{<ref "/docs/forms/validation.md">}})). Set `[204, 304, "4xx", "5xx"]` for htmx 2 behavior. |
| **MorphIgnore**         | `unset`       | `["data-htmx-powered"]` | Attributes to ignore when morphing during `innerMorph` and `outerMorph` swaps. |
| **MorphScanLimit**      | `unset`       | `10`             | Sibling scan limit used during morph operations. |
| **MorphSkip**           | `unset`       | `null`           | CSS selector for elements whose contents should not be morphed. |
| **MorphSkipChildren**   | `unset`       | `null`           | CSS selector for elements whose children should not be morphed. |
| **Extensions**          | `unset`       | `null`           | Comma‑separated allow-list of extension names. Prefer `UseExtensions(...)` and `RestrictExtensions` (below); when you set this yourself, Rizzy adds its own extensions and every enabled one to it. See [Extensions]({{<ref "/docs/htmx/extensions.md">}}). |
| **Prefix**              | `unset`       | `"data-hx-"`     | An alternative attribute prefix. htmx 4 always accepts `hx-` and also accepts this prefix, so `data-hx-` attributes work out of the box. |
| **LogAll**              | `unset`       | `false`          | Enables logging of all HTMX lifecycle events to the browser console. Useful for debugging. |
| **AllowEmptySwapAfterOOB** | `unset`    | `false`          | When `true`, an empty main response is still swapped after out-of-band content was processed. |
| **MetaCharacter**       | `unset`       | `:`              | A character htmx uses instead of `:` in attribute and event names (for example `-` to write `hx-on-click`), for templating systems that do not allow colons. |
| **GenerateScriptNonce** | `false`       | N/A              | Rizzy‑specific: If `true`, sets htmx's `inlineScriptNonce` to the page nonce. htmx then stamps that nonce on **every** script it inserts, including injected ones, which defeats a CSP. Leave it off and let Rizzy's `rizzy-nonce` extension handle scripts (see [Content Security Policy]({{<ref "/docs/introduction/contentsecurity.md">}})). |
| **UseExtensions(...)**  | none          | N/A              | Rizzy‑specific: enables htmx extensions (`HtmxExtension.Sse`, `Preload`, ...). `<RzScripts />` loads them; their registered names join the allow-list whenever one is in use. |
| **RestrictExtensions**  | `false`       | N/A              | Rizzy‑specific: when `true`, the allow-list contains only Rizzy's own extensions, the enabled ones and any listed in `Extensions`. |
| **Scripts**             | jsDelivr, minified, SRI | N/A    | Rizzy‑specific: where `<RzScripts />` loads htmx and its extensions from (`HtmxScriptOptions`). The Rizzy script URL is `RizzyConfig.ClientScriptUrl`. |
| **Set(key, value)**     | none          | N/A              | Rizzy‑specific: writes any other `htmx.config` key, typically an extension's settings (`Set("sse", new { reconnect = true })`). Keys a property already writes are rejected. |
| **RizzyDiagnostics**    | enabled       | N/A              | Rizzy‑specific: set to `false` to silence the console warnings rizzy.js logs for a misconfigured page (missing or invalid meta tag, or a server/client version mismatch). |

Properties that existed in HTMX 2 such as `DefaultSwapDelay`, `IncludeIndicatorStyles`, `HistoryCacheSize`, `SelfRequestsOnly`, `DisableSelector`, and `WithCredentials` have either been renamed or removed in HTMX 4.  For example, you no longer use `hx-disable` to skip HTMX processing—use the `hx-ignore` attribute instead.  Similarly, the `hx-ext` attribute has been removed; extensions are enabled by including their scripts and, if desired, whitelisting them via the `Extensions` property shown above.

## Conclusion

By following this documentation, you can install Rizzy.Htmx and configure HTMX 4 behavior within your ASP.NET Core application according to your requirements.  Remember to render `<RzHeadOutlet />` in your root layout, before the htmx script, to apply the configuration, and to update any deprecated attributes (for example, replace `hx-disable` with `hx-ignore` and remove any `hx-ext` usage) when migrating existing markup to HTMX 4.