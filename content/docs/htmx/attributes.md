---
title: "Typed Attributes (Hx)"
description: "Write htmx 4 attributes in Razor with the typed Hx builder: every core and extension attribute, encoded values and htmx 4 syntax."
summary: ""
date: 2026-11-08T12:00:00-05:00
lastmod: 2026-11-08T12:00:00-05:00
draft: false
weight: 120
toc: true
seo:
  title: "Typed Attributes (Hx)"
  description: "Write htmx 4 attributes in Razor with the typed Hx builder: every core and extension attribute, encoded values and htmx 4 syntax."
  canonical: ""
  noindex: false
---

Every htmx attribute can be written by hand in Razor (`hx-post="/save"`), and that keeps working. The
`Hx` builder is a typed alternative: one method per attribute that htmx 4.0.1 and its official
extensions read, with values encoded for you. Pass the result to Blazor's `@attributes`:

```razor
<button @attributes="@(Hx.Post("/save")
                         .Target(HxTarget.Closest("form"))
                         .Swap(SwapStyle.outerHTML.Transition(true))
                         .Trigger(Trigger.OnEvent("click").Once())
                         .Confirm("Save changes?")
                         .Vals(new { draft = true }))">
    Save
</button>
```

renders

```html
<button hx-post="/save" hx-target="closest form" hx-swap="outerHTML transition:true"
        hx-trigger="click once" hx-confirm="Save changes?" hx-vals="{&quot;draft&quot;:true}">Save</button>
```

Wrap the expression in `@( ... )` so Razor accepts the double quotes inside it. When the values depend
on a loop variable, a small helper method keeps the markup readable:

```razor
@foreach (var item in Items)
{
    <tr @attributes="RowAttributes(item)">...</tr>
}

@code {
    private HxAttributes RowAttributes(Item item) =>
        Hx.Delete($"/items/{item.Id}").Confirm($"Delete {item.Name}?").Target(HxTarget.This).Swap(SwapStyle.outerHTML);
}
```

## How values and names are written

- **Builders plug in:** `Trigger(...)` takes the [trigger builder]({{<ref "/docs/htmx/triggers.md">}}), `Swap(...)` the [swap style builder]({{<ref "/docs/htmx/swapstyle.md">}}), and `Status(...)` builds `hx-status:<code>`.
- **JSON values are encoded:** `Vals`, `Headers`, `Config`, `Boost(object)` and `Confirm(HxConfirm)` serialize their argument (camelCase), so quotes and `<` cannot break out of the attribute.
- **Inheritance is explicit in htmx 4:** call `Inherited()` (or `Append()`) right after the attribute it applies to. `Hx.Target("#main").Inherited()` renders `hx-target:inherited="#main"`; calling both renders `name:inherited:append`.
- **Calling a method again replaces** that attribute, including its `:inherited`/`:append` form (call `Inherited()` again if you still want it). `Attr(name, null)` removes one, and `Attr(name, value)` sets anything without a method.
- **Build one per render.** An attribute set is mutable and is read when Blazor renders it. Build it inline or return a new one from a method, as above; don't keep one in a field and keep adding to it.
- **Names use the `hx-` prefix**, which htmx always accepts (`HtmxConfig.Prefix`, `data-hx-` by default in htmx 4, is an alternative). When `HtmxConfig.MetaCharacter` is set (for example `-`), `:` in names becomes that character (`hx-status-422`, `hx-on-click`), because htmx then looks the names up that way. The value is copied from `HtmxConfig` when the app starts.
- **`On(...)` is inline script:** a nonce-based [Content Security Policy]({{<ref "/docs/introduction/contentsecurity.md">}}) blocks `hx-on:*` handlers.

## HxTarget: extended selectors

`HxTarget` builds htmx 4's extended selectors for `Target`, `Include`, `Indicator`, `Disable` and the trigger `From` modifier:

| Helper | Value |
|---|---|
| `HxTarget.This`, `Document`, `Window`, `Body`, `Host` | `this`, `document`, `window`, `body`, `host` |
| `HxTarget.Id("item:1")` | `#item\:1` (CSS-escaped) |
| `HxTarget.Closest("tr")` | `closest tr` |
| `HxTarget.Find(".x")` / `FindAll(".x")` | `find .x` / `findAll .x` |
| `HxTarget.Next()` / `Next(".x")` | `next` / `next .x` |
| `HxTarget.Previous()` / `Previous(".x")` | `previous` / `previous .x` |
| `HxTarget.Global("#x")` | `global #x` |

## Core attributes


<!-- BEGIN GENERATED: core-attributes -->
| Method | Description |
|---|---|
| `Get(string url)` | `hx-get`: issues a GET request to `url`. |
| `Post(string url)` | `hx-post`: issues a POST request to `url`. |
| `Put(string url)` | `hx-put`: issues a PUT request to `url`. |
| `Patch(string url)` | `hx-patch`: issues a PATCH request to `url`. |
| `Delete(string url)` | `hx-delete`: issues a DELETE request to `url`. |
| `Query(string url)` | `hx-query`: issues a QUERY request to `url` (htmx 4). |
| `Action(string url)` | `hx-action`: the request URL, combined with `Method`. |
| `Method(string method)` | `hx-method`: the HTTP method used with `Action`. |
| `Target(string selector)` | `hx-target`: where the response goes (a CSS selector or an `HxTarget` value). |
| `Swap(SwapStyle style)` | `hx-swap`: how the response is swapped. |
| `Swap(SwapStyleBuilder style)` | `hx-swap`: how the response is swapped, with modifiers. |
| `Swap(string swap)` | `hx-swap`: a raw swap specification. |
| `Select(string selector)` | `hx-select`: which part of the response to swap in. |
| `SelectOob(string selectors)` | `hx-select-oob`: parts of the response to swap out of band (`#a, #b:afterbegin`). |
| `SwapOob(string value = "true")` | `hx-swap-oob`: swaps this element out of band, by id (`true`) or with a swap style. |
| `SwapOob(SwapStyle style)` | `hx-swap-oob`: swaps this element out of band with a swap style. |
| `SwapOob(SwapStyleBuilder style)` | `hx-swap-oob`: swaps this element out of band with a swap style and modifiers. |
| `Trigger(TriggerModifierBuilder trigger)` | `hx-trigger`: when the request is sent. |
| `Trigger(TriggerBuilder trigger)` | `hx-trigger`: when the request is sent. |
| `Trigger(string trigger)` | `hx-trigger`: a raw trigger specification. |
| `Vals(object values)` | `hx-vals`: extra values to send, from an object or dictionary (encoded as JSON). |
| `Headers(object headers)` | `hx-headers`: extra request headers, from an object or dictionary (encoded as JSON). |
| `Include(string selector)` | `hx-include`: other elements whose values are sent (a selector or `HxTarget` value). |
| `Encoding(string encoding)` | `hx-encoding`: the request body encoding. |
| `EncodingMultipart()` | `hx-encoding="multipart/form-data"`, needed for file uploads. |
| `Validate(bool validate = true)` | `hx-validate`: run the browser's form validation before sending (forms validate by default). |
| `Config(object config)` | `hx-config`: per-request settings (for example `new { timeout = 5000 }`), encoded as JSON. |
| `Confirm(string text)` | `hx-confirm`: asks before sending, with the browser's `confirm()` or a custom dialog. |
| `Confirm(HxConfirm props)` | `hx-confirm` with props for a custom dialog (the `rizzy-confirm` extension). |
| `Indicator(string selector)` | `hx-indicator`: elements that get the request class while the request runs. |
| `Disable(string selector)` | `hx-disable`: elements disabled while the request runs (htmx 4). |
| `Sync(string sync)` | `hx-sync`: a raw sync specification (`closest form:abort`). |
| `Sync(string selector, HxSyncStrategy strategy)` | `hx-sync`: synchronizes requests with those of another element. |
| `Status(int statusCode, string spec)` | `hx-status:<code>`: how to handle a response status (`Status(422, "target:#errors")`). |
| `Status(string pattern, string spec)` | `hx-status:<pattern>`: how to handle a status pattern such as `4xx` or `5xx`. |
| `Boost(bool boost = true)` | `hx-boost`: turns links and forms inside into htmx requests. |
| `Boost(object settings)` | `hx-boost` with settings applied to boosted requests (for example `new { target = "#main" }`). |
| `PushUrl(bool push = true)` | `hx-push-url`: push the request URL (`true`) into history, or not. |
| `PushUrl(string url)` | `hx-push-url`: push `url` into history. |
| `ReplaceUrl(bool replace = true)` | `hx-replace-url`: replace the current URL with the request URL (`true`), or not. |
| `ReplaceUrl(string url)` | `hx-replace-url`: replace the current URL with `url`. |
| `HistoryElt()` | `hx-history-elt`: on back/forward, restore only this element. |
| `Ignore()` | `hx-ignore`: htmx does not process this element or its descendants. |
| `Preserve()` | `hx-preserve`: keep this element (matched by id) unchanged across swaps. |
| `MorphSkip()` | `hx-morph-skip`: morph swaps leave this element unchanged. |
| `MorphSkipChildren()` | `hx-morph-skip-children`: morph swaps leave this element's children unchanged. |
| `On(string eventName, string script)` | `hx-on:<event>`: runs `script` when `eventName` fires (for example `On(HtmxEvents.AfterSwap, "...")`). This is inline script: a nonce-based Content Security Policy blocks it unless the page allows it. |
| `On(params (string Trigger, string Script)[] handlers)` | `hx-on` with several handlers in one attribute, each with a full trigger specification (`("click once", "...")`). Inline script, like `On`. |
<!-- END GENERATED: core-attributes -->


`HxSyncStrategy` values: `Drop`, `Abort`, `Replace`, `QueueFirst` (htmx's default), `QueueLast`, `QueueAll`.

`HxConfirm` props, read by a custom confirm dialog (`rz:confirm-dialog`): `Title`, `Text`, `ShowConfirmButton`, `ShowDenyButton`, `ShowCancelButton`, `ConfirmButtonText`, `DenyButtonText`, `DismissButtonText`. Without a custom dialog, the browser's `confirm()` shows the title and text.

## Extension attributes

These need the extension enabled with `HtmxConfig.UseExtensions(...)` (see [Extensions]({{<ref "/docs/htmx/extensions.md">}})). Without it, htmx ignores them.


<!-- BEGIN GENERATED: extension-attributes -->
| Method | Description |
|---|---|
| `SseConnect(string url)` | `hx-sse:connect` (Sse): opens a Server-Sent Events connection. |
| `SseClose(string eventName)` | `hx-sse:close` (Sse): closes the connection when this SSE event arrives. |
| `WsConnect(string url)` | `hx-ws:connect` (Ws): opens a WebSocket. |
| `WsSend()` | `hx-ws:send` (Ws): sends this element's values over the WebSocket when triggered. |
| `MultipartConnect(string url)` | `hx-multipart:connect` (Multipart): streams a multipart response. |
| `MultipartClose(string eventName)` | `hx-multipart:close` (Multipart): closes the stream when this part event arrives. |
| `Preload()` | `hx-preload` (Preload): preloads the request, by default on hover/focus. |
| `Preload(TriggerModifierBuilder trigger)` | `hx-preload` (Preload): preloads the request on the given trigger. |
| `Preload(string trigger)` | `hx-preload` (Preload): preloads the request on a raw trigger specification. |
| `Head(HxHeadStrategy strategy)` | `hx-head` (Head): how a response's head is merged, or `re-eval` on a head element. |
| `Prompt(string text)` | `hx-prompt` (Prompt): asks for text before sending; the answer arrives as `HX-Prompt`. |
| `Live(string expression)` | `hx-live` (Live): a reactive expression re-evaluated as the page changes. |
| `Pending(string templateSelector)` | `hx-pending` (Pending): selector of a template shown in the target while the request runs. |
| `PTag(string initialTag)` | `hx-ptag` (PTag): the initial polling tag; later tags come from `HX-PTag`. |
| `Targets(string selector)` | `hx-targets` (Targets): swaps the response into every element matching the selector. |
| `BrowserIndicator(bool show = true)` | `hx-browser-indicator` (BrowserIndicator): show the browser's loading indicator. |
| `History(bool cache)` | `hx-history="false"` (HistoryCache): keep this page out of the history cache (for example pages with sensitive data). |
| `Nonce(string nonce)` | `hx-nonce` (Csp): the page nonce, required on every htmx element by the hx-csp extension. |
<!-- END GENERATED: extension-attributes -->


`HxHeadStrategy` values: `Merge`, `Append`, `ReEval` (`re-eval`).

{{< callout context="note" title="Kept in step with htmx" icon="info-circle" >}}
A test compares this builder with the attributes the installed htmx package reads, so an htmx upgrade that adds an attribute fails CI until `Hx` covers it.
{{< /callout >}}
