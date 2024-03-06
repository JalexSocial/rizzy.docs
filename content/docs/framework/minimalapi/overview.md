---
title: "Overview"
description: ""
summary: ""
date: 2024-03-06T09:42:53-05:00
lastmod: 2024-03-06T09:42:53-05:00
draft: false
weight: 50
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---
Minimal APIs in .NET 8 offer a streamlined approach for building HTTP APIs and web applications with less boilerplate code. They are designed to make the development process faster and more efficient, allowing developers to focus on the business logic rather than the underlying infrastructure. Minimal APIs are ideal for small to medium-sized projects and microservices, providing a simple yet powerful way to handle requests and responses.

Rizzy works with Minimal APIs by providing the ability to render both views and partial views. When Rizzy is added to your project on startup it adds a scoped service of type IRizzyService.

## RizzyService

### Properties

- **ViewContext**: Holds the view context necessary for rendering Razor components, providing configuration and rendering information.

### Methods

#### View Rendering

- **View\<TComponent\>(object? data = null)**: Renders a full view using a specified Razor component. Optionally accepts dynamic data to pass to the component.
  - `TComponent`: The type of Razor component to render.
  - `data`: Dynamic data to pass to the component, optional.

- **View\<TComponent\>(Dictionary<string, object?> data)**: Renders a full view using a specified Razor component with explicitly provided data in dictionary form.
  - `TComponent`: The type of Razor component to render.
  - `data`: A dictionary containing the data to pass to the component.

#### Partial View Rendering

- **PartialView\<TComponent\>(object? data = null)**: Renders a partial view using a specified Razor component, suitable for inclusion in other views. Optionally accepts dynamic data.
  - `TComponent`: The type of Razor component to render as a partial view.
  - `data`: Dynamic data to pass to the component, optional.

- **PartialView\<TComponent\>(Dictionary<string, object?> data)**: Renders a partial view using a specified Razor component with explicitly provided data in dictionary form. Intended for component inclusion in other views.
  - `TComponent`: The type of Razor component to render as a partial view.
  - `data`: A dictionary containing the data to pass to the component.

#### Utilities

- **CurrentActionUrl**: A utility property that provides the current action method URL, useful for specifying form action targets within Razor Component views. Automatically derived from the current HTTP request.


