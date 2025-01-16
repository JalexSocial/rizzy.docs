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

This document provides a brief overview of CSP, the use of nonces for securing inline scripts, styles, and other content, and how to use the `IRizzyNonceProvider` for nonce management.

## What is CSP?

A Content Security Policy (CSP) is a security mechanism that helps prevent cross-site scripting (XSS) and other code injection attacks by restricting the sources from which content (e.g., scripts, styles, images) can be loaded. A typical CSP might look like this:

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; base-uri 'self'; script-src 'self' 'nonce-<REPLACE_WITH_ONE_TIME_USE_RANDOM_STRING>'; style-src 'self' 'nonce-<REPLACE_WITH_ONE_TIME_USE_RANDOM_STRING>';" />
```

## Using Nonces with Inline Content

Nonces (numbers used once) allow inline content to execute when its nonce matches the value specified in the CSP header. The general workflow is:

1. **Generate Nonces:** Secure, random nonce values are created.
2. **Inject Nonces:** Nonce values are applied as attributes to inline `<script>`, `<style>`, or other elements.
3. **CSP Enforcement:** The server sends a CSP header or meta tag that includes these nonce values, and only inline content tagged with the correct nonce is executed.

## Generating and Validating Nonces with Rizzy

Rizzy provides an interface, `IRizzyNonceProvider`, for generating nonce values. The provider uses a cryptographically secure HMAC key to generate and validate nonce tokens. An HMAC key must be provided during application startup or can be generated automatically.

### IRizzyNonceProvider

| Member                     | Type               | Description                                                                                                                                                                                                                      |
|----------------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **GetNonceValues()**       | `RizzyNonceValues` | Retrieves all nonce values for the current HTTP request. If they have not been generated for this request, new nonce values are generated, cached, and returned.                                                             |
| **GetNonceFor(NonceType)** | `string`           | Retrieves (or generates) the nonce value for a given nonce type. For example, `GetNonceFor(NonceType.Script)` returns the nonce used in inline script elements.                                                                |

### NonceType Enumeration

The `NonceType` enumeration defines the supported types of nonce values. These are used to specify the nonce for various content types in the CSP and inline elements.

| Enum Value | Description                                                       |
|------------|-------------------------------------------------------------------|
| **Script** | Nonce for inline `<script>` tags.                                 |
| **Style**  | Nonce for inline `<style>` tags.                                  |
| **Font**   | Nonce for font requests.                                          |
| **Image**  | Nonce for image elements.                                         |
| **Connect**| Nonce for connect requests (e.g., WebSocket connections, AJAX).     |

## HMAC Key Configuration

Nonces require an HMAC key for generation and validation. Configure the key on application startup (the key must be a Base64-encoded string at least 256 bits in length):

```csharp
builder.AddRizzy(config =>
{
    config.NonceHMACKey = "Your_Base64_Encoded_HMAC_Key";
});
```

For distributed environments, ensure that all instances share the same HMAC key. Otherwise, the key can be generated automatically during startup.

### Generating a Secure HMAC Key

Below is an example of generating a secure Base64-encoded HMAC key:

```csharp
/// <summary>
/// Generates a secure HMAC key using a cryptographically secure random number generator.
/// </summary>
/// <param name="keySizeInBytes">Size of the key in bytes (e.g., 32 for 256-bit).</param>
/// <returns>Base64-encoded HMAC key.</returns>
private byte[] GenerateSecureHmacKey(int keySizeInBytes = 32)
{
    byte[] key = new byte[keySizeInBytes];
    RandomNumberGenerator.Fill(key);
    return key;
}

private string GetBase64Key() => Convert.ToBase64String(GenerateSecureHmacKey());
```

## Usage in a Blazor Application (App.razor)

Below is a simplified example of using the nonce values in a Blazor component. Nonce values are injected into the CSP meta tag and applied to inline script and stylesheet links using the `GetNonceFor(NonceType.X)` methods.

```razor
@using Rizzy.Nonce

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="Content-Security-Policy" 
          content="default-src 'self'; 
                   connect-src 'self' localhost:* http://localhost:* ws://localhost:* wss://localhost:*; 
                   script-src 'self' 'nonce-@NonceProvider.GetNonceFor(NonceType.Script)'; 
                   style-src 'self' 'nonce-@NonceProvider.GetNonceFor(NonceType.Style)';">
    <!-- Link to stylesheets with nonce attributes -->
    <link nonce="@NonceProvider.GetNonceFor(NonceType.Style)" rel="stylesheet" href="/css/app.css" />

    <HeadOutlet />

    <!-- Link to scripts with nonce attributes -->
    <script defer nonce="@NonceProvider.GetNonceFor(NonceType.Script)" src="https://cdn.jsdelivr.net/npm/@@alpinejs/csp@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
    <Routes />
</body>
</html>

@code {
    [Inject] private IRizzyNonceProvider NonceProvider { get; set; } = null!;
}
```

## Summary

- **CSP:** Enforces permitted sources for content. Nonces ensure that only inline content with the correct one-time value is executed.
- **Nonce Generation:** Nonces are generated using secure random bytes combined with an HMAC signature. An HMAC key is required for this process.
- **IRizzyNonceProvider:** Provides nonce values for the current request; use `GetNonceFor(NonceType.X)` to retrieve a specific nonce.
- **NonceType Enumeration:** Defines supported nonce types—Script, Style, Font, Image, and Connect.
- **HMAC Key:** Must be configured (or generated) and shared in distributed environments.

This implementation secures web applications by ensuring that only inline elements with validated, type-specific nonces are executed, thereby reducing the risk of XSS attacks.
