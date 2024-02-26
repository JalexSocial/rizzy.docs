---
title: "Setup with MVC Controllers"
description: ""
summary: ""
date: 2024-02-25T18:39:34-05:00
lastmod: 2024-02-25T18:39:34-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "setup-68f0d8c4af328cc4a6370500fcc4986e"
weight: 50
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Rizzy enhances ASP.NET MVC applications by integrating Razor Components, offering a seamless way to incorporate component-based views within your traditional MVC architecture. This guide outlines how to utilize Rizzy to leverage the power of Razor Components in your MVC controllers.

## Getting Started

### Upgrading Your Controller

Alter your MVC controllers to inherit from `RzController` for basic functionality:

```csharp {title="HomeController.cs"}
public class HomeController : RzController
{
    // Controller actions here
}
```

For applications that require returning MVC Views alongside Razor Components, use `RzControllerWithViews`:

```csharp {title="HomeController.cs"}
public class HomeController : RzControllerWithViews
{
    // Controller actions here, with the ability to return MVC Views
}
```

## Rendering Views and Partial Views

Rizzy enables your controllers to render Razor Components as full views or partial views, providing a flexible approach to building your UI. This is achieved through the following methods available in `RzController`. Each `TComponent` type must be a Razor Component:

- **View&lt;TComponent&gt;(object? data = null)**: Renders the specified Razor Component as a full view. This method allows you to pass parameter data to the component, enriching your UI with interactive and data-driven components.

- **View&lt;TComponent&gt;(Dictionary&lt;string, object?&gt; data)**: This overload accepts a dictionary of data, providing a structured way to pass parameters to your Razor Component. It's particularly useful when you have multiple pieces of data to pass to the component.

- **PartialView&lt;TComponent&gt;(object? data = null)**: Renders a specified Razor Component as a partial view. This method is ideal for rendering components that are meant to be part of a larger page, such as widgets or reusable UI segments, without the layout associated with full views.

- **PartialView&lt;TComponent&gt;(Dictionary&lt;string, object?&gt; data)**: Similar to its full view counterpart, this method accepts a dictionary of data for rendering the component. It enables the inclusion of complex components within existing views, enhancing the modularity of your application.

Here's an example from `HomeController` where we return a Razor Component called `HomeIndex`:

```csharp
    public IResult Index()
    {
        return View<HomeIndex>();
    }
```

To utilize a familiar MVC-style feel to passing parameters to components you can still opt to call your parameter `Model` as follows:

```csharp {title="HomeController.cs"}
    public IResult Index()
    {
        var myModel = new MyViewModel();

        return View<Message>(new { Model = myModel });
    }
```

Then inside your Razor Component you just need to call your parameter `Model`:

```csharp {title="Message.razor"}

@Model.Message

@code {
  [Parameter]
  public MyViewModel? Model {get; set;} = default!;
}
```

## JSON Serialization

Rizzy provides methods for serializing data to JSON, facilitating the development of APIs or dynamic web applications that require JSON responses:

- **Json(object? data)**: Serializes the provided data object to JSON. This method simplifies the process of returning JSON responses from your controller actions.

- **Json(object? data, object? serializerSettings)**: Allows for custom serialization by accepting serializer settings. This method gives you control over the serialization process, enabling you to tailor the JSON response according to your requirements.

## Leveraging Razor Components

By inheriting from `RzController` or `RzControllerWithViews`, you unlock the ability to seamlessly integrate Razor Components into your MVC applications. This integration bridges the gap between traditional MVC development and modern component-based architectures, offering you the flexibility to build rich, interactive web applications using ASP.NET's robust ecosystem.

Rizzy's approach to rendering Razor Components as views or partial views directly within MVC controllers enriches your application's UI capabilities, making it easier to develop complex, data-driven interfaces with the reusable and maintainable codebase that Razor Components provide.