---
title: "Request"
description: ""
summary: ""
date: 2024-02-05T12:10:20-05:00
lastmod: 2024-02-05T12:10:20-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "request-73afe35878d725325150eb4a35856a4d"
weight: 200
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
The `HtmxRequest` class reads the htmx 4 request headers: whether a request was made by htmx, whether it is boosted or a history restore, what kind of response it expects, and which elements are involved.

| Property         | Type              | Description |
|------------------|-------------------|-------------|
| `Method`         | `string`          | The HTTP method of the current request. |
| `Path`           | `PathString`      | The request path. |
| `IsHtmx`         | `bool`            | Whether the request was made by htmx (`HX-Request`). |
| `IsBoosted`      | `bool`            | Whether the request came from an element using `hx-boost`. |
| `IsHistoryRestore` | `bool`          | Whether htmx is restoring a page on back/forward (`HX-History-Restore-Request`). |
| `CurrentURL`     | `Uri?`            | The browser's current URL (`HX-Current-URL`). |
| `RequestType`    | `string?`         | The raw `HX-Request-Type` header: `partial` or `full`. |
| `Type`           | `HtmxRequestType` | The parsed request type: `None`, `Partial`, `Full` or `Unknown`. |
| `IsPartial`      | `bool`            | Whether the response should be a fragment: an htmx request that targets part of the page and is not a history restore. |
| `IsFullPage`     | `bool`            | The inverse of `IsPartial`: a full page is expected. |
| `Target`         | `string?`         | The raw `HX-Target` header, in htmx 4's `tag#id` form (for example `div#results`). |
| `TargetId`       | `string?`         | The id part of `Target` (URI-decoded), or `null` when the target has no id (`HX-Target: div`). |
| `Source`         | `string?`         | The raw `HX-Source` header for the element that triggered the request, in `tag#id` form. |
| `SourceId`       | `string?`         | The id part of `Source`, or `null` when the element has no id. |
| `Prompt`         | `string?`         | The answer to `hx-prompt` (`HX-Prompt`, URI-decoded). Needs the hx-prompt [extension]({{<ref "/docs/htmx/extensions.md">}}). |
| `PTag`           | `string?`         | The element's polling tag (`HX-PTag`). Needs the hx-ptag extension; answer 304 when nothing changed. |
| `LastPartId`     | `string?`         | The last part id before a reconnect (`HX-Last-Part-ID`). Needs the hx-multipart extension. |

`HtmxLayout` uses `IsPartial` to decide whether to render your layout; see [Layouts]({{<ref "/docs/components/layout.md">}}).

{{< callout context="note" title="Rizzy 6" icon="info-circle" >}}
htmx 4 no longer sends `HX-Trigger`, `HX-Trigger-Name` or `HX-Prompt`, so Rizzy 6 removed `Trigger`, `TriggerName` and `Prompt`. Use `Source`/`SourceId` for the element that issued the request.
{{< /callout >}}

{{< callout context="note" title="Note" icon="info-circle" >}}
The HtmxRequest class was constructed based on HTMX usage of Request headers.  You can find more information about HTMX request headers on the official [htmx 4 documentation site](https://four.htmx.org/).
{{< /callout >}}

## Working With HtmxRequest

`HtmxRequest` only has a dependency on HttpContext, so you can use it in any scoped dependency service that has access to HttpContext.  To manually create an HtmxRequest object you need only to create a new instance of the class as follows:

```csharp
var request = new HtmxRequest(httpContext);
```

The `HtmxRequest` object is accessible from the `Request` property of a controller (or any `HttpRequest`):

```csharp
var request = Request.Htmx();
```

## IsHtmx

Determines if the current request was triggered by HTMX.

**Example**

```csharp
bool isHtmxRequest = Request.IsHtmx();
```

## IsBoosted

Checks whether the current request was initiated via an element using `hx-boost`.

**Example**

```csharp
bool isBoosted = Request.Htmx().IsBoosted;
```

## IsHistoryRestore

Identifies if the request is an HTMX history restore request.

**Example**

```csharp
bool isHistoryRestore = Request.Htmx().IsHistoryRestore;
```

## CurrentURL

Gets the current URL from the browser as triggered by the HTMX request.

**Example**

```csharp
Uri? currentUrl = Request.Htmx().CurrentURL;
```

## IsPartial and Type

Tells you what kind of response htmx expects. Most code doesn't need this, because `View<T>` already renders a fragment or a full page accordingly.

**Example**

```csharp
var htmx = Request.Htmx();
if (htmx.IsPartial)
{
    // htmx targets one element: return just the fragment
}
else if (htmx.Type == HtmxRequestType.Full)
{
    // boosted body swap, hx-select or history restore: return the full page
}
```

## Target and TargetId

`Target` is the raw `HX-Target` header (`tag#id` in htmx 4); `TargetId` is the id, or `null` if the target element has no id.

**Example**

```csharp
string? targetId = Request.Htmx().TargetId;   // "results" for HX-Target: div#results
```

## Source and SourceId

The element that triggered the request.

**Example**

```csharp
string? sourceId = Request.Htmx().SourceId;   // "save" for HX-Source: button#save
```
