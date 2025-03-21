---
title: "Getting Started"
description: ""
summary: ""
date: 2024-02-05T12:07:02-05:00
lastmod: 2024-02-05T12:07:02-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "getting-started-b61c1d09773be2e6c7aa6e8dbfc38058"
weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This README provides instructions on how to incorporate the Rizzy library into your ASP.NET projects. Rizzy leverages .NET 8 capabilities to enhance your web application development process, particularly focusing on HTMX integration.

## Requirements

- **.NET Version**: .NET 8 or newer.

## Installation

Rizzy is available as a NuGet package. You can install it using the .NET CLI with the following command:

```sh
dotnet add package Rizzy
```

For the latest version and more details, visit the [Rizzy NuGet package page](https://www.nuget.org/packages/Rizzy).

## Configuration

After installing Rizzy, you need to configure it in your `Program.cs` or startup configuration file. This setup involves specifying your application's root component, default layout, antiforgery strategy, and HTMX configurations. Here's how to add Rizzy to your application builder:

```csharp
builder.Services.AddRizzy(config =>
    {
        config.RootComponent = typeof(HtmxApp<AppLayout>);
        config.DefaultLayout = typeof(HtmxLayout<MainLayout>);
        config.AntiforgeryStrategy = AntiforgeryStrategy.GenerateTokensPerPage;
    })
    .WithHtmxConfiguration(config =>
    {
        config.SelfRequestsOnly = true;
    })
    .WithHtmxConfiguration("articles", config =>
    {
        config.SelfRequestsOnly = true;
        config.GlobalViewTransitions = true;
    });
```

### Configuration Details

- **RootComponent**: Defines the default root component for your component hierarchy. Wrapping a Layout in `HtmxApp` ensures that when a page is rendered with HTMX, it won't render the Layout.
- **DefaultLayout**: Applied to any view that doesn't specifically specify a Layout attribute.
- **AntiforgeryStrategy**: Configures antiforgery tokens behavior. Options include turning off antiforgery tokens, generating them on each request, or generating them on each full-page reload.

### HTMX Configuration

`WithHtmxConfiguration` allows setting up HTMX-specific settings, supporting both default and named configurations. In this example we configure:

- **SelfRequestsOnly**: Restricts HTMX requests to the same origin.
- **GlobalViewTransitions**: Enables global view transitions for the specified named configuration.

Multiple configurations can be defined for different parts of your application, offering granular control over HTMX behavior.

For more detailed information on configuring HTMX in Rizzy, refer to the [Htmx Configuration Documentation](https://jalexsocial.github.io/rizzy.docs/docs/htmx/configuration/).

## Conclusion

Rizzy offers a powerful and flexible way to enhance your ASP.NET applications with advanced HTMX integration and configuration options.