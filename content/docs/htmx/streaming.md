---
title: "Blazor Streaming Rendering with HTMX"
description: "Learn how to use Blazor's Streaming Rendering feature alongside HTMX swaps using the rizzy-streaming HTMX extension."
summary: "Combine the performance benefits of Blazor's streaming rendering with the dynamic updates of HTMX using Rizzy's dedicated extension."
date: 2024-03-07T10:00:00-05:00 # Adjust date as needed
lastmod: 2024-03-07T10:00:00-05:00 # Adjust date as needed
draft: false
menu:
  docs:
    parent: "htmx" # Assuming parent is the HTMX section
    identifier: "streaming-a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2" # Unique identifier
    weight: 450 # Position within the HTMX section
toc: true
seo:
  title: "Using Blazor Streaming Rendering and HTMX with Rizzy"
  description: "Guide on integrating Blazor's [StreamRendering] attribute with HTMX partial updates via the rizzy-streaming extension."
---

## Overview

Blazor's **Streaming Rendering** (`[StreamRendering]` attribute) is a powerful feature introduced in .NET 8. It enhances the perceived performance of server‑side rendered (SSR) Blazor components by rendering the initial page structure quickly and then streaming updates for parts of the component that rely on long‑running asynchronous operations (like fetching data).

HTMX excels at fetching and swapping HTML fragments dynamically without full page reloads. Combining these two technologies presents a challenge: how does Blazor's DOM patching via streaming interact correctly when HTMX might swap out the container holding the streaming component?

Rizzy provides the `rizzy-streaming` HTMX extension to bridge this gap.

## The Challenge

When a Blazor component uses `[StreamRendering]`, the initial render might contain placeholders. Once the async operations complete, Blazor sends DOM patch instructions over the connection to update these placeholders.

If HTMX performs a swap (`hx-swap`) on an element that *contains* a streaming Blazor component *before* the streaming updates have arrived or completed, those updates might target elements that no longer exist or have been replaced, leading to errors or unexpected behavior.

## The Solution: Rizzy Streaming

The `rizzy-streaming` extension cooperates with htmx core instead of replacing its response handling:

1. It reads the response until the initial HTML is complete and hands htmx an ordinary response with just that HTML. htmx then runs its normal pipeline: the swap, `HX-*` response headers, `hx-status`, error events and `hx-sync` queueing.
2. The rest of the stream is read in the background. htmx waits for it before it fires `HX-Trigger` events, removes the request indicator and starts the next queued request, so triggers fire once, after the last update.
3. Each `<blazor-ssr>` update block is applied after the main swap. Blazor's `<blazor-ssr-end>` element patches the streamed component content in place; the extension defines it if Blazor's own script is not loaded.

If the connection breaks partway through, the error is logged to the console and `htmx:error` is raised on the requesting element.

The extension raises `htmx:rizzy:stream:open`, `htmx:rizzy:stream:block` and `htmx:rizzy:stream:close` on the requesting element.

## How to Enable Rizzy Streaming

Nothing to enable: the Rizzy client script registers `rizzy-streaming` (along with Rizzy's other extensions) when it loads. htmx 4 has no `hx-ext` attribute. Load htmx first, then Rizzy:

```html {title="AppLayout.razor"}
<head>
    <RzHeadOutlet />
    <RzScripts />
</head>
```

If you restrict extensions, Rizzy keeps its own (including `rizzy-streaming`) in the allow-list; see [Extensions]({{<ref "/docs/htmx/extensions.md">}}). Streaming also works together with the Preload extension, which serves clicks from a response fetched on `mousedown`.

## Using Streaming Components

On the component side, simply use the standard `[StreamRendering]` attribute on any Blazor component where you want to enable streaming rendering. Rizzy and the `rizzy-streaming` extension handle the necessary coordination with HTMX behind the scenes.

```razor {title="StreamingWeather.razor"}
@using Rizzy
@attribute [StreamRendering]

<RzPageTitle>Streaming Weather</RzPageTitle>

<h1>Weather Forecast</h1>

@if (forecasts == null)
{
    <p><em>Loading weather forecast... Please wait.</em></p>
}
else
{
    <table class="table">
        <thead>
            <tr><th>Date</th><th>Temp. (C)</th><th>Summary</th></tr>
        </thead>
        <tbody>
            @foreach (var forecast in forecasts)
            {
                <tr>
                    <td>@forecast.Date.ToShortDateString()</td>
                    <td>@forecast.TemperatureC</td>
                    <td>@forecast.Summary</td>
                </tr>
            }
        </tbody>
    </table>
}
```

## Example Scenario

Imagine you have a dashboard where users can click a button to load the weather forecast into a specific section using HTMX.

**Controller Action:**

```csharp
// In your HomeController or relevant controller
public class DashboardController : RzController
{
    [HttpGet]
    public IResult LoadWeatherWidget()
    {
        // View<T> renders just the component for an htmx request that targets an element,
        // and streams it progressively (see "View or PartialView" below).
        return View<StreamingWeather>();
    }
}
```

**Triggering Element (e.g., in Dashboard.razor):**

```html
<div id="weather-widget-container">
    <!-- Initial content or placeholder -->
    <p>Click the button to load the weather.</p>
</div>

<button class="btn btn-primary"
        hx-get="/Dashboard/LoadWeatherWidget"
        hx-target="#weather-widget-container"
        hx-swap="innerHTML">
    Load Weather
</button>
```

**Flow:**

1.  User clicks the "Load Weather" button.
2.  HTMX makes a GET request to `/Dashboard/LoadWeatherWidget`.
3.  The `LoadWeatherWidget` action returns the `StreamingWeather` component. Because the request targets an element, no layout is rendered.
4.  HTMX receives the initial HTML containing the "Loading..." message and swaps it into `#weather-widget-container`.
5.  The `StreamingWeather` component's `OnInitializedAsync` continues running (`Task.Delay(1500)`).
6.  Once the delay finishes and `forecasts` is populated, Blazor sends streaming updates to render the final table.
7.  The `rizzy-streaming` extension coordinates these updates with HTMX, ensuring the weather table correctly replaces the "Loading..." message within the HTMX-managed container.

## View or PartialView

Both stream, but only `View<T>` streams **progressively** for htmx requests:

- **`View<T>`** wraps the htmx fragment in a minimal `<html><body>` document, so the client can tell where the initial HTML ends. The placeholder is swapped in immediately and replaced when the data arrives.
- **`PartialView<T>`** sends a bare fragment. The client cannot tell where the initial HTML ends, so it waits for the whole stream and swaps the finished content once. The result is correct, but the user sees nothing until the data is ready.

Use `View<T>` for components with `[StreamRendering]`.

## Considerations

* **Complexity:** While `rizzy-streaming` simplifies the integration, interactions between complex, nested streaming components and frequent HTMX swaps might still require careful testing.
* **Performance:** Ensure your async operations within streaming components are efficient. Streaming rendering improves *perceived* load time but doesn't make the underlying operations faster.

## Conclusion

The `rizzy-streaming` HTMX extension provides a crucial link between Blazor's `[StreamRendering]` feature and HTMX's dynamic content swapping. By including this extension globally in your layout (via the Rizzy client script), you can confidently use streaming rendering in your Blazor components, knowing that Rizzy will help manage their interaction with HTMX‑driven updates, leading to faster‑feeling, interactive user experiences.