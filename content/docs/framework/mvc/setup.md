---
title: "Setup with MVC Controllers"
description: "Integrate Rizzy with your ASP.NET MVC controllers to render Razor Components, automatically cascade ModelState, and combine multiple render fragments."
date: 2024-02-25T18:39:34-05:00
lastmod: 2024-02-25T18:39:34-05:00
draft: false
menu:
  docs:
    identifier: "setup-68f0d8c4af328cc4a6370500fcc4986e"
weight: 50
toc: true
seo:
  title: "Setup with MVC Controllers"
  description: "A detailed guide on integrating Rizzy with MVC controllers, cascading ModelState, and rendering multiple render fragments."
---

Rizzy transforms your traditional ASP.NET MVC applications by integrating Razor Components into your controllers. This powerful integration enables you to build modern, interactive UIs while still leveraging the familiar MVC architecture. In this guide, you will learn how to render Razor Component views and partial views, combine multiple render fragments, and handle form data within your components.

## Getting Started

To begin, update your MVC controllers so that they inherit from either `RzController` or `RzControllerWithViews`. This allows Rizzy to automatically cascade ModelState and pass any necessary data to your Razor Components.

For example, create a controller that renders Razor Component views:

```csharp
// HomeController.cs - Full Component View
public class HomeController : RzController
{
    public IResult Index()
    {
        // Renders the HomeIndex component as a full view.
        return View<HomeIndex>();
    }
}
```

If your application needs to return both Razor Component views and traditional MVC views, use:

```csharp
// HomeController.cs - Mixed Views
public class HomeController : RzControllerWithViews
{
    // Controller actions can return both Razor Component views and standard MVC views.
}
```

## Rendering Views and Partial Views

Rizzy extends your controllers with methods to render Razor Components as full views or partial views. Here are the key methods provided by `RzController`:

- **View&lt;TComponent&gt;(object? data = null)**  
  Renders the specified Razor Component as a full view. Pass parameters using an anonymous object.

- **View&lt;TComponent&gt;(Dictionary&lt;string, object?&gt; data)**  
  Accepts a dictionary of parameters, which is useful when passing multiple pieces of data.

- **PartialView&lt;TComponent&gt;(object? data = null)**  
  Renders the specified Razor Component as a partial view without the outer layout. Ideal for widgets or reusable UI segments.

- **PartialView&lt;TComponent&gt;(Dictionary&lt;string, object?&gt; data)**  
  Works like the full view overload but accepts a dictionary.

For example, to render a component named `HomeIndex` with parameters:

```csharp
public IResult Index()
{
    var myModel = new MyViewModel { Message = "Hello from MVC!" };
    return View<HomeIndex>(new { Model = myModel });
}
```

## Rendering Multiple Render Fragments

Rizzy also supports rendering multiple render fragments in a single partial view. This feature is especially useful when you want to compose a page from several independent UI sections without wrapping them in one large component.

Use the overload that accepts an array of `RenderFragment` objects:

**MultiFragments.razor**

```razor
@code {
    // A simple header fragment defined with inline markup.
    public static RenderFragment Header => @<header>This is the header section.</header>;

    // A main content fragment that accepts dynamic content as a parameter.
    public static RenderFragment MainContent(string content) => 
		@<main>
			@content
		</main>;

    // A footer fragment defined with inline markup.
    public static RenderFragment Footer => @<footer>This is the footer section.</footer>;
}
```

**Controller Method**
```csharp
public IResult MultiFragmentView()
{
    // Render all fragments together as a composite partial view.
    return PartialView(
        MultiFragments.Header, 
        MultiFragments.MainContent("This is the main content area."), 
        MultiFragments.Footer
    );
}
```

In this example, the header, content, and footer fragments are rendered sequentially to build a complete composite view, making your UI modular and maintainable.

## Handling Form Data

Rizzy simplifies the process of handling form data by automatically cascading the ModelState to your views and partial views. This ensures that any validation errors from your controller are available within your Razor Components.

A key component in this process is `<RzInitialValidator>`. When placed inside an `EditForm`, it checks whether ModelState errors exist. If errors are present, it transfers them to the form. Otherwise, it automatically invokes the form's `Validate` method so that your component begins with accurate validation.

There are two approaches to working with form data in your components:

### 1. Passing the Model as a Parameter

In this approach, the controller passes the model explicitly to the view, and your component declares a property decorated with `[Parameter]`. This method is useful when you want to explicitly control the data being sent to your component.

**Controller Example:**

```csharp
public IResult SubmitForm(Person person)
{
    if (!ModelState.IsValid)
    {
        // Pass the model explicitly to the partial view.
        return PartialView<FormComponent>(new { Model = person });
    }
    // Process valid data...
    return View<SuccessComponent>();
}
```

**Razor Component Example:**

```razor
@* FormComponent.razor *@
<EditForm Model="@Model">
    <RzInitialValidator />
    <!-- Form inputs go here -->
</EditForm>

@code {
    [Parameter]
    public Person? Model { get; set; }
}
```

### 2. Binding the Model Directly from the Form

Alternatively, you can allow the form to supply the model data directly to your component by using `[SupplyParameterFromForm]`. In this scenario, you do not need to pass the model from your controller.

{{< callout context="note" title="Note on [SupplyParameterFromForm] Integration" icon="info-circle" >}}
Rizzy aims to make integrating Blazor components into MVC as smooth as possible. To enable the convenient `[SupplyParameterFromForm]` attribute for binding data directly from forms in this context, Rizzy carefully uses **reflection** to connect with certain internal ASP.NET Core services (like `HttpContextFormDataProvider`).

This technique bridges a gap where public APIs are not currently available, avoiding the need to replicate complex framework logic within Rizzy itself. While this integration is designed to be robust, it's important to understand that it interfaces with non-public parts of the .NET framework. As such, significant changes in future .NET versions *could* impact this specific feature, potentially requiring adjustments in Rizzy to maintain compatibility. We are committed to monitoring this and ensuring Rizzy works smoothly across .NET updates.
{{< /callout >}}

**Controller Example:**

```csharp
public IResult SubmitForm()
{
    // No need to pass the model explicitly; it will be bound from the form.
    return PartialView<FormComponent>();
}
```

**Razor Component Example:**

```razor
@* FormComponent.razor using form binding *@
<EditForm>
    <RzInitialValidator />
    <!-- Form inputs go here -->
</EditForm>

@code {
    [SupplyParameterFromForm]
    public Person? Person { get; set; }
}
```

Both approaches ensure that your form data is available in your Razor Component, with `<RzInitialValidator>` handling ModelState errors by transferring them to the EditForm if they exist, or by automatically validating the form if no errors are present.

## Conclusion

By upgrading your MVC controllers to inherit from `RzController` or `RzControllerWithViews`, you unlock the ability to integrate Razor Components into your application seamlessly. Rizzy automatically cascades ModelState to your views, supports both full and partial view rendering, and even allows you to combine multiple render fragments into a single composite view.

Whether you choose to pass your model explicitly using `[Parameter]` or bind it directly from the form with `[SupplyParameterFromForm]`, Rizzy adapts to your workflow. With these capabilities at your fingertips, you can build rich, interactive web applications that blend the best of both MVC and modern component-based architectures.

Happy coding!
