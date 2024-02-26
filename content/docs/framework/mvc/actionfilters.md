---
title: "HTMX Action Filters"
description: ""
summary: ""
date: 2024-02-26T07:19:20-05:00
lastmod: 2024-02-26T07:19:20-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "actionfilters-e2ef1041c8d3f2359929e403e3fba5f0"
weight: 150
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

HTMX facilitates partial webpage updates via AJAX-style requests, enhancing user experience without relying on extensive JavaScript. With Rizzy, special action filters for handling HTMX requests and responses can be used to reduce some of the boilerplate code you will frequently use with the library. These filters are categorized into HTMX Request Filters and HTMX Response Filters.

## HTMX Request Filters

HTMX Request Filters ensure that certain actions or controllers respond exclusively to HTMX requests.

### [HtmxRequest]

`HtmxRequest` is an action filter attribute that will conditionally execute actions based on HTMX request headers. It optionally checks for requests targeting a specific element by it's Hx-Target Id.

#### Example

```csharp
public class SampleController : RzController
{
    // Responds to all HTMX requests
    [HttpGet("data")]
    [HtmxRequest]
    public IActionResult GetData()
    {
        return Ok(new { message = "HTMX response" });
    }

    // Responds only to HTMX requests targeting '#specific-target'
    [HttpGet("specific-data")]
    [HtmxRequest(Target = "#specific-target")]
    public IActionResult GetSpecificData()
    {
        return Ok(new { message = "Response for a specific HTMX target" });
    }
}
```

## HTMX Response Filters

HTMX Response Filters modify the HTTP response to direct client-side HTMX behaviors such as redirection, refreshing, or updating page segments. 

### [HtmxResponse]

`HtmxResponse` filter applies HTMX-specific response headers for client-side actions like redirection or refreshing part of the page based on server-side outcomes.

#### Available Properties

Below is a list of all available attributes you can set on `[HtmxResponse]` along with their descriptions:

- **Location:** Specifies a URL to which the client-side should be redirected without a full page reload. This enables server-side redirection logic to be applied client-side seamlessly.

- **PushUrl:** Instructs the client-side to add a new URL to the browser's history stack. This is useful for updating the URL without reloading the page, maintaining the SPA (Single Page Application) feel.

- **PreventBrowserHistoryUpdate:** When set to `true`, prevents the browser's history from being updated. This can be used to avoid adding entries to the history stack during certain operations.

- **PreventBrowserCurrentUrlUpdate:** Setting this to `true` stops the browser's current URL from being updated. This is useful in scenarios where you want to update the page content without changing the URL displayed in the address bar.

- **Redirect:** Initiates a client-side redirect to a specified URL. This is another way to perform redirections, similar to `Location` but more explicitly designed for HTMX's redirect capabilities.

- **Refresh:** A boolean value that, when set to `true`, triggers a full page refresh from the client side. This is equivalent to the user hitting the refresh button on their browser, useful for re-fetching the entire page content.

- **ReplaceUrl:** Replaces the current URL in the browser's address bar with the specified one. Unlike `PushUrl`, this doesn't add a new entry to the history stack but modifies the current state.

- **Reswap:** Specifies how the response will be swapped on the client side, using HTMX swap strategies. This controls the animation or transition effect used when updating the page content.

- **Retarget:** Changes the target element for the content update to a different element specified by a CSS selector. This allows server-side logic to dynamically target different parts of the page for updates.

- **StopPolling:** When set to `true`, sends a status code that instructs HTMX to stop polling. This is useful for stopping client-side polling based on server-side conditions.

- **Reselect:** Chooses a specific part of the response for swapping, using a CSS selector. This allows you to refine exactly what part of the server response should be used to update the client side.

Each of these attributes modifies the HTTP response headers in a way that HTMX on the client side can interpret and act upon, allowing for a rich, dynamic user experience with minimal effort from the server side.

#### Example

```csharp {title="SampleController.cs"}
public class SampleController : RzController
{
    // Initiates client-side redirection to '/new-location'
    [HttpGet("redirect")]
    [HtmxResponse(Redirect = "/new-location")]
    public IActionResult HtmxRedirect()
    {
        return Ok();
    }

    // Causes a client-side page refresh
    [HttpGet("refresh")]
    [HtmxResponse(Refresh = true)]
    public IActionResult HtmxRefresh()
    {
        return Ok();
    }

    // Pushes a new URL to the browser history stack
    [HttpGet("push-url")]
    [HtmxResponse(PushUrl = "/new-page")]
    public IActionResult HtmxPushUrl()
    {
        return Ok();
    }
}
```

These filters enable direct and efficient integration between server-side .NET actions and client-side HTMX functionality for dynamic web applications.