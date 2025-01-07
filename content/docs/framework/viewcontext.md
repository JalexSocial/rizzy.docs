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

The `RzViewContext` provides a context for views within an application. It offers access to HTTP contexts, URL helpers, component configurations, and form contexts, enhancing the capability to render Razor Components and manage form interactions seamlessly. This context acts as a bridge between frameworks like MVC and Razor Components.

## Usage

The `RzViewContext` is automatically available as the `ViewContext` property inside any `RzController` and can be easily injected into any Razor Component or other scoped services. It is also provided as a Cascaded parameter when using a Razor Component View or PartialView. This design promotes a cohesive and streamlined approach to handling views, components, and forms within the ASP.NET MVC application.

## Properties

- **Htmx**: Gets the HTMX context for the current request, enabling HTMX specific operations and interactions within the application. See [HTMX Request](/docs/htmx/request/) and [HTMX Response](/docs/htmx/response/) documentation for more information.
- **HttpContext**: Provides access to the `Microsoft.AspNetCore.Http.HttpContext` for the current request, useful for accessing request and response information.
- **RouteData**: Gets the `AspNetCore.Routing.RouteData` for the current request, useful for retrieving route information.
- **ComponentType**: The type of the Razor component being rendered. This property is set when configuring the view and is used internally to identify the component.
- **ComponentParameters**: A dictionary containing all the parameters that are set on the component view, allowing dynamic parameter passing to Razor Components.

## Methods

- **AddFormContext**: Overloaded methods to add a form context with specified names, actions, models, and optional use of data annotations for validation. These methods facilitate form handling, validation, and context management within Razor Components or MVC views.
    - **AddFormContext(string id, string formName, string formAction, object model, bool useDataAnnotations = true)**: Adds a form context with a unique HTML ID, name, action, and model. Uses data annotations for validation by default.
    - **AddFormContext(string formName, object model, bool useDataAnnotations = true)**: Simplified method to add a form context without specifying an HTML ID or form action.
    - **AddFormContext(string formName, string formAction, object model, bool useDataAnnotations = true)**: Adds a form context with a form name, action, and model, allowing for a concise form setup.
- **TryGetFormContext(string formName, out RzFormContext context)**: Attempts to retrieve a form context by name. Returns true if found; otherwise, false. This method is essential for accessing specific form contexts for further operations or validations.

```csharp {title="HomeController.cs"}
    public IResult Information()
    {
        ViewContext.AddFormContext("myForm", CurrentActionUrl, new Person());

        return View<Information>();
    }

    [HttpPost, ValidateAntiForgeryToken]
    public IResult Information([FromForm] Person person)
    {
        var ctx = ViewContext.AddFormContext("myForm", CurrentActionUrl, person);
        ctx.EditContext.Validate();

        return View<Information>();
    }
```

```csharp {title="Information.razor"}
<div id="information">

	<h3>Information</h3>

	<RzEditForm FormContext="_formContext" hx-post="@_formContext?.FormUrl" hx-target="#information">
		<RzValidationSummary/>

		<div class="form-group">
			<label for="name">Name:</label>
			<RzInputText id="name" class="form-control" @bind-Value="Person.Name"/>
			<RzValidationMessage For="@(() => Person.Name)"/>
		</div>

		<button type="submit" class="btn btn-primary">Submit</button>
	</RzEditForm>

</div>

@code {
    private RzFormContext? _formContext;

    [Inject] public RzViewContext ViewContext { get; set; } = default!;

    public Person Person { get; set; } = new();

    protected override void OnInitialized()
    {
        if (ViewContext.TryGetFormContext("myForm", out _formContext))
        {
            Person = _formContext.Model<Person>();
        }
    }
}
```


