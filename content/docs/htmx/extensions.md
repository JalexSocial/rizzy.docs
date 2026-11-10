---
title: "Extensions"
description: "Enable htmx 4 extensions with one line: Rizzy loads their scripts and keeps htmx's extension allow-list in step."
summary: ""
date: 2026-11-08T12:00:00-05:00
lastmod: 2026-11-08T12:00:00-05:00
draft: false
weight: 400
toc: true
seo:
  title: "htmx 4 Extensions with Rizzy"
  description: "Enable htmx 4 extensions with HtmxConfig.UseExtensions and RzScripts; allow-list sync, settings, custom extensions and diagnostics."
  canonical: ""
  noindex: false
---

htmx 4 ships 17 official extensions (Server-Sent Events, WebSockets, preloading, head merging and
more), and Rizzy has four of its own. Using one takes three things that must line up:

1. its script must load **after** htmx;
2. if `htmx.config.extensions` (the allow-list) is set, it must contain the extension's
   **registered name**, which is often not its file name: `hx-sse.js` registers as `sse`,
   `hx-ws.js` as `ws`, `hx-preload.js` as `preload`;
3. the allow-list must keep Rizzy's own extensions.

When any of these is wrong, htmx skips the extension **silently**. Rizzy takes care of all three.

## Enabling extensions

```csharp {title="Program.cs"}
builder.Services.AddHtmx(o =>
{
    o.UseExtensions(HtmxExtension.Sse, HtmxExtension.Preload);
});
```

```razor {title="AppLayout.razor"}
<head>
    ...
    <RzHeadOutlet />
    <RzScripts />
</head>
```

`<RzScripts />` renders, in this order:

1. htmx, from jsDelivr for the version Rizzy is tested with (`HtmxAssets.Version`), with a
   subresource integrity hash;
2. `rizzy.js` (Rizzy's own extensions and diagnostics), from `RizzyConfig.ClientScriptUrl`;
3. each enabled extension, also with its integrity hash.

Every script carries the request's CSP nonce, so a [nonce-based Content Security Policy]({{<ref "/docs/introduction/contentsecurity.md">}}) works unchanged.

Then use the extension's attributes, ideally through the [typed builder]({{<ref "/docs/htmx/attributes.md">}}):

```razor
@* Connects on load (hx-trigger chooses when to connect), swaps unnamed messages into the div and
   closes when the server sends an event named "done". Named events are dispatched as DOM events. *@
<div @attributes="@(Hx.SseConnect("/notifications").SseClose("done"))"></div>

<a href="/reports" @attributes="@(Hx.Get("/reports").Preload())">Reports</a>
```

## The allow-list

By default htmx accepts every extension that registers, and Rizzy writes no allow-list.

- If you set `HtmxConfig.Extensions` yourself, Rizzy **adds** its own four extensions and every
  enabled extension to your list, so none of them is rejected.
- Set `RestrictExtensions = true` to allow **only** the extensions Rizzy knows about: its own, the
  enabled ones and any you list in `Extensions`. A script that sneaks in another extension is
  then rejected by htmx.

```csharp
builder.Services.AddHtmx(o =>
{
    o.UseExtensions(HtmxExtension.Preload);
    o.RestrictExtensions = true;
    // htmx.config.extensions = "rizzy-antiforgery, rizzy-nonce, rizzy-streaming, rizzy-confirm, preload"
});
```

## Extension settings

Several extensions read their own section of `htmx.config`. Set them with `Set(key, value)`; the
value is written into the meta tag as JSON (camelCase). Keys that an `HtmxConfig` property already
writes (`mode`, `extensions`, ...) are rejected with an error that names the property to use instead:

```csharp
builder.Services.AddHtmx(o => o
    .UseExtensions(HtmxExtension.Sse, HtmxExtension.HistoryCache, HtmxExtension.Preload)
    .Set("sse", new { reconnect = true, reconnectDelay = 1000 })
    .Set("historyCache", new { size = 20 })
    .Set("preload", new { boostEvent = "mouseover" }));
```

## Where the scripts come from

`HtmxConfig.Scripts` controls `<RzScripts />`:

| Option | Default | Description |
|---|---|---|
| `BaseUrl` | jsDelivr URL of `htmx.org@<tested version>/dist/` | Where `htmx.min.js` and `ext/<name>.min.js` are loaded from. Point it at your own copy (for example `/lib/htmx/`) to serve htmx yourself. |
| `Minified` | `true` | Load the `.min.js` files. |
| `Integrity` | `null` (automatic) | Add SRI hashes (and `crossorigin="anonymous"`) for the pinned version. Automatic means only for the default jsDelivr URL, because a copy you serve yourself may be another version, which the browser would refuse to run. Set `true` for your own copy of the same version. |
| `IncludeHtmx` | `true` | Load htmx itself. Set to `false` if your layout or bundler already loads it. |

```csharp
builder.Services.AddHtmx(o => o.Scripts = new HtmxScriptOptions { BaseUrl = "/lib/htmx/" });
```

The Rizzy script itself is configured on `RizzyConfig`: `ClientScriptUrl` (default
`_content/Rizzy/js/rizzy.js`).

## Third-party and your own extensions

Describe the extension with `HtmxExtension.Custom(name, scriptUrl)`. It joins the allow-list and,
when you give a script URL, `<RzScripts />` loads it after the official ones:

```csharp
o.UseExtensions(HtmxExtension.Custom("my-ext", "/js/my-ext.js"));
```

## When something is wrong

rizzy.js reports problems on the browser console when the page loads:

- **htmx rejected an extension** because the allow-list does not name it (including Rizzy's own,
  if you set `Extensions` without `UseExtensions`).
- **An extension enabled on the server never registered**, usually because `<RzScripts />` is
  missing from the root layout or its script was not loaded. rizzy.js tracks registrations from the
  moment it loads, so if you write the script tags yourself, load extensions **after** rizzy.js;
  one loaded before it works but is reported here.

Set `HtmxConfig.RizzyDiagnostics = false` to silence these checks.

## Official extensions

| Extension | `HtmxExtension` | Registered name | What it does | Typed API |
|---|---|---|---|---|
| `hx-sse` | `Sse` | `sse` | Server-Sent Events | `Hx.SseConnect`, `SseClose`; `HtmxEvents.Sse.*` |
| `hx-ws` | `Ws` | `ws` | WebSockets | `Hx.WsConnect`, `WsSend`; `HtmxEvents.Ws.*` |
| `hx-preload` | `Preload` | `preload` | Preloads boosted links (on `mousedown` by default) and `hx-preload` elements | `Hx.Preload` |
| `hx-head` | `Head` | `hx-head` | Merges `<head>` elements from responses | `Hx.Head`, `Preserve`; `HtmxEvents.Head.*` |
| `hx-prompt` | `Prompt` | `hx-prompt` | htmx 2's `hx-prompt` | `Hx.Prompt`; `HtmxRequest.Prompt`; `HtmxEvents.Prompt.Answered` |
| `hx-live` | `Live` | `hx-live` | Reactive `hx-live` expressions | `Hx.Live` |
| `hx-pending` | `Pending` | `hx-pending` | Shows a template in the target while a request runs | `Hx.Pending` |
| `hx-ptag` | `PTag` | `ptag` | Polling tags: skip unchanged content | `Hx.PTag`; `HtmxRequest.PTag`; `Response.Htmx().PTag(...)` |
| `hx-targets` | `Targets` | `hx-targets` | One response, several targets | `Hx.Targets` |
| `hx-browser-indicator` | `BrowserIndicator` | `browser-indicator` | Browser's own loading indicator | `Hx.BrowserIndicator`; `Set("boostBrowserIndicator", true)` |
| `hx-csp` | `Csp` | `hx-csp` | Nonce-gated htmx processing; an alternative to Rizzy's `rizzy-nonce` | `Hx.Nonce`; `HtmxEvents.Csp.*` |
| `hx-multipart` | `Multipart` | `hx-multipart` | Streamed multipart responses | `Hx.MultipartConnect`, `MultipartClose`; `HtmxRequest.LastPartId`; `HtmxEvents.Multipart.*` |
| `hx-upsert` | `Upsert` | `upsert` | `upsert` swap style | `Hx.Swap("upsert ...")` |
| `hx-download` | `Download` | `download` | File downloads with progress | `Hx.Swap("download")`; `Response.Htmx().Download(url)`; `HtmxEvents.Download.*` |
| `hx-history-cache` | `HistoryCache` | `history-cache` | htmx 2-style history cache | `Hx.History(false)`; `Set("historyCache", ...)`; `HtmxEvents.HistoryCache.*` |
| `htmx-2-compat` | `Htmx2Compat` | `compat` | htmx 2 event names and behavior | |
| `hx-alpine-compat` | `AlpineCompat` | `alpine-compat` | Alpine.js on swapped and morphed content | |

Rizzy's own extensions, always loaded with `rizzy.js`: `rizzy-antiforgery`, `rizzy-nonce`,
`rizzy-streaming` and `rizzy-confirm` (`HtmxExtension.Rizzy`).

{{< callout context="note" title="Extensions that change the request's fetch" icon="info-circle" >}}
Preload serves a click from a response it fetched on `mousedown`, and other extensions may wrap the
request's fetch function. Rizzy's streaming extension keeps whatever they install and streams the
final response, so `[StreamRendering]` pages still stream alongside them.
{{< /callout >}}
