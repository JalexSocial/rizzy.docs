---
title: "Troubleshooting Guide"
description: "Common issues encountered when using Rizzy and how to resolve them."
summary: "Find solutions to frequent problems with HTMX requests, validation, antiforgery, layout rendering, and more in Rizzy."
date: 2024-07-27T10:00:00-05:00 # Adjust date as needed
lastmod: 2024-07-27T10:00:00-05:00 # Adjust date as needed
draft: false
weight: 950 # Position near the end, after Reference
toc: true
seo:
  title: "Rizzy Troubleshooting Guide"
  description: "Solve common problems when working with Rizzy, HTMX, Blazor components, validation, and antiforgery in ASP.NET Core."
---

## Introduction

This guide covers common problems developers might encounter when using Rizzy and provides steps to diagnose and resolve them. Before diving into specific issues, always ensure you've checked:

1.  **Browser Developer Tools:**
    *   **Console:** Look for JavaScript errors (HTMX, Alpine.js, custom scripts).
    *   **Network Tab:** Inspect requests. Check the URL, method, status code (200 OK, 400 Bad Request, 404 Not Found, 500 Internal Server Error), request headers (especially `HX-Request`), and response content/headers.
2.  **Server Logs:** Check your ASP.NET Core application logs for exceptions or warnings.

## Common Issues

### 1. HTMX Requests Not Working or Not Reaching the Server

**Symptoms:**

*   Clicking a button/element with `hx-get`/`hx-post` does nothing.
*   Network tab shows no request being made.
*   Network tab shows a 404 Not Found error for the request URL.

**Diagnosis & Solutions:**

*   **Is HTMX loaded?** Ensure the HTMX JavaScript library is included correctly in your main layout (`AppLayout.razor` or similar) *before* any elements try to use `hx-*` attributes. Check the browser console for errors related to HTMX loading.
*   **Correct URL?** Double-check the URL specified in `hx-get`, `hx-post`, etc. Does it exactly match a defined route in your ASP.NET Core application (MVC action or Minimal API endpoint)? Pay attention to leading slashes (`/`) and case sensitivity if applicable.
*   **Correct HTTP Method?** Does the `hx-*` attribute (`hx-post`) match the method expected by your server endpoint (`[HttpPost]`, `MapPost`)?
*   **Routing Configured?** Verify your ASP.NET Core routing is correctly configured (`MapControllers()`, `MapGet()`, `MapPost()`, etc.) in `Program.cs`.

### 2. HTMX Request Successful (200 OK) but UI Doesn't Update Correctly

**Symptoms:**

*   Network tab shows a 200 OK response, but the target element doesn't change.
*   The wrong part of the page is updated.
*   The entire page seems to reload instead of just a partial update.

**Diagnosis & Solutions:**

*   **Check Response Content:** Examine the 'Response' tab in the Network tools for the successful request. Is the server returning the expected HTML fragment? If it's returning a full HTML page, see Issue #5 below. If it's returning JSON or something else unexpected, ensure your controller action is returning `PartialView<YourComponent>()` or similar Rizzy result.
*   **Check `hx-target`:** Is the CSS selector in `hx-target` correct and does it uniquely identify an element *already present* in the DOM *before* the swap occurs? Use the browser's element inspector to verify the selector. Common mistakes include typos or targeting an element that doesn't exist yet.
*   **Check `hx-swap`:** Is the `hx-swap` style appropriate? `innerHTML` (default) replaces the content *inside* the target, while `outerHTML` replaces the target element itself. Other styles (`beforeend`, `afterend`, etc.) insert content relative to the target. Ensure the chosen style matches how your returned HTML fragment is structured. See [SwapStyle docs]({{<ref "/docs/htmx/swapstyle.md">}}).
*   **HTMX Errors:** Check the browser console for any specific errors reported by HTMX during the swap process.
*   **Valid HTML Fragment:** Ensure the HTML returned by the server is valid. Malformed HTML can sometimes cause swapping to fail silently or partially.

### 3. Antiforgery Validation Fails (400 Bad Request or Similar)

**Symptoms:**

*   POST, PUT, DELETE, or PATCH requests made via HTMX fail with a 400 Bad Request status code.
*   Server logs might indicate an antiforgery token validation failure.

**Diagnosis & Solutions:**

*   **Middleware Order:** Ensure `app.UseAntiforgery()` is present in `Program.cs` and placed *after* `app.UseRouting()` and any authentication/authorization middleware (`app.UseAuthentication(); app.UseAuthorization();`).
*   **Token Present in Form/Page:**
    *   For standard form posts, ensure you have `<AntiforgeryToken />` inside your Blazor `EditForm`.
    *   For general HTMX requests needing protection (often non-GET), ensure the antiforgery token is available to HTMX. The easiest way with Rizzy is often to:
        *   Configure `RizzyConfig.AntiforgeryStrategy = AntiforgeryStrategy.GenerateTokensPerPage;` in `Program.cs`.
        *   Include `<HtmxAntiforgeryScript />` in your main layout (`AppLayout.razor`). This component injects JavaScript that automatically adds the necessary token to HTMX requests based on the configuration in the `htmx-config` meta tag.
    *   Verify the `htmx-config` meta tag (rendered by `<HtmxConfigHeadOutlet />`) contains the correct `antiforgery` configuration (header name, form field name, cookie name). See [HTMX Configuration]({{<ref "/docs/htmx/configuration.md">}}).
*   **`[ValidateAntiForgeryToken]` Attribute:** Ensure the controller action or Minimal API endpoint being called has the `[ValidateAntiForgeryToken]` attribute (or uses convention-based filters if configured globally).
*   **Cookie Present:** Check browser developer tools (Application -> Cookies) to ensure the antiforgery cookie (usually `.AspNetCore.Antiforgery.*`) is present.

### 4. Validation Errors Are Not Displayed

**Symptoms:**

*   Form submission fails server-side validation (`ModelState.IsValid` is false).
*   The controller returns the form component view again.
*   No validation messages appear next to the fields or in the summary.

**Diagnosis & Solutions:**

*   **Correct Components Used?**
    *   Is the form wrapped in an `<EditForm Model="@YourModel">`?
    *   Is `<DataAnnotationsValidator />` placed *inside* the `EditForm`?
    *   Is `<RzInitialValidator />` placed *inside* the `EditForm` (usually right after `DataAnnotationsValidator`)? This component is crucial for transferring `ModelState` errors to the `EditContext`.
    *   Are you using `<RzValidationMessage For="@(() => YourModel.PropertyName)" />` for field-specific messages?
    *   Are you using `<RzValidationSummary />` for a summary?
*   **Check Response:** Inspect the HTML response in the Network tab. Does it contain the expected validation message elements (e.g., `<div class="validation-message field-validation-error" ...>Your error</div>`)?
*   **`ModelState` Propagation:** Are you using `RzController` or `IRizzyService` methods (`View<T>`, `PartialView<T>`)? These automatically pass `ModelState` down. If you are manually rendering, ensure you pass the `ModelStateDictionary` as a parameter to `RzPage` or `RzPartial`.
*   **Client-Side Validation (Optional):** If you expect *client-side* validation messages *before* submitting, ensure:
    *   You have included a compatible JavaScript validation library (like the `aspnet-validation.js` included with RizzyUI/Rizzy or jQuery Unobtrusive Validation).
    *   The `RzInput*` components are generating the necessary `data-val-*` attributes (inspect the rendered HTML). This relies on `DataAnnotationsProcessor` and having Data Annotation attributes (`[Required]`, etc.) on your model.

### 5. Full Layout Renders During HTMX Partial Updates

**Symptoms:**

*   An HTMX request intended to update only a small part of the page causes the entire site layout (header, footer, nav) to be rendered inside the target element.

**Diagnosis & Solutions:**

*   **Correct Rizzy Configuration:** In `Program.cs`, ensure:
    *   `config.RootComponent = typeof(HtmxApp<YourAppLayout>);`
    *   `config.DefaultLayout = typeof(HtmxLayout<YourMainLayout>);`
    (Replace `YourAppLayout` and `YourMainLayout` with your actual layout component types). These wrappers are essential for detecting HTMX requests and suppressing the full layout rendering. See [Getting Started]({{<ref "/docs/introduction/getting-started.md">}}).
*   **Is it an HTMX Request?** Verify the request includes the `HX-Request: true` header in the Network tab. If not, HTMX isn't making the request correctly, or something is stripping the header.
*   **Correct Rendering Method?** Are you calling `PartialView<YourComponent>()` from your controller/endpoint for partial updates? While `View<YourComponent>()` *should* also work correctly with the `HtmxLayout` wrapper, `PartialView` is generally preferred for fragments as it explicitly uses an empty layout by default.

### 6. Out-of-Band (OOB) Swaps Not Working

**Symptoms:**

*   An HTMX response is supposed to update multiple elements (the main target and others via OOB), but only the main target updates.

**Diagnosis & Solutions:**

*   **Check Response HTML:** Inspect the raw HTML response in the Network tab. Does it contain elements with the `hx-swap-oob="true"` (or other swap styles) attribute? These are the OOB elements.
*   **Target IDs Exist:** Does the `id` attribute of the OOB element in the response match the `id` of an element *already present* in the main document *before* the swap happens? OOB swaps target existing elements by ID.
*   **`<HtmxSwapContent />` Present:** Have you included the `<HtmxSwapContent />` component somewhere in your main layout (e.g., `AppLayout.razor`)? This component is responsible for rendering content added via the `IHtmxSwapService`. See [Out of Band Swapping]({{<ref "/docs/htmx/swaps.md">}}).
*   **Server Logic:** Ensure your server-side code (e.g., controller action) is correctly calling `IHtmxSwapService.AddSwappableComponent`, `AddSwappableFragment`, etc., *during* the HTMX request lifecycle.

### 7. Streaming Rendering (`[StreamRendering]`) Issues with HTMX

**Symptoms:**

*   A component with `[StreamRendering]` loads initially via HTMX, showing a placeholder ("Loading...").
*   The final content never appears, or JavaScript errors occur related to Blazor updates.

**Diagnosis & Solutions:**

*   **Extension Enabled?** Have you added `hx-ext="rizzy-streaming"` to a high-level element, typically the `<body>` tag in your main layout (`AppLayout.razor`)? This extension is required to coordinate Blazor's streaming updates with HTMX swaps. See [Streaming Rendering with HTMX]({{<ref "/docs/htmx/streaming.md">}}).
*   **Check Console:** Look for specific errors from Blazor's streaming rendering JavaScript or the `rizzy-streaming` extension.

## Still Stuck?

If you've worked through these steps and are still facing issues:

*   Simplify your scenario to isolate the problem.
*   Double-check the relevant Rizzy and HTMX documentation.
*   Consider creating a minimal reproducible example.
*   Seek help from the community (e.g., project's GitHub Discussions/Issues, relevant forums). Provide clear details about the problem, what you've tried, relevant code snippets, and browser/server logs if possible.