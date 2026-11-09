---
title: "Events"
description: "Constants for every htmx 4 event, official extension event and Rizzy event, for triggers, hx-on handlers and JavaScript listeners."
summary: ""
date: 2026-11-08T12:00:00-05:00
lastmod: 2026-11-08T12:00:00-05:00
draft: false
weight: 320
toc: true
seo:
  title: "Events"
  description: "Constants for every htmx 4 event, official extension event and Rizzy event, for triggers, hx-on handlers and JavaScript listeners."
  canonical: ""
  noindex: false
---

`HtmxEvents` has a constant for every event htmx 4.0.1, its official extensions and Rizzy dispatch.
Use them wherever an event name goes:

```razor
@* Refresh when an item is saved anywhere on the page *@
<div @attributes="@(Hx.Get("/items").Trigger(Trigger.OnEvent("itemSaved").From(HxTarget.Body)))"></div>

@* Run code after the request (inline script: see the CSP note on the Typed Attributes page) *@
<form @attributes="@(Hx.Post("/save").On(HtmxEvents.AfterRequest, "this.reset()"))">...</form>
```

```csharp
// Server side: trigger an event on the requesting element
Response.Htmx().Trigger("itemSaved", new { id = 42 });

// Listen for an extension event in a trigger
var trigger = Trigger.OnEvent(HtmxEvents.Sse.AfterMessage);
```

When `HtmxConfig.MetaCharacter` is set, htmx dispatches event names with `:` replaced by that character. `HtmxEvents.WithMetaCharacter(name, "-")` converts a name; the `Hx` builder does this for `On(...)` attribute names automatically.

## htmx core

| Constant | Event |
|---|---|
| `HtmxEvents.Abort` | `htmx:abort` |
| `HtmxEvents.AfterCleanup` | `htmx:after:cleanup` |
| `HtmxEvents.AfterHistoryPush` | `htmx:after:history:push` |
| `HtmxEvents.AfterHistoryReplace` | `htmx:after:history:replace` |
| `HtmxEvents.AfterHistoryUpdate` | `htmx:after:history:update` |
| `HtmxEvents.AfterImplicitInheritance` | `htmx:after:implicitInheritance` |
| `HtmxEvents.AfterInit` | `htmx:after:init` |
| `HtmxEvents.AfterProcess` | `htmx:after:process` |
| `HtmxEvents.AfterRequest` | `htmx:after:request` |
| `HtmxEvents.AfterSettle` | `htmx:after:settle` |
| `HtmxEvents.AfterSwap` | `htmx:after:swap` |
| `HtmxEvents.AfterViewTransition` | `htmx:after:viewTransition` |
| `HtmxEvents.BeforeCleanup` | `htmx:before:cleanup` |
| `HtmxEvents.BeforeHistoryRestore` | `htmx:before:history:restore` |
| `HtmxEvents.BeforeHistoryUpdate` | `htmx:before:history:update` |
| `HtmxEvents.BeforeInit` | `htmx:before:init` |
| `HtmxEvents.BeforeMorphAttr` | `htmx:before:morph:attr` |
| `HtmxEvents.BeforeMorphNode` | `htmx:before:morph:node` |
| `HtmxEvents.BeforeOnInit` | `htmx:before:on:init` |
| `HtmxEvents.BeforeProcess` | `htmx:before:process` |
| `HtmxEvents.BeforeRequest` | `htmx:before:request` |
| `HtmxEvents.BeforeResponse` | `htmx:before:response` |
| `HtmxEvents.BeforeSettle` | `htmx:before:settle` |
| `HtmxEvents.BeforeSwap` | `htmx:before:swap` |
| `HtmxEvents.BeforeViewTransition` | `htmx:before:viewTransition` |
| `HtmxEvents.ConfigRequest` | `htmx:config:request` |
| `HtmxEvents.Confirm` | `htmx:confirm` |
| `HtmxEvents.Error` | `htmx:error` |
| `HtmxEvents.FinallyRequest` | `htmx:finally:request` |
| `HtmxEvents.FinallySwap` | `htmx:finally:swap` |
| `HtmxEvents.ResponseError` | `htmx:response:error` |
| `HtmxEvents.Scope` | `htmx:scope` |

`htmx:process:<type>` is dispatched for each `<hx-*>` template element in a response: `HtmxEvents.Process("partial")` gives `htmx:process:partial`.

## Extensions

These are dispatched only when the extension is enabled (see [Extensions]({{<ref "/docs/htmx/extensions.md">}})).

### hx-csp

| Constant | Event |
|---|---|
| `HtmxEvents.Csp.Strip` | `htmx:security:strip` |
| `HtmxEvents.Csp.Violation` | `htmx:security:violation` |

### hx-download

| Constant | Event |
|---|---|
| `HtmxEvents.Download.Complete` | `htmx:download:complete` |
| `HtmxEvents.Download.Progress` | `htmx:download:progress` |
| `HtmxEvents.Download.Start` | `htmx:download:start` |

### hx-head

| Constant | Event |
|---|---|
| `HtmxEvents.Head.AfterMerge` | `htmx:head:after:merge` |
| `HtmxEvents.Head.BeforeAdd` | `htmx:head:before:add` |
| `HtmxEvents.Head.BeforeMerge` | `htmx:head:before:merge` |
| `HtmxEvents.Head.BeforeRemove` | `htmx:head:before:remove` |

### hx-history-cache

| Constant | Event |
|---|---|
| `HtmxEvents.HistoryCache.AfterRestore` | `htmx:history:cache:after:restore` |
| `HtmxEvents.HistoryCache.AfterSave` | `htmx:history:cache:after:save` |
| `HtmxEvents.HistoryCache.BeforeRestore` | `htmx:history:cache:before:restore` |
| `HtmxEvents.HistoryCache.BeforeSave` | `htmx:history:cache:before:save` |
| `HtmxEvents.HistoryCache.Hit` | `htmx:history:cache:hit` |
| `HtmxEvents.HistoryCache.Miss` | `htmx:history:cache:miss` |

### hx-multipart

| Constant | Event |
|---|---|
| `HtmxEvents.Multipart.AfterConnection` | `htmx:multipart:after:connection` |
| `HtmxEvents.Multipart.AfterPart` | `htmx:multipart:after:part` |
| `HtmxEvents.Multipart.BeforeConnection` | `htmx:multipart:before:connection` |
| `HtmxEvents.Multipart.BeforePart` | `htmx:multipart:before:part` |
| `HtmxEvents.Multipart.Close` | `htmx:multipart:close` |
| `HtmxEvents.Multipart.Error` | `htmx:multipart:error` |

### hx-prompt

| Constant | Event |
|---|---|
| `HtmxEvents.Prompt.Answered` | `htmx:prompt` |

### hx-sse

| Constant | Event |
|---|---|
| `HtmxEvents.Sse.AfterConnection` | `htmx:sse:after:connection` |
| `HtmxEvents.Sse.AfterMessage` | `htmx:sse:after:message` |
| `HtmxEvents.Sse.BeforeConnection` | `htmx:sse:before:connection` |
| `HtmxEvents.Sse.BeforeMessage` | `htmx:sse:before:message` |
| `HtmxEvents.Sse.Close` | `htmx:sse:close` |
| `HtmxEvents.Sse.Error` | `htmx:sse:error` |

### hx-ws

| Constant | Event |
|---|---|
| `HtmxEvents.Ws.AfterConnection` | `htmx:ws:after:connection` |
| `HtmxEvents.Ws.AfterMessageIncoming` | `htmx:ws:after:message:incoming` |
| `HtmxEvents.Ws.AfterMessageOutgoing` | `htmx:ws:after:message:outgoing` |
| `HtmxEvents.Ws.BeforeConnection` | `htmx:ws:before:connection` |
| `HtmxEvents.Ws.BeforeMessageIncoming` | `htmx:ws:before:message:incoming` |
| `HtmxEvents.Ws.BeforeMessageOutgoing` | `htmx:ws:before:message:outgoing` |
| `HtmxEvents.Ws.Close` | `htmx:ws:close` |
| `HtmxEvents.Ws.Error` | `htmx:ws:error` |

## Rizzy

| Constant | Event |
|---|---|
| `HtmxEvents.Rizzy.StreamOpen` | `htmx:rizzy:stream:open` |
| `HtmxEvents.Rizzy.StreamBlock` | `htmx:rizzy:stream:block` |
| `HtmxEvents.Rizzy.StreamClose` | `htmx:rizzy:stream:close` |
| `HtmxEvents.Rizzy.ConfigWarn` | `htmx:rizzy:config:warn` |
| `HtmxEvents.Rizzy.ConfirmDialog` | `rz:confirm-dialog` |
| `HtmxEvents.Rizzy.ServerError` | `rz:server-error` |
