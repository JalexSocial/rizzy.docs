---

title: "Response"  
description: ""  
summary: ""  
date: 2024-02-05T12:10:35-05:00  
lastmod: 2024-02-05T12:10:35-05:00  
draft: false  
menu:  
  docs:  
    parent: ""  
    identifier: "response-62ebe8c1dcbe3a08e7cf1a03c3fff9ab"  
    weight: 300  
toc: true  
seo:  
  title: "" # custom title (optional)  
  description: "" # custom description (recommended)  
  canonical: "" # custom canonical URL (optional)  
  noindex: false # false (default) or true  
---

The `HtmxResponse` class enables developers to manage client‑side behavior through response headers in applications that leverage HTMX. This includes navigating, refreshing, and updating parts of the web page without a full reload, as well as triggering client‑side events.

| Member Signature | Return Type | Description |
|------------------|-------------|-------------|
| `StatusCode(HttpStatusCode statusCode)` | `HtmxResponse` | Sets the response status code to the specified `statusCode`. |
| `EmptyBody()` | `HtmxResponse` | Instructs the response to not render any component markup (headers and cookies are still returned). |
| `Location(string path)` | `HtmxResponse` | Performs a client‑side redirect without a full page reload by setting the location header using a string path. |
| `Location(LocationTarget locationTarget)` | `HtmxResponse` | Performs a client‑side redirect without a full page reload by setting the location header using a serialized `LocationTarget` object. |
| `PushUrl(string url)` | `HtmxResponse` | Pushes a new URL onto the history stack using a string value. |
| `PushUrl(Uri url)` | `HtmxResponse` | Pushes a new URL onto the history stack by converting a `Uri` to its string representation. |
| `PreventBrowserHistoryUpdate()` | `HtmxResponse` | Prevents the browser’s history from being updated (overwrites any existing PushUrl header). |
| `PreventBrowserCurrentUrlUpdate()` | `HtmxResponse` | Prevents the browser’s current URL from being updated (overwrites any existing ReplaceUrl header). |
| `LocalLocation(string localUrl)` | `HtmxResponse` | Like `Location`, but only for local URLs (`/path` or `~/path`, resolved against the app's path base); throws for external URLs, so user input cannot cause an open redirect. |
| `LocalRedirect(string localUrl)` | `HtmxResponse` | Like `Redirect`, but only for local URLs; throws for external URLs. |
| `IsLocalUrl(string? url)` (static) | `bool` | Whether a URL is local (`/path` or `~/path`, but not `//host` or `/\host`). |
| `Redirect(string url)` | `HtmxResponse` | Triggers a client‑side redirect to the specified URL (as a string) and requests an empty response body. |
| `Redirect(Uri url)` | `HtmxResponse` | Triggers a client‑side redirect to the specified URL (as a `Uri`), converting it to a string. |
| `Refresh()` | `HtmxResponse` | Enables a client‑side full refresh of the page (sets a refresh header and requests an empty response body). |
| `ReplaceUrl(string url)` | `HtmxResponse` | Replaces the current URL in the browser’s location bar using a string URL. |
| `ReplaceUrl(Uri url)` | `HtmxResponse` | Replaces the current URL in the browser’s location bar by converting a `Uri` to its string representation. |
| `Reswap(string modifier)` | `HtmxResponse` | Specifies how the response will be swapped by setting the `hx‑swap` modifier using a string. |
| `Reswap(SwapStyle swapStyle, string? modifier = null)` | `HtmxResponse` | Specifies how the response will be swapped using a `SwapStyle` and an optional modifier string. If `SwapStyle.Default` is provided, the modifier string is used directly. |
| `Reswap(SwapStyleBuilder swapStyle)` | `HtmxResponse` | Specifies how the response will be swapped by building a swap style from a `SwapStyleBuilder` instance. |
| `Retarget(string selector)` | `HtmxResponse` | Updates the target element for the content update by specifying a CSS selector. |
| `PTag(string tag)` | `HtmxResponse` | Sends a new polling tag (`HX-PTag`) for the hx-ptag [extension]({{<ref "/docs/htmx/extensions.md">}}). |
| `Download(string url)` | `HtmxResponse` | Tells the hx-download extension to fetch `url` as a file download (`HX-Download`). |
| `ValidationFailed(string? retargetSelector = null, SwapStyle reswap = SwapStyle.Default)` | `HtmxResponse` | Marks the response as a validation failure (status 422, which htmx 4 swaps), optionally retargeting it or changing the swap style. See [Validation]({{<ref "/docs/forms/validation.md">}}). |
| `Reselect(string selector)` | `HtmxResponse` | Chooses which part of the response is used to be swapped in by specifying a CSS selector. |
| `Trigger(string eventName)` | `HtmxResponse` | Triggers a client‑side event (`HX-Trigger`) on the element that issued the request. |
| `Trigger<TEventDetail>(string eventName, TEventDetail detail, JsonSerializerOptions? jsonSerializerOptions = null)` | `HtmxResponse` | Triggers a client‑side event with a JSON `detail` (serialized with the app's `JsonOptions` unless you pass options). |
| `TriggerOn(string eventName, string targetSelector)` | `HtmxResponse` | Triggers the event on the element matching `targetSelector` instead of the requesting element. |
| `TriggerOn<TEventDetail>(string eventName, string targetSelector, TEventDetail detail, JsonSerializerOptions? jsonSerializerOptions = null)` | `HtmxResponse` | `TriggerOn` with a JSON `detail`. |

{{< callout context="note" title="Note" icon="info-circle" >}}
The HtmxResponse class was constructed based on HTMX usage of response headers. You can find more information about HTMX response headers on the official [htmx 4 documentation site](https://four.htmx.org/).
{{< /callout >}}

{{< callout context="caution" title="htmx requests only" icon="alert-triangle" >}}
Every method that sets an `HX-*` header, and `EmptyBody()`, throws an `InvalidOperationException` when the current request is not an htmx request, because a browser would ignore the header. Check `Request.IsHtmx()` first in actions that serve both kinds of request. Only `StatusCode` and `IsLocalUrl` work for any request.
{{< /callout >}}

## Working With HtmxResponse

`HtmxResponse` only has a dependency on `HttpContext`, so you can use it in any scoped dependency service that has access to `HttpContext`. To manually create an `HtmxResponse` object you need only to create a new instance of the class as follows:

```csharp
var response = new HtmxResponse(httpContext);
```

Or as an `HttpContext.Response` extension:

```csharp
var response = HttpContext.Response.Htmx();
```

If you are familiar with Htmx.net, then you can use a similar syntax under the Rizzy library.  Please note that Rizzy uses its own HTMX server‑side implementation so you will need to use the documentation.

```csharp
HttpContext.Response.Htmx(h => {
  h.PushUrl("/new-url")
   .Trigger("show-special-notification");
});
```

For the purposes of the examples in this guide, we will be using an instance of `HtmxResponse` that is available as an `HttpResponse` extension.

## Location

Performs a client‑side redirect to the specified path without a full page reload, leveraging HTMX's ability to handle AJAX navigation seamlessly.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Location("/new-path");
});
```

This method is particularly useful for implementing SPA‑like behavior in traditional server‑rendered applications, allowing for partial updates and navigation without losing the state of the application.

## PushUrl

Pushes a new URL onto the browser's history stack. This method leverages HTMX's support for AJAX‑driven navigation while maintaining correct browser history and bookmarkable URLs.

*Example*

```csharp
Response.Htmx(h =>
{
    h.PushUrl("/another-path");
});
```

Use this method to dynamically update the URL in response to partial content updates, ensuring that users can use the browser's back and forward buttons as expected.

## PreventBrowserHistoryUpdate

Ensures that the browser's history is not updated following an AJAX request, overriding any previous `PushUrl` action. This is useful in scenarios where updates should not affect the browser's history, such as filtering or sorting operations on a page.

*Example*

```csharp
Response.Htmx(h =>
{
    h.PreventBrowserHistoryUpdate();
});
```

## PreventBrowserCurrentUrlUpdate

Stops the browser’s current URL from being updated.

*Example*

```csharp
Response.Htmx(h =>
{
    h.PreventBrowserCurrentUrlUpdate();
});
```

## Redirect

Facilitates a client‑side redirection, akin to a traditional HTTP redirect but executed via HTMX, allowing for a smoother user experience without a full page refresh.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Redirect("/redirect-path");
});
```

This method is useful for redirecting the user after actions that do not require a full page reload, such as form submissions or after performing AJAX‑based operations.

When the URL comes from user input (for example a `returnUrl` query parameter), use `LocalRedirect` (or `LocalLocation`) instead. It accepts only local URLs, resolves `~/` against the app's path base, and throws for anything else:

```csharp
Response.Htmx(h =>
{
    h.LocalRedirect(returnUrl ?? "~/");
});
```

## Refresh

Triggers a full page refresh from the server‑side. This can be particularly beneficial after a sequence of operations where a fresh state from the server is required.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Refresh();
});
```

In HTMX, a full page refresh might be necessary in scenarios where client‑side state needs to be completely reset, or when significant changes have been made that require a fresh page load.

## ReplaceUrl

Updates the current URL in the browser's location bar.

*Example*

```csharp
Response.Htmx(h =>
{
    h.ReplaceUrl("/new-url");
});
```

## Reswap

{{< callout context="note" title="Note" icon="info-circle" >}}
Reswap uses `SwapStyle` and swap modifiers. For complete information on `SwapStyle` see [SwapStyle Documentation](/docs/htmx/swapstyle).
{{< /callout >}}

Specifies how the response will be swapped into the target element. This allows for fine‑grained control over how parts of the page are updated with server responses.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Reswap(SwapStyle.innerHTML);
});
```

*Example with Modifiers*

```csharp
Response.Htmx(h =>
{
    h.Reswap(SwapStyle.innerHTML.ShowWindow(ScrollDirection.top).Transition(true));
});
// Reswap output: "innerHTML transition:true show:top showTarget:window"
```

*Example with Fluent Modifiers*

```csharp
Response.Htmx(h =>
{
    h.Reswap(SwapStyle.beforebegin.ShowWindow(ScrollDirection.top));
});
// Reswap output: "beforebegin show:top showTarget:window"
```

### SwapStyle Options

Here are the `SwapStyle` options that define how the response is swapped into the target element on the page:

- `Default`: Uses the application's default swap style or HTMX's default.
- `innerHTML`: Replace the inner HTML of the target element.
- `outerHTML`: Replace the entire target element with the response.
- `beforebegin`: Insert the response before the target element.
- `afterbegin`: Insert the response inside the target element, before its first child.
- `beforeend`: Insert the response inside the target element, after its last child.
- `afterend`: Insert the response after the target element.
- `delete`: Deletes the target element, regardless of the response.
- `none`: Does not append content from the response (though out‑of‑band items will still be processed).
- `innerMorph`: Morphs the contents of the target element by diffing the existing and new HTML.
- `outerMorph`: Morphs the target element itself by diffing the existing and new HTML.
- `textContent`: Replace only the text content inside the target element.
- `before`: Insert the response content immediately before the target node without replacing it.
- `after`: Insert the response content immediately after the target node without replacing it.
- `prepend`: Prepend the response content as the first child of the target element.
- `append`: Append the response content as the last child of the target element.

## Retarget

Changes the target element for the response update using a CSS selector.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Retarget("#new-target");
});
```

## Reselect

Determines which part of the response is swapped in, using a CSS selector.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Reselect(".content-part");
});
```

## Trigger

Triggers custom events on the client (`HX-Trigger`), which you can handle with `hx-trigger`, `hx-on:*` or `addEventListener`. In htmx 4 these events fire once, after the response has been swapped.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Trigger("itemSaved", new { id = 42 });
});
```

```html
<div hx-get="/items" hx-trigger="itemSaved from:body">...</div>
```

- Calling `Trigger` more than once adds the events in call order. Calling it again for the **same** event name replaces that event's earlier detail. Event names are case‑sensitive, like DOM event names.
- The detail is serialized with your app's `JsonOptions` (camelCase by default), and the header is always valid, ASCII‑only JSON.
- htmx 4 has no `HX-Trigger-After-Swap`/`HX-Trigger-After-Settle` headers, so Rizzy 6 removed `TriggerTiming`.

### TriggerOn

Dispatches the event on another element instead of the one that issued the request:

```csharp
Response.Htmx(h =>
{
    h.TriggerOn("refresh", "#cart-summary");
});
```

## ValidationFailed

Answers a form post that failed validation: status 422 plus the re-rendered form. htmx 4 swaps 4xx responses, so the form (with its errors) replaces the old one.

```csharp
if (!ModelState.IsValid)
{
    Response.Htmx().ValidationFailed();             // or ValidationFailed("#errors") to retarget
    return View<SignupForm>();
}
```

See [Validation]({{<ref "/docs/forms/validation.md">}}) for the full flow.
