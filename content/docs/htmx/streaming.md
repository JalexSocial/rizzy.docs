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

Blazor's **Streaming Rendering** (`[StreamRendering]` attribute) is a powerful feature introduced in .NET 8. It enhances the perceived performance of server-side rendered (SSR) Blazor components by rendering the initial page structure quickly and then streaming updates for parts of the component that rely on long-running asynchronous operations (like fetching data).

HTMX excels at fetching and swapping HTML fragments dynamically without full page reloads. Combining these two technologies presents a challenge: how does Blazor's DOM patching via streaming interact correctly when HTMX might swap out the container holding the streaming component?

Rizzy provides the `rizzy-streaming` HTMX extension to bridge this gap.

## The Challenge

When a Blazor component uses `[StreamRendering]`, the initial render might contain placeholders. Once the async operations complete, Blazor sends DOM patch instructions over the connection to update these placeholders.

If HTMX performs a swap (`hx-swap`) on an element that *contains* a streaming Blazor component *before* the streaming updates have arrived or completed, those updates might target elements that no longer exist or have been replaced, leading to errors or unexpected behavior.

## The Solution: `hx-ext="rizzy-streaming"`

The `rizzy-streaming` HTMX extension provides **document-wide coordination** between Blazor's streaming rendering updates and HTMX's swapping mechanism. By including this extension, Rizzy helps ensure that streaming updates are correctly applied even when content is dynamically loaded or replaced via HTMX swaps.

It helps manage the lifecycle and potential conflicts, allowing you to leverage the benefits of both technologies simultaneously.

## How to Enable `rizzy-streaming`

To enable the extension, add the `hx-ext="rizzy-streaming"` attribute to the `<body>` tag (or another high-level common ancestor element) in your main application layout file (e.g., `AppLayout.razor` if using the Rizzy templates).

```html {title="AppLayout.razor" hl_lines=["2"]}
<!-- ... other head elements ... -->
<body hx-ext="rizzy-streaming">
    @Body

    <HtmxSwapContent/>
    <!-- ... other scripts ... -->
</body>
</html>
```

This ensures the extension monitors the entire document for potential interactions between streaming rendering and HTMX swaps.

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

@code {
    private WeatherForecast[]? forecasts;

    protected override async Task OnInitializedAsync()
    {
        // Simulate a long-running async task
        await Task.Delay(1500); // Simulate network latency or DB query

        var startDate = DateOnly.FromDateTime(DateTime.Now);
        var summaries = new[] { "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot" };
        forecasts = Enumerable.Range(1, 5).Select(index => new WeatherForecast
        {
            Date = startDate.AddDays(index),
            TemperatureC = Random.Shared.Next(-20, 55),
            Summary = summaries[Random.Shared.Next(summaries.Length)]
        }).ToArray();
    }

    // WeatherForecast class definition...
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
        // Return the StreamingWeather component as a partial view
        return PartialView<StreamingWeather>();
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
3.  The `LoadWeatherWidget` action returns the `StreamingWeather` component rendered as a partial view.
4.  HTMX receives the initial HTML containing the "Loading..." message and swaps it into `#weather-widget-container`.
5.  The `StreamingWeather` component's `OnInitializedAsync` continues running (`Task.Delay(1500)`).
6.  Once the delay finishes and `forecasts` is populated, Blazor attempts to send streaming updates.
7.  The `rizzy-streaming` extension, enabled on the `<body>`, helps coordinate these updates with the DOM, ensuring the weather table correctly replaces the "Loading..." message within the HTMX-managed container.

## Considerations

*   **Complexity:** While `rizzy-streaming` simplifies the integration, interactions between complex, nested streaming components and frequent HTMX swaps might still require careful testing.
*   **Performance:** Ensure your async operations within streaming components are efficient. Streaming rendering improves *perceived* load time but doesn't make the underlying operations faster.

## Conclusion

The `rizzy-streaming` HTMX extension provides a crucial link between Blazor's `[StreamRendering]` feature and HTMX's dynamic content swapping. By enabling this extension globally in your layout, you can confidently use streaming rendering in your Blazor components, knowing that Rizzy will help manage their interaction with HTMX-driven updates, leading to faster-feeling, interactive user experiences.
