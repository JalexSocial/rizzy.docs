
---
title: "Getting Started"
description: "Install Rizzy 6, register it, create the root layout and render your first htmx-driven component."
summary: ""
date: 2024-02-05T12:07:02-05:00
lastmod: 2026-11-08T12:00:00-05:00
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

This guide sets up Rizzy in an ASP.NET Core app and renders a Razor component that htmx updates
without a page reload. Upgrading an existing Rizzy 5 app? See [Upgrading to Rizzy 6]({{<ref "/docs/reference/upgrading.md">}}).

## Requirements

- **.NET 10** or newer.
- **htmx 4.0.1** or newer, loaded by your layout (from a CDN or your own static files).

## Installation

```sh
dotnet add package Rizzy
```

The `Rizzy` package brings the matching `Rizzy.Htmx` package and the Rizzy client script
(`_content/Rizzy/js/rizzy.js`). The three are always released together with the same version.

## Register Rizzy (Program.cs)

<img src="/images/getting-started-builder.svg" class="img-fluid" alt="Builder Services">

```csharp {title="Program.cs"}
using Rizzy;
using MyApp; // the namespace of your components (your project's root namespace)

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews(); // only if you use MVC controllers
builder.Services.AddRizzy(options =>
{
    options.RootComponent = typeof(HtmxApp<AppLayout>);    // the HTML document
    options.DefaultLayout = typeof(HtmxLayout<MainLayout>); // page chrome, skipped for htmx fragments
});

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();   // serves _content/Rizzy/js/rizzy.js
app.UseRouting();
// app.UseAuthentication(); app.UseAuthorization(); if you use them
app.UseAntiforgery();
app.UseRizzy();

app.MapGet("/", (IRizzyService rizzy) => rizzy.View<Home>());
app.MapPost("/greet", (IRizzyService rizzy) => rizzy.PartialView<Greeting>(new { Name = "htmx" }));
app.MapDefaultControllerRoute();

app.Run();
```

What this does:

- **`AddRizzy(...)`** registers everything Rizzy needs, including htmx support (`AddHtmx`) and Razor
  components (`AddRazorComponents`). Repeated calls are safe. Call `AddHtmx(config => ...)` as well only
  to change the [htmx configuration]({{<ref "/docs/htmx/configuration.md">}}).
- **`RootComponent`** is the component that renders the HTML document. `HtmxApp<AppLayout>` renders
  your `AppLayout` for normal requests and skips it for htmx fragment requests. Startup fails if it is
  `null`, and a warning is logged if you leave the default (which renders no `<head>`).
- **`DefaultLayout`** applies to components without an `@layout` directive. `HtmxLayout<MainLayout>`
  renders `MainLayout` for full pages, boosted navigation and back/forward, and skips it for htmx
  requests that target one element. See [Layouts]({{<ref "/docs/components/layout.md">}}).
- **`AddControllersWithViews()`** (rather than `AddControllers()`) is needed if your MVC actions use
  `[ValidateAntiForgeryToken]`; it registers the MVC antiforgery filters.
- **`UseAntiforgery()`** goes after routing and authentication. **`UseRizzy()`** goes after it.

## Add `_Imports.razor`

```razor {title="_Imports.razor"}
@using Microsoft.AspNetCore.Components.Web
@using Rizzy
```

## Create the root layout

The root layout renders **`<RzHeadOutlet />`** and then **`<RzScripts />`** in its `<head>`.
`RzHeadOutlet` renders Blazor's `HeadOutlet` (page titles and `<HeadContent>`) plus Rizzy's
`<meta name="htmx-config">` tag, which carries your htmx settings and the antiforgery token.
`RzScripts` then loads htmx (the tested version, with a subresource integrity hash), the Rizzy script
and any [extensions]({{<ref "/docs/htmx/extensions.md">}}) you enable. htmx reads the meta tag once,
when its script loads, so the outlet comes first.

```razor {title="AppLayout.razor"}
@inherits LayoutComponentBase

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <base href="/" />
    <RzHeadOutlet />
    <RzScripts />
</head>
<body>
    @Body
</body>
</html>
```

```razor {title="MainLayout.razor"}
@inherits LayoutComponentBase

<main>@Body</main>
```

The Rizzy script registers Rizzy's own htmx extensions (antiforgery, CSP nonces, streaming
rendering, confirm dialogs) when it loads; no `hx-ext` attributes are needed. To load the scripts
yourself instead, see `HtmxConfig.Scripts` on the [Extensions]({{<ref "/docs/htmx/extensions.md">}}) page.

## Write components

```razor {title="Home.razor"}
<RzPageTitle>Home</RzPageTitle>

<h1>Hello</h1>
<button hx-post="/greet" hx-target="#greeting">Greet</button>
<div id="greeting"></div>
```

```razor {title="Greeting.razor"}
<p>Hello, @Name!</p>

@code {
    [Parameter] public string? Name { get; set; }
}
```

Plain `hx-*` attributes work, and so does the [typed `Hx` builder]({{<ref "/docs/htmx/attributes.md">}}):
`<button @attributes="@(Hx.Post("/greet").Target("#greeting"))">Greet</button>`.

Run the app and click the button. htmx posts to `/greet` (rizzy.js adds the antiforgery token), and
`PartialView<Greeting>` returns just the fragment, which htmx swaps into `#greeting`.
`View<Home>` renders the full page for a normal request, but only the component for an htmx request
that targets an element.

{{< callout context="note" title="Keep the console open" icon="info-circle" >}}
htmx 4 logs every error to the browser console, and Rizzy logs one clear warning when the page is
misconfigured (for example a root layout without `<RzHeadOutlet />`). See
[Troubleshooting]({{<ref "/docs/reference/troubleshooting.md">}}).
{{< /callout >}}

## Next steps

1. Use MVC controllers: inherit from `RzController` (or `RzControllerWithViews`) and return
   `View<T>()`/`PartialView<T>()`. See [Setup with MVC Controllers]({{<ref "/docs/framework/mvc/setup.md">}}).
2. Build forms with server-side validation: [Validation]({{<ref "/docs/forms/validation.md">}}).
3. Send extra fragments in one response: [Out of Band Swapping]({{<ref "/docs/htmx/swaps.md">}}).
4. Control htmx from the server: [Response]({{<ref "/docs/htmx/response.md">}}).
5. Lock down scripts: [Content Security Policy]({{<ref "/docs/introduction/contentsecurity.md">}}).

The `src/RizzyDemo` app in the [Rizzy repository](https://github.com/JalexSocial/Rizzy) shows all of
these together, including streaming rendering, 422 validation and a nonce-based CSP.
