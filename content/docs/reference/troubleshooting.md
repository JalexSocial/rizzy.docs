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
    *   **Network Tab:** Inspect requests. Check the URL, method, status code (200 OK, 400 Bad Request, 404 Not Found, 500 Internal Server Error), request headers (especially `HX-Request`), and response content/headers.
2.  **Server Logs:** Check your ASP.NET Core application logs for exceptions or warnings.

## Common Issues

### 1. HTMX Requests Not Working or Not Reaching the Server

**Symptoms:**

*   Clicking a button/element with `hx-get`/`hx-post` does nothing.
*   Network tab shows no request being made.
*   Network tab shows a 404 Not Found error for the request URL.

**Diagnosis & Solutions:**

*   **Is HTMX loaded?** Ensure the HTMX JavaScript library is included correctly in your main layout (`AppLayout.razor` or similar) *before* any elements try to use `hx-*` attributes. Check the browser console for errors related to HTMX loading.
*   **Correct URL?** Double-check the URL specified in `hx-get`, `hx-post`, etc. Does it exactly match a defined route in your ASP.NET Core application (MVC action or Minimal API endpoint)? Pay attention to leading slashes (`/`) and case sensitivity if applicable.
*   **Correct HTTP Method?** Does the `hx-*` attribute (`hx-post`) match the method expected by your server endpoint (`[HttpPost]`, `MapPost`)?
*   **Routing Configured?** Verify your ASP.NET Core routing is correctly configured (`MapControllers()`, `MapGet()`, `MapPost()`, etc.) in `Program.cs`.

### 2. HTMX Request Successful (200 OK) but UI Doesn't Update Correctly

**Symptoms:**

*   Network tab shows a 200 OK response, but the target element doesn't change.
*   The wrong part of the page is updated.
*   The entire page seems to reload instead of just a partial update.

**Diagnosis & Solutions:**

*   **Check Response Content:** Examine the 'Response' tab in the Network tools for the successful request. Is the server returning the expected HTML fragment? If it's returning a full HTML page, see Issue #5 below. If it's returning JSON or something else unexpected, ensure your controller action is returning `PartialView<YourComponent>()` or similar Rizzy result.
*   **Check `hx-target`:** Is the CSS selector in `hx-target` correct and does it uniquely identify an element *already present* in the DOM *before* the swap occurs? Use the browser's element inspector to verify the selector. Common mistakes include typos or targeting an element that doesn't exist yet.
*   **Check `hx-swap`:** Is the `hx-swap` style appropriate? `innerHTML` (default) replaces the content *inside* the target, while `outerHTML` replaces the target element itself. Other styles (`beforeend`, `afterend`, etc.) insert content relative to the target. Ensure the chosen style matches how your returned HTML fragment is structured. See [SwapStyle docs]({{<ref "/docs/htmx/swapstyle.md">}}).
*   **HTMX Errors:** Check the browser console for any specific errors reported by HTMX during the swap process.
*   **Valid HTML Fragment:** Ensure the HTML returned by the server is valid. Malformed HTML can sometimes cause swapping to fail silently or partially.

### 3. Antiforgery Validation Fails (400 Bad Request or Similar)

**Symptoms:**

*   POST, PUT, DELETE, or PATCH requests made via HTMX fail with a 400 Bad Request status code.
*   Server logs might indicate an antiforgery token validation failure.

**Diagnosis & Solutions:**

*   **Middleware Order:** Ensure `app.UseAntiforgery()` is present in `Program.cs` and placed *after* `app.UseRouting()` and any authentication/authorization middleware (`app.UseAuthentication(); app.UseAuthorization();`).
*   **Token on the page:** rizzy.js reads the token from the `<meta name="htmx-config">` tag and sends it in a header (`RequestVerificationToken`) on every htmx request that isn't a GET. Check that:
    *   Your root layout renders `<RzHeadOutlet />` (not `<HeadOutlet />`) before the htmx script. If the tag is missing, rizzy.js logs a console warning that says so. Pages with their own `<HeadContent>` are fine.
    *   `<RzScripts />` (or your own htmx and `_content/Rizzy/js/rizzy.js` script tags, htmx first, no `type="module"`) is in the root layout.
    *   The meta tag's `antiforgery` entry has a `requestToken` (it is generated per page with the default `RizzyConfig.AntiforgeryStrategy`).
    *   The request in the Network tab carries the `RequestVerificationToken` header.
*   **MVC registration:** `[ValidateAntiForgeryToken]` needs `AddControllersWithViews()` (or `AddMvcCore().AddViews()`). With `AddControllers()` alone the attribute's filter is not registered.
*   **Minimal APIs:** endpoints that bind form data are validated by `UseAntiforgery()`; others need `.WithMetadata(new RequireAntiforgeryTokenAttribute())` or `IAntiforgery.ValidateRequestAsync`.
*   **Cookie Present:** Check browser developer tools (Application → Cookies) to ensure the antiforgery cookie (usually `.AspNetCore.Antiforgery.*`) is present.

### 4. Validation Errors Are Not Displayed

**Symptoms:**

*   Form submission fails server-side validation (`ModelState.IsValid` is false).
*   The controller returns the form component view again.
*   No validation messages appear next to the fields or in the summary.

**Diagnosis & Solutions:**

*   **Correct Components Used?**
    *   Is the form wrapped in an `<EditForm Model="@YourModel">`?
    *   Is `<DataAnnotationsValidator />` placed *inside* the `EditForm`?
    *   Is `<RzModelStateProvider />` placed *inside* the `EditForm`? It copies `ModelState` errors into the `EditContext`. (`RzInitialValidator` only runs the Data Annotations validation; it does not read `ModelState`.)
    *   Are you using `<RzValidationMessageBase For="@(() => YourModel.PropertyName)" />` for field‑specific messages?
    *   Are you using `<RzValidationSummaryBase />` for a summary?
*   **Check Response:** Inspect the HTML response in the Network tab. Does it contain the expected validation message elements (e.g., `<div class="validation-message field-validation-error" …>Your error</div>`)?
*   **`ModelState` Propagation:** `RzController`'s `View<T>`/`PartialView<T>` pass the controller's `ModelState` automatically. `IRizzyService` (minimal APIs) has no `ModelState` of its own: pass a `ModelStateDictionary` to `View`/`PartialView`.
*   **Was the response swapped?** If you return status 422 (`Response.Htmx().ValidationFailed()`), make sure `HtmxConfig.NoSwap` does not include `"4xx"`, or route the response with `hx-status:422="..."`.
*   **Client‑Side Validation (Optional):** If you expect *client‑side* validation messages *before* submitting, ensure:
    *   You have included a compatible JavaScript validation library (such as the `aspnet-validation` script included with RizzyUI, or jQuery Unobtrusive Validation). The Rizzy client script does not validate.
    *   The `RzInput*Base` components are generating the necessary `data-val-*` attributes (inspect the rendered HTML). This relies on `DataAnnotationsProcessor` and having Data Annotation attributes (`[Required]`, etc.) on your model.

### 5. Full Layout Renders During HTMX Partial Updates

**Symptoms:**

*   An HTMX request intended to update only a small part of the page causes the entire site layout (header, footer, nav) to be rendered inside the target element.

**Diagnosis & Solutions:**

*   **Correct Rizzy Configuration:** In `Program.cs`, ensure:
    *   `config.RootComponent = typeof(HtmxApp<YourAppLayout>);`
    *   `config.DefaultLayout = typeof(HtmxLayout<YourMainLayout>);`
    (Replace `YourAppLayout` and `YourMainLayout` with your actual layout component types). These wrappers are essential for detecting HTMX requests and suppressing the full layout rendering. See [Getting Started]({{<ref "/docs/introduction/getting-started.md">}}).
*   **Is it an HTMX Request?** Verify the request includes the `HX-Request: true` header in the Network tab. If not, HTMX isn't making the request correctly, or something is stripping the header.
*   **Request type:** `View<T>` skips the layouts only for htmx requests that target one element (`HX-Request-Type: partial`). Boosted links that swap the whole `<body>`, `hx-select` and back/forward restores send `HX-Request-Type: full` and get the full page on purpose. Give boosted links an `hx-target` (for example `hx-target:inherited="article"`), or use `PartialView<T>()` for endpoints that only ever return fragments.

### 6. Out‑of‑Band (OOB) Swaps Not Working

**Symptoms:**

*   An HTMX response is supposed to update multiple elements (the main target and others via OOB), but only the main target updates.

**Diagnosis & Solutions:**

*   **Check Response HTML:** Inspect the raw HTML response in the Network tab. Does it contain elements with the `hx-swap-oob="true"` (or other swap styles) attribute? These are the OOB elements.
*   **Target IDs Exist:** Does the `id` attribute of the OOB element in the response match the `id` of an element *already present* in the main document *before* the swap happens? OOB swaps target existing elements by ID.
*   **Rendered once:** `View<T>`/`PartialView<T>` render the queued content automatically. If you also placed `<HtmxSwapContent />` in a layout, remove it (the content would be rendered twice). See [Out of Band Swapping]({{<ref "/docs/htmx/swaps.md">}}).
*   **Server Logic:** Ensure your server‑side code (e.g., controller action) is correctly calling `IHtmxSwapService.AddSwappableComponent`, `AddSwappableFragment`, etc., *during* the HTMX request lifecycle.

### 7. Streaming Rendering (`[StreamRendering]`) Issues with HTMX

**Symptoms:**

*   A component with `[StreamRendering]` loads initially via HTMX, showing a placeholder ("Loading...").
*   The final content never appears, or JavaScript errors occur related to Blazor updates.

**Diagnosis & Solutions:**

*   **Rizzy script loaded?** htmx 4 has no `hx-ext`; the Rizzy client script registers `rizzy-streaming` when it loads. Load htmx first, then `<script src="_content/Rizzy/js/rizzy.js"></script>` (no `type="module"`).
*   **Extension allow-list:** if you set `HtmxConfig.Extensions`, it must include `rizzy-streaming` (and Rizzy's other extensions: `rizzy-antiforgery, rizzy-nonce, rizzy-confirm`).
*   **Content appears only at the end:** `PartialView<T>` sends a bare fragment, so the client waits for the whole stream. Use `View<T>` for progressive streaming. See [Streaming Rendering with HTMX]({{<ref "/docs/htmx/streaming.md">}}).
*   **Check Console:** Look for specific errors from Blazor's streaming rendering JavaScript or the `rizzy-streaming` extension.

### 8. An htmx extension does nothing

htmx skips an extension silently when its script did not load or when `htmx.config.extensions` does not name it (by its registered name: `sse`, not `hx-sse`). Enable extensions with `HtmxConfig.UseExtensions(...)` and render `<RzScripts />`; rizzy.js then warns on the console about a rejected extension or one that never registered. See [Extensions]({{<ref "/docs/htmx/extensions.md">}}).

### 9. Console warning: "no <meta name="htmx-config"> on this page"

rizzy.js checks the page when it loads. This warning means htmx has no Rizzy configuration and no antiforgery token. Render `<RzHeadOutlet />` instead of `<HeadOutlet />` in your root layout, before the htmx script. A second warning reports when the server runs a different Rizzy major version than the script (for example a cached CDN copy of rizzy.js). Set `HtmxConfig.RizzyDiagnostics = false` to silence these checks.

## Still Stuck?

If you've worked through these steps and are still facing issues:

*   Simplify your scenario to isolate the problem.
*   Double-check the relevant Rizzy and HTMX documentation.
*   Consider creating a minimal reproducible example.
*   Seek help from the community (e.g., project's GitHub Discussions/Issues, relevant forums). Provide clear details about the problem, what you've tried, relevant code snippets, and browser/server logs if possible.