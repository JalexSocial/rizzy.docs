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
weight: 12
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This guide provides instructions on how to incorporate the Rizzy library into your ASP.NET projects. Rizzy leverages .NET 8 capabilities to enhance your web application development process, particularly focusing on integrating Razor Components with HTMX.

## Requirements

- **.NET Version**: .NET 8 or newer.

## Installation

Rizzy is available as a NuGet package. You can install it using the .NET CLI or the Visual Studio NuGet Package Manager.

**Using .NET CLI:**

```sh
dotnet add package Rizzy
dotnet add package Rizzy.Htmx # Recommended: Also add the HTMX helper library
```

**Using Visual Studio:**

1.  Right-click on your project in Solution Explorer and select "Manage NuGet Packages...".
2.  Search for `Rizzy` and click Install.
3.  Search for `Rizzy.Htmx` and click Install.

For the latest versions and more details, visit the package pages:
- [Rizzy on NuGet](https://www.nuget.org/packages/Rizzy)
- [Rizzy.Htmx on NuGet](https://www.nuget.org/packages/Rizzy.Htmx)

## Configuration (Program.cs)

<img src="/images/getting-started-builder.svg" class="img-fluid" alt="Builder Services">

After installing the packages, you need to configure Rizzy and its HTMX integration in your `Program.cs` file. This involves registering necessary services and setting up configurations.

```csharp
using Rizzy;
using Rizzy.Configuration;
using Rizzy.Htmx;
using Rizzy.Htmx.Antiforgery; // For AntiforgeryStrategy enum
using YourApp.Components.Layout; // Replace with your actual layout namespaces

var builder = WebApplication.CreateBuilder(args);

// Add standard services like Controllers, Razor Components etc.
builder.Services.AddControllers(); // If using MVC
builder.Services.AddRazorComponents();

// --- Rizzy Configuration ---

// 1. Add Rizzy Core Services
// This configures Rizzy-specific services and options.
builder.Services.AddRizzy(config =>
{
    // RootComponent: The main component wrapping your app.
    // HtmxApp<T> ensures layouts aren't re-rendered on HTMX partial requests.
    config.RootComponent = typeof(HtmxApp<AppLayout>); // Replace AppLayout with your root layout

    // DefaultLayout: Applied to components without an explicit @layout directive.
    // HtmxLayout<T> handles switching between full/minimal layouts for HTMX requests.
    config.DefaultLayout = typeof(HtmxLayout<MainLayout>); // Replace MainLayout with your default content layout
});

// 2. Add HTMX Configuration Services (Optional but Recommended)
// This configures the *default* HTMX behavior via HtmxConfig.
builder.Services.AddHtmx(config =>
{
    // Example: Restrict HTMX requests to the same origin by default.
    config.SelfRequestsOnly = true;

    // Example: Enable generation of nonces for inline styles/scripts via IRizzyNonceProvider
    // Requires IRizzyNonceProvider to be registered (AddRizzy does this).
    // Use with caution regarding CSP implications. See CSP docs.
    // config.GenerateScriptNonce = true;
    // config.GenerateStyleNonce = true;

    // Add other default HTMX settings as needed...
});

// --- End Rizzy Configuration ---


// --- Build the App ---
var app = builder.Build();

// --- Configure Middleware Pipeline ---
// Ensure middleware is in the correct order

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

// Add Authentication/Authorization middleware if used

app.UseAntiforgery(); // Crucial: Must be after UseRouting and UseAuthentication/UseAuthorization

// Add Rizzy Middleware (Handles specific HTMX request processing, like Nonce headers)
app.UseRizzy();

// --- Map Endpoints ---
app.MapControllers(); // If using MVC
// Map Minimal API endpoints...

app.Run();
```

### Configuration Details Explained

*   **`AddRizzy(config => ...)`**: Configures the core Rizzy library.
    *   `RootComponent`: Typically `HtmxApp<YourAppLayout>` to handle layout switching correctly for HTMX requests.
    *   `DefaultLayout`: Typically `HtmxLayout<YourMainLayout>` applied to components without an `@layout` directive.
    *   `AntiforgeryStrategy`: Controls how antiforgery tokens are managed, important for security with HTMX POST requests. `GenerateTokensPerPage` is often suitable.
*   **`AddHtmx(config => ...)`**: Configures the *default* `HtmxConfig` used when rendering the `<HtmxConfigHeadOutlet />` without a specific configuration name. See [HTMX Configuration]({{<ref "/docs/htmx/configuration.md">}}) for all options.
*   **`app.UseAntiforgery()`**: Essential for security. Must be placed correctly in the middleware pipeline.
*   **`app.UseRizzy()`**: Adds the Rizzy middleware for handling specific HTMX interactions (e.g., response nonce headers). Place it *after* `UseAntiforgery()`.

## Conclusion

With Rizzy installed and configured, you can now start building your application using Razor Components rendered server-side and enhanced with HTMX. Remember to:

1.  Inherit your MVC controllers from `RzController` or `RzControllerWithViews`.
2.  Use `View<TComponent>` and `PartialView<TComponent>` methods in your controllers/endpoints.
3.  Utilize Rizzy's components (like `RzInput*`, `HtmxSwapService`) as needed.
4.  Add HTMX attributes directly to your HTML elements within `.razor` files.

Refer to the specific documentation sections for details on Components, Forms, HTMX features, and Framework integration.
```