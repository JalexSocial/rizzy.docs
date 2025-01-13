---
title: "RzViewContext"
description: ""
summary: ""
date: 2024-02-25T21:41:00-05:00
lastmod: 2024-02-25T21:41:00-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "viewcontext-aa3123177334cb8930d4da4611a72026"
weight: 25
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

The `RzViewContext` provides a context for views within an application. It offers access to HTTP contexts, URL helpers, component configurations, and, optionally, field mappings for form components. This context acts as a bridge between frameworks like MVC and Razor Components.

**Note:** In previous versions, it was necessary to wrap forms in a dedicated `RzEditForm` with an associated `RzFormContext`. With the update, you can now simply use the standard Blazor `EditForm` rendered server-side. Instead of managing a form context manually, just add an `hx-post="/information/update"` attribute along with the necessary `hx-target` attribute on the `EditForm`. When posting back data, decorate your form-bound properties with the `[SupplyParameterFromForm]` attribute.

## Usage

The `RzViewContext` is automatically available as the `ViewContext` property inside any `RzController` and can be easily injected into any Razor Component or other scoped services. It is also provided as a Cascaded parameter when using a Razor Component View or PartialView. This design promotes a cohesive and streamlined approach to handling views, components, and forms within the ASP.NET MVC application.

## Properties

- **Htmx**: Gets the HTMX context for the current request, enabling HTMX specific operations and interactions. See [HTMX Request](/docs/htmx/request/) and [HTMX Response](/docs/htmx/response/) documentation for more information.
- **HttpContext**: Provides access to the `Microsoft.AspNetCore.Http.HttpContext` for the current request, useful for accessing request and response information.
- **RouteData**: Gets the `AspNetCore.Routing.RouteData` for the current request, useful for retrieving route information.
- **ComponentType**: The type of the Razor component being rendered. This property is set when configuring the view and is used internally to identify the component.
- **ComponentParameters**: A dictionary containing all the parameters that are set on the component view, allowing dynamic parameter passing to Razor Components.
- **Field Mappings**: Provides methods to get or add field mappings for a given `EditContext`. Field mappings are used to store and manage form field configurations.
  - `GetOrAddFieldMapping(EditContext editContext)`: Retrieves the existing field mapping for an `EditContext` or creates one if it does not exist.
  - `RemoveFieldMapping(EditContext editContext)`: Removes the field mapping for the specified `EditContext` if it is no longer required.

```csharp {title="HomeController.cs"}
    public IResult Information()
    {
        return View<Information>();
    }

    [HttpPost, ValidateAntiForgeryToken]
    public IResult Information([FromForm] Person person)
    {
	// Do whatever you want with person

        return View<Information>();
    }
```

```csharp {title="Information.razor"}
<div id="information">

    <h3>Information</h3>

    <EditForm Model="Person" hx-post="/home/information" hx-target="#information">
        <ValidationSummary />

        <div class="form-group">
            <label for="name">Name:</label>
            <InputText id="name" class="form-control" @bind-Value="Person.Name" />
            <ValidationMessage For="@(() => Person.Name)" />
        </div>

        <button type="submit" class="btn btn-primary">Submit</button>
    </EditForm>

</div>

@code {
    [SupplyParameterFromForm]
    public Person Person { get; set; } = new();
}

```


