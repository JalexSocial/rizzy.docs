---
title: "Overview"
description: ""
summary: ""
date: 2024-02-05T12:12:06-05:00
lastmod: 2024-02-05T12:12:06-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "overview-c04dc965d8ce34d7059c0711330d112b"
weight: 25
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Rizzy has reimplemented many of the built-in default Blazor components for Forms. This allows the library to take advantage of some of the subtle differences between components that are interactive via Blazor and those who are interactive because of a combination of HTMX and client-side components. The component library here is very bare-bones and can serve as the basis for a styled set of components.

## Rizzy Form Components

Rizzy provides built-in input components to receive and validate user input. The built-in input components in the following table are supported in an RzEditForm with an RzFormContext.

The components in the table are also supported outside of a form in Razor component markup. Inputs are validated when they're changed and when a form is submitted.



| Blazor | Rizzy Equivalent |
| ------------ | ------------------ |
| [AntiforgeryToken](https://learn.microsoft.com/en-us/aspnet/core/blazor/forms/?view=aspnetcore-8.0#antiforgery-support) | AntiforgeryToken |
| [DataAnnotationsValidator](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#dataannotationsvalidator) | DataAnnotationsValidator |
| [EditForm](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#editform) | RzEditForm |
| [InputCheckbox](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputcheckbox) | RzInputCheckbox |
| [InputDate](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputdate) | RzInputDate |
| [InputFile](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputfile) | RzInputFile |
| [InputNumber](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputnumber) | RzInputNumber |
| [InputRadio](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputradio-and-inputradiogroup) | RzInputRadio |
| [InputRadioGroup](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputradio-and-inputradiogroup) | RzInputRadioGroup |
| [InputSelect](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputselect) | RzInputSelect |
| [InputText](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputtext) | RzInputText |
| [InputTextArea](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputtextarea) | RzInputTextArea |
| [ValidationSummary](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#validationsummary) | RzValidationSummary |

All of the input components, including RzEditForm, support arbitrary attributes. Any attribute that doesn't match a component parameter is added to the rendered HTML element.

Input components provide default behavior for validating when a field is changed:

- For input components in a form with an EditContext, the default validation behavior includes updating the field CSS class to reflect the field's state as valid or invalid with validation styling of the underlying HTML element. This is done through the use of client-side data annotations.

## Example Form

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