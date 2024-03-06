---
title: "Mapping Endpoints"
description: ""
summary: ""
date: 2024-03-06T09:59:09-05:00
lastmod: 2024-03-06T09:59:09-05:00
draft: false
weight: 199
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## How to Use Rizzy with Minimal APIs

First, let's define a component that will display a message:

```html {title="LoveHtmx.razor"}
<div class="alert alert-info">
	<span class="text-lg-center">
		@Message
	</span>
</div>

@code{
    [Parameter]
    public string? Message { get; set; } = "I ❤️ HTMX";
}
```

### Configure the Endpoint

Configure an endpoint in your Minimal API setup that utilizes Rizzy to render the above partial view. This demonstrates how to use Rizzy's `PartialView` method to serve dynamic content based on the `Message` parameter.  If you want your View to be an entire page, utilize the View method.

```csharp
app.MapGet("/love-htmx",
    ([FromServices] IRizzyService rizzy) => rizzy.PartialView<LoveHtmx>(new { Message = "I ❤️ ASP.NET Core" }));
```

### Conclusion

After configuring the endpoint, run your application. When a client sends a request to `/love-htmx`, the server uses Rizzy to render the partial view with the message "I ❤️ ASP.NET Core". This demonstrates a basic but powerful integration of Rizzy with Minimal APIs in .NET 8 for rendering dynamic views.
