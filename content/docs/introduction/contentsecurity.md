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

                           |

## Usage in a Blazor Application (App.razor)

Below is a simplified example of using the nonce values in a Blazor component. Nonce values are injected into the CSP meta tag and applied to inline script and stylesheet links using the `GetNonceFor(NonceType.X)` methods.

```razor
@using Rizzy

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

    <HeadOutlet />

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

## Usage with HTMX to Automatically Update HTMX Configuration with Nonce Values

Configure HTMX to use the IRizzyNonceProvider implementation to correctly configure nonce values in the HTMX configuration.  

{{< callout context="caution" title="Warning" icon="utline/alert-triangle" >}}
These configuration options will set the inlineScriptNonce and inlineStyleNonce settings. These settings cause nonce values to be injected into any received content from an htmx request and will negate the use of Content Security Policies.  Please use with extreme caution.
{{< /callout >}}


```razor
builder.Services.AddHtmx(config =>
    {
        config.GenerateScriptNonce = true;  
        config.GenerateStyleNonce = true;
    })
```


## Summary

- **CSP:** Enforces permitted sources for content. Nonces ensure that only inline content with the correct one-time value is executed.
- **Nonce Generation:** Nonces are generated using secure random bytes and available as an extension method via HttpContext
