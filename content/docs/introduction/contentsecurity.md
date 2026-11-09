---

title: "Content Security Policy"
description: ""
summary: ""
date: 2025-01-16T12:51:13-05:00
lastmod: 2025-01-16T12:51:13-05:00
draft: false
weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This document provides a brief overview of CSP, the use of nonces for securing inline scripts and styles, and how to use the `IRizzyNonceProvider` for nonce management.

## What is CSP?

A Content Security Policy (CSP) is a security mechanism that helps prevent cross-site scripting (XSS) and other code injection attacks by restricting the sources from which content (e.g., scripts, styles, images) can be loaded. A typical CSP might look like this:

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; base-uri 'self'; script-src 'self' 'nonce-<REPLACE_WITH_ONE_TIME_USE_RANDOM_STRING>'; style-src 'self' 'nonce-<REPLACE_WITH_ONE_TIME_USE_RANDOM_STRING>';" />
```

## Using Nonces with Inline Content

Nonces (numbers used once) allow inline content to execute when its nonce matches the value specified in the CSP header. The general workflow is:

1. **Generate Nonces:** Secure, random nonce values are created.
2. **Inject Nonces:** Nonce values are applied as attributes to inline `script` or `style` elements.
3. **CSP Enforcement:** The server can send a CSP header or meta tag that includes these nonce values or they can be included within a meta tag inside the document, and only inline content tagged with the correct nonce is executed.

## Generating Nonces with Rizzy

Rizzy provides a basic service for generating nonce values that can be injected into any component as you like. 

### IRizzyNonceProvider

| Member                     | Type               | Description                                                                                                                                                                                                                      |
|----------------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **GetNonce()** | `string`           | Retrieves (or generates) the nonce value                                                                |


## Usage in a Blazor Application

Below is a simplified example of using the nonce values in a Blazor component. Nonce values are injected into the CSP meta tag and applied to inline script and stylesheet links using the `GetNonce()` method.

```razor
@using Rizzy.Htmx

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="Content-Security-Policy" 
          content="default-src 'self'; 
                   connect-src 'self' localhost:* http://localhost:* ws://localhost:* wss://localhost:*; 
                   script-src 'self' 'nonce-@NonceProvider?.GetNonce()'; 
                   style-src 'self' 'nonce-@NonceProvider?.GetNonce()';">
    <!-- Link to stylesheets with nonce attributes -->
    <link nonce="@NonceProvider?.GetNonce()" rel="stylesheet" href="/css/app.css" />

    <RzHeadOutlet />

    <!-- Link to scripts with nonce attributes -->
    <script defer nonce="@NonceProvider?.GetNonce()" src="https://cdn.jsdelivr.net/npm/@@alpinejs/csp@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
    <Routes />
</body>
</html>

@code {
    [Inject] 
	private IRizzyNonceProvider? NonceProvider { get; set; } = null!;
}
```

## Scripts in htmx responses

Every Rizzy response is rendered with its own nonce, and Rizzy sends it to htmx requests in the `HX-Nonce` response header. A `<script nonce="...">` that your component renders into an htmx fragment therefore carries the **response's** nonce, while the browser only trusts the nonce the **page** was loaded with.

The `rizzy-nonce` extension (part of rizzy.js) bridges the two without weakening the policy:

- Scripts and styles rendered by the server with the response nonce are given the page nonce, so they run.
- Markup without a nonce stays without one, so an injected `<script>` is still blocked by the browser.
- A copy of the page nonce found in a response is removed: the server never knows the page nonce, so its presence means it was stolen and echoed back.

The response is never parsed or re-serialized, so fragments such as table rows swap exactly as they would without Rizzy. On pages without a nonce the extension does nothing.

rizzy.js reads the page nonce from the `nonce` property of a `<script nonce>` element, so give the htmx and Rizzy script tags the page nonce.

### A complete setup

```csharp {title="Program.cs"}
// Send a nonce-based policy with every response. Register it before the endpoints run.
app.Use(async (context, next) =>
{
    var nonce = context.RequestServices.GetRequiredService<IRizzyNonceProvider>().GetNonce();
    context.Response.Headers.ContentSecurityPolicy =
        $"script-src 'nonce-{nonce}'; object-src 'none'; base-uri 'self'";
    await next();
});
```

```razor {title="AppLayout.razor"}
@inherits LayoutComponentBase
@inject Rizzy.Htmx.IRizzyNonceProvider NonceProvider

<!DOCTYPE html>
<html lang="en">
<head>
    <RzHeadOutlet />
    <script src="https://cdn.jsdelivr.net/npm/htmx.org@4.0.1/dist/htmx.min.js" integrity="sha384-Qp9rdC8H7EqOoX+nR0P3RPG2Noji+qdwJlGpfzwQJsfOpp3sGwIdSP9xO3+UlEhn"
            crossorigin="anonymous" nonce="@NonceProvider.GetNonce()"></script>
    <script src="_content/Rizzy/js/rizzy.js" nonce="@NonceProvider.GetNonce()"></script>
</head>
<body>
    @Body
</body>
</html>
```

A component can then render a script into an htmx fragment:

```razor
@inject Rizzy.Htmx.IRizzyNonceProvider NonceProvider

<div id="chart"></div>
<script nonce="@NonceProvider.GetNonce()">
    drawChart(document.getElementById("chart"));
</script>
```

Inline event handlers (`onclick="..."`) and `hx-on:*` attributes are inline script too; a strict `script-src` blocks them. Move that code into nonced scripts or files. The Rizzy demo app (`src/RizzyDemo`) runs with this policy and includes a page that shows a server-rendered script running while an injected one is blocked.

{{< callout context="caution" title="Leave GenerateScriptNonce off" icon="alert-triangle" >}}
`HtmxConfig.GenerateScriptNonce = true` sets htmx's `inlineScriptNonce`, which makes htmx stamp the page nonce on **every** script it inserts, including injected ones. That defeats the policy, and `rizzy-nonce` makes it unnecessary. (Rizzy 6 removed `GenerateStyleNonce`: htmx 4 has no style nonce setting.)
{{< /callout >}}

## Summary

- **CSP:** Enforces permitted sources for content. Nonces ensure that only inline content with the correct one-time value is executed.
- **Nonce Generation:** Nonces are generated using secure random bytes and available via the IRizzyNonceProvider scoped service
