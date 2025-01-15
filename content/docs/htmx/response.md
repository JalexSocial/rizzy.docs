Below is the documentation with all the C# examples reformatted for proper indentation:

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

The `HtmxResponse` class enables developers to manage client-side behavior through response headers in applications that leverage HTMX. This includes navigating, refreshing, and updating parts of the web page without a full reload, as well as triggering client-side events.

| Member Signature | Return Type | Description |
|------------------|-------------|-------------|
| `StatusCode(HttpStatusCode statusCode)` | `HtmxResponse` | Sets the response status code to the specified `statusCode`. |
| `EmptyBody()` | `HtmxResponse` | Instructs the response to not render any component markup (headers and cookies are still returned). |
| `Location(string path)` | `HtmxResponse` | Performs a client-side redirect without a full page reload by setting the location header using a string path. |
| `Location(LocationTarget locationTarget)` | `HtmxResponse` | Performs a client-side redirect without a full page reload by setting the location header using a serialized `LocationTarget` object. |
| `PushUrl(string url)` | `HtmxResponse` | Pushes a new URL onto the history stack using a string value. |
| `PushUrl(Uri url)` | `HtmxResponse` | Pushes a new URL onto the history stack by converting a `Uri` to its string representation. |
| `PreventBrowserHistoryUpdate()` | `HtmxResponse` | Prevents the browser’s history from being updated (overwrites any existing PushUrl header). |
| `PreventBrowserCurrentUrlUpdate()` | `HtmxResponse` | Prevents the browser’s current URL from being updated (overwrites any existing ReplaceUrl header). |
| `Redirect(string url)` | `HtmxResponse` | Triggers a client-side redirect to the specified URL (as a string) and requests an empty response body. |
| `Redirect(Uri url)` | `HtmxResponse` | Triggers a client-side redirect to the specified URL (as a `Uri`), converting it to a string. |
| `Refresh()` | `HtmxResponse` | Enables a client-side full refresh of the page (sets a refresh header and requests an empty response body). |
| `ReplaceUrl(string url)` | `HtmxResponse` | Replaces the current URL in the browser’s location bar using a string URL. |
| `ReplaceUrl(Uri url)` | `HtmxResponse` | Replaces the current URL in the browser’s location bar by converting a `Uri` to its string representation. |
| `Reswap(string modifier)` | `HtmxResponse` | Specifies how the response will be swapped by setting the `hx-swap` modifier using a string. |
| `Reswap(SwapStyle swapStyle, string? modifier = null)` | `HtmxResponse` | Specifies how the response will be swapped using a `SwapStyle` and an optional modifier string. If `SwapStyle.Default` is provided, the modifier string is used directly. |
| `Reswap(SwapStyleBuilder swapStyle)` | `HtmxResponse` | Specifies how the response will be swapped by building a swap style from a `SwapStyleBuilder` instance. |
| `Retarget(string selector)` | `HtmxResponse` | Updates the target element for the content update by specifying a CSS selector. |
| `Reselect(string selector)` | `HtmxResponse` | Chooses which part of the response is used to be swapped in by specifying a CSS selector. |
| `StopPolling()` | `HtmxResponse` | Sets the response status code to stop polling (using the special `HtmxStatusCodes.StopPolling` status). |
| `Trigger(string eventName, TriggerTiming timing = TriggerTiming.Default)` | `HtmxResponse` | Triggers a client-side event with the given `eventName` and optional timing. |
| `Trigger<TEventDetail>(string eventName, TEventDetail detail, TriggerTiming timing = TriggerTiming.Default, JsonSerializerOptions? jsonSerializerOptions = null)` | `HtmxResponse` | Triggers a client-side event with a given `eventName`, including serialized event detail data, optional timing, and optional JSON serializer options. |

{{< callout context="note" title="Note" icon="info-circle" >}}
The HtmxResponse class was constructed based on HTMX usage of Response headers. You can find more information about HTMX response headers on the official [Htmx documentation site](https://htmx.org/reference/#response_headers).
{{< /callout >}}

## Working With HtmxResponse

`HtmxResponse` only has a dependency on HttpContext, so you can use it in any scoped dependency service that has access to HttpContext. To manually create an HtmxResponse object you need only to create a new instance of the class as follows:

```csharp
var response = new HtmxResponse(httpContext);
```

For the purposes of the examples in this guide, we will be using an instance of HtmxResponse that is available as an HttpResponse extension.

## Location

Performs a client-side redirect to the specified path without a full page reload, leveraging HTMX's ability to handle AJAX navigation seamlessly.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Location("/new-path");
});
```

This method is particularly useful for implementing SPA-like behavior in traditional server-rendered applications, allowing for partial updates and navigation without losing the state of the application.

## PushUrl

Pushes a new URL onto the browser's history stack. This method leverages HTMX's support for AJAX-driven navigation while maintaining correct browser history and bookmarkable URLs.

*Example*

```csharp
Response.Htmx(h =>
{
    h.PushUrl("/another-path");
});
```

Use this method to dynamically update the URL in response to partial content updates, ensuring that users can use the browser's back and forward buttons as expected.

## PreventBrowserHistoryUpdate

Ensures that the browser's history is not updated following an AJAX request, overriding any previous PushUrl action. This is useful in scenarios where updates should not affect the browser's history, such as filtering or sorting operations on a page.

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

Facilitates a client-side redirection, akin to a traditional HTTP redirect but executed via HTMX, allowing for a smoother user experience without a full page refresh.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Redirect("/redirect-path");
});
```

This method is useful for redirecting the user after actions that do not require a full page reload, such as form submissions or after performing AJAX-based operations.

## Refresh

Triggers a full page refresh from the server-side. This can be particularly beneficial after a sequence of operations where a fresh state from the server is required.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Refresh();
});
```

In HTMX, a full page refresh might be necessary in scenarios where client-side state needs to be completely reset, or when significant changes have been made that require a fresh page load.

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
Reswap uses SwapStyle and SwapStyle modifiers. For complete information on SwapStyle see [SwapStyle Documentation](/docs/htmx/swapstyle).
{{< /callout >}}

Specifies how the response will be swapped into the target element. This allows for fine-grained control over how parts of the page are updated with server responses.

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
// Reswap output: "innerHTML show:window:top transition:true"
```

*Example with Fluent Modifiers*

```csharp
Response.Htmx(h =>
{
    h.Reswap(SwapStyle.beforebegin.ShowWindow(ScrollDirection.top));
});
// Reswap output: "beforebegin show:window:top"
```

### SwapStyle Options

Here are the `SwapStyle` options that define how the response is swapped into the target element on the page:

- `Default`: Uses the application's default swap style or htmx's default.
- `innerHTML`: Replace the inner HTML of the target element.
- `outerHTML`: Replace the entire target element with the response.
- `beforebegin`: Insert the response before the target element.
- `afterbegin`: Insert the response inside the target element, before its first child.
- `beforeend`: Insert the response inside the target element, after its last child.
- `afterend`: Insert the response after the target element.
- `delete`: Deletes the target element, regardless of the response.
- `none`: Does not append content from the response (though out-of-band items will still be processed).

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

Initiates custom events on the client side, which can be used to trigger JavaScript actions in response to server-side events. This method makes use of HTMX's ability to interact with custom JavaScript by triggering events based on server responses.

*Example*

```csharp
Response.Htmx(h =>
{
    h.Trigger("customEvent", new { key = "value" }, TriggerTiming.AfterSwap);
});
```

This functionality is particularly useful for integrating server-side logic with client-side behaviors, allowing developers to create rich, interactive web applications that respond dynamically to server-side changes.

### TriggerTiming Options

Understanding the timing for triggering client-side events is also crucial:

- `Default`: Trigger events as soon as the response is received.
- `AfterSettle`: Trigger events after the settling step, which includes processing scripts and styles.
- `AfterSwap`: Trigger events after the swap step, ensuring the DOM has been updated.

These options can be used with the `Trigger` method to control when events are fired in response to HTMX actions.