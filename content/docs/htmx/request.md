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
The `HtmxRequest` class provides properties to determine characteristics of a request triggered by HTMX within an ASP.NET application. This class helps in identifying whether a request is made via HTMX, if it is boosted, part of a history restore, or contains specific HTMX-related headers such as the current URL, target, trigger name, trigger id, and prompt responses.

| Property         | Type              | Description                                                                                         |
|------------------|-------------------|-----------------------------------------------------------------------------------------------------|
| `Method`         | `string`          | Gets the HTTP method of the current request.                                                      |
| `Path`           | `PathString`      | Gets the request path.                                                                              |
| `IsHtmx`         | `bool`            | Gets whether or not the current request is an Htmx triggered request.                               |
| `IsBoosted`      | `bool`            | Gets whether or not the current request is initiated via an element using `hx-boost`.                 |
| `IsHistoryRestore` | `bool`          | Gets whether or not the current request is an Htmx history restore request.                         |
| `CurrentURL`     | `Uri?`            | Gets the current URL of the browser.                                                                |
| `Target`         | `string?`         | Gets the `id` of the target element if it exists.                                                 |
| `TriggerName`    | `string?`         | Gets the `name` of the triggered element if it exists.                                             |
| `Trigger`        | `string?`         | Gets the `id` of the triggered element if it exists.                                               |
| `Prompt`         | `string?`         | Gets the user response to an `hx-prompt`, if any.                                                   |

{{< callout context="note" title="Note" icon="info-circle" >}}
The HtmxRequest class was constructed based on HTMX usage of Request headers.  You can find more information about HTMX request headers on the official [Htmx documentation site](https://htmx.org/reference/#request_headers).
{{< /callout >}}

## Working With HtmxRequest

`HtmxRequest` only has a dependency on HttpContext, so you can use it in any scoped dependency service that has access to HttpContext.  To manually create an HtmxRequest object you need only to create a new instance of the class as follows:

```csharp
var request = new HtmxRequest(httpContext);
```

The `HtmxResponse` object is accessible from the Response controller property:

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

## Target

Retrieves the `id` of the target element from the HTMX request if it exists.

**Example**

```csharp
string? targetId = Request.Htmx().Target;
```

## TriggerName

Obtains the `name` of the element that triggered the HTMX request if available.

**Example**

```csharp
string? triggerName = Request.Htmx().TriggerName;
```

## Trigger

Gets the `id` of the element that initiated the HTMX request if present.

**Example**

```csharp
string? triggerId = Request.Htmx().Trigger;
```

## Prompt

Retrieves the user response to an `hx-prompt` from the HTMX request, if any.

**Example**

```csharp
string? promptResponse = Request.Htmx().Prompt;
```
