---
title: "Configuration"
description: ""
summary: ""
date: 2024-02-05T12:11:27-05:00
lastmod: 2024-02-05T12:11:27-05:00
draft: false
menu:
  docs:
    htmx:
      parent: ""
      identifier: "configuration-9be46cbb530cd63819776bc374ed5c77"
weight: 100
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This document provides a comprehensive guide on configuring HTMX within your application.

{{< callout context="note" title="Note" icon="info-circle" >}}
The configuration portion or Rizzy was constructed based on HTMX head configuration.  You can find more information about HTMX head configuration on the official [Htmx documentation site](https://htmx.org/docs/#config).
{{< /callout >}}

## Customizing HTMX Configuration

### Adding HTMX Configuration in Program.cs

In `Program.cs`, you can add custom HTMX configurations using the `AddHtmx()` method. You can also add named configurations for your app. Here's an example:

```csharp
builder.Services.AddHtmx(config =>
    {
        config.SelfRequestsOnly = true;
    });

// Add an alternate named configuration
builder.Services.Configure<HtmxConfig>("articles", config =>
{
	config.SelfRequestsOnly = true;
	config.GlobalViewTransitions = true;
});    
```

The first call creates a default configuration, while the second call creates a named configuration using the configuration name "articles".

### Setting Configuration in HTML

To include configurations inside the `<head>` tag of your HTML document, use the `<HtmxConfigHeadOutlet/>` component:

```html
<HtmxConfigHeadOutlet/>
```

Named configurations can also be specified as a parameter:

```html
<HtmxConfigHeadOutlet Configuration="articles"/>
```

## HTMX Configuration Properties

Here is a description of the HTMX configuration properties that can be customized for your application:

| Property                 | Description                                                                                          |
|--------------------------|------------------------------------------------------------------------------------------------------|
| HistoryEnabled           | Enables history tracking.                                                                            |
| HistoryCacheSize         | Sets the size of the history cache.                                                                  |
| RefreshOnHistoryMiss     | Determines whether to refresh the page on history misses.                                             |
| DefaultSwapStyle         | Sets the default swap style.                                                                         |
| DefaultSwapDelay         | Sets the default swap delay.                                                                         |
| DefaultSettleDelay       | Sets the default settle delay.                                                                       |
| IncludeIndicatorStyles   | Specifies whether to include indicator styles.                                                        |
| IndicatorClass           | Sets the class for indicators.                                                                       |
| RequestClass             | Sets the class for requests.                                                                         |
| AddedClass               | Sets the class for added elements.                                                                    |
| SettlingClass            | Sets the class for settling elements.                                                                 |
| SwappingClass            | Sets the class for swapping elements.                                                                 |
| AllowEval                | Specifies whether to allow eval.                                                                      |
| AllowScriptTags          | Specifies whether to allow script tags.                                                               |
| InlineScriptNonce        | Sets the nonce for inline scripts.                                                                    |
| InlineStyleNonce         | Sets the nonce for inline styles.                                                                    |
| GenerateScriptNonce      | If true, will utilize an IRizzyNonceProvider instance to generate script nonces for CSP policies.    |
| GenerateStyleNonce       | If true, will utilize an IRizzyNonceProvider instance to generate style nonces for CSP policies.    |
| AttributesToSettle       | Specifies attributes to settle during the settling phase.                                             |
| UseTemplateFragments     | Specifies whether to use HTML template tags for parsing content.                                       |
| WsReconnectDelay         | Sets the WebSocket reconnect delay.                                                                  |
| WsBinaryType             | Sets the type of binary data received over WebSocket.                                                 |
| DisableSelector          | Sets the selector for disabling elements.                                                             |
| WithCredentials          | Specifies whether to allow cross-site Access-Control requests with credentials.                        |
| Timeout                  | Sets the request timeout.                                                                            |
| ScrollBehavior           | Sets the behavior for boosted links on page transitions.                                              |
| DefaultFocusScroll       | Specifies whether the focused element should be scrolled into view.                                    |
| GetCacheBusterParam      | Specifies whether to include a cache-busting parameter in GET requests.                                |
| GlobalViewTransitions    | Specifies whether to use the View Transition API when swapping in new content.                         |
| MethodsThatUseUrlParams  | Specifies methods to encode parameters in the URL.                                                    |
| SelfRequestsOnly         | Specifies whether to allow only AJAX requests to the same domain as the current document.             |
| IgnoreTitle              | Specifies whether to ignore the title of the document when a title tag is found in new content.       |
| ScrollIntoViewOnBoost    | Specifies whether the boosted element should be scrolled into view.                                   |


## Conclusion

By following this documentation, you can effectively configure HTMX in your library according to your application's requirements.