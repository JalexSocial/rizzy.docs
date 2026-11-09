
---
title: "Validation"
description: "Learn how to implement form validation using Rizzy components, data annotations, and server-side ModelState."
summary: "Leverage Data Annotations and Rizzy components for seamless client-side and server-side form validation."
date: 2024-03-06T07:25:10-05:00 # Adjust date as needed
lastmod: 2024-07-26T10:00:00-05:00 # Adjust date as needed
draft: false
weight: 200
toc: true
seo:
  title: "Form Validation with Rizzy"
  description: "Implement robust client-side and server-side form validation in Rizzy using Data Annotations, validation components, and ModelState integration."
  canonical: "" 
  noindex: false 
---

Rizzy aims to provide a familiar validation experience, similar to traditional ASP.NET Core MVC or Razor Pages, by leveraging Data Annotations and integrating seamlessly with Blazor's `EditContext`. This allows for both client-side feedback (when paired with a suitable JS library) and robust server-side validation.

## Key Validation Components

-   **`EditForm`**: The container for your form inputs. Rizzy often uses this in conjunction with HTMX attributes for submissions (e.g., `hx-post`).
-   **`DataAnnotationsValidator`**: Attaches validation support based on Data Annotation attributes (`[Required]`, `[StringLength]`, etc.) on your model to the `EditForm`'s `EditContext`.
-   **`RzInput*Base` Components**: (e.g., `RzInputTextBase`, `RzInputNumberBase`) These components automatically generate standard HTML input elements along with `data-val-*` attributes based on the Data Annotations found on the bound model property. These attributes are essential for client-side validation libraries.
-   **`RzValidationMessageBase`**: Displays validation messages for a *specific* field, similar to `asp-validation-for`.
-   **`RzValidationSummaryBase`**: Displays a summary of *all* validation messages for the form, similar to `asp-validation-summary`.
-   **`RzModelStateProvider`**: Place it inside the `EditForm` to show **server-side** errors. It copies the errors from the cascaded `ModelStateDictionary` into the `EditContext`, so each error appears next to its field. Keys from MVC model binding (`Person.Name`, `Person.Address.City`) are mapped to the right field. `RzController` passes the controller's `ModelState` automatically; with `IRizzyService` (minimal APIs), pass one to `View`/`PartialView`.
-   **`RzInitialValidator`**: Optional. Runs the form's Data Annotations validation when the form renders, so the form shows its current validity immediately (for example when re-rendering a posted model).

## Complex Validation Example

Let's illustrate with a model containing various validation rules and the corresponding Razor component form.

### Example Model (`SignupViewModel.cs`)

```csharp
using System.ComponentModel.DataAnnotations;

public class SignupViewModel
{
    [Required(ErrorMessage = "Username is required.")]
    [StringLength(20, MinimumLength = 5, ErrorMessage = "Username must be between 5 and 20 characters.")]
    [RegularExpression("^[a-zA-Z0-9_]*$", ErrorMessage = "Username can only contain letters, numbers, and underscores.")]
    public string? Username { get; set; }

    [Required(ErrorMessage = "Email is required.")]
    [EmailAddress(ErrorMessage = "Please enter a valid email address.")]
    public string? Email { get; set; }

    [Required(ErrorMessage = "Password is required.")]
    [DataType(DataType.Password)]
    [StringLength(100, MinimumLength = 8, ErrorMessage = "Password must be at least 8 characters long.")]
    public string? Password { get; set; }

    [Required(ErrorMessage = "Please confirm your password.")]
    [DataType(DataType.Password)]
    [Compare(nameof(Password), ErrorMessage = "Passwords do not match.")]
    public string? ConfirmPassword { get; set; }

    [Range(18, 120, ErrorMessage = "You must be between 18 and 120 years old.")]
    public int? Age { get; set; } // Optional field with Range validation

    [Range(typeof(bool), "true", "true", ErrorMessage = "You must accept the terms and conditions.")]
    public bool AcceptTerms { get; set; }

    // Example of a custom validation attribute (implementation not shown here)
    //[MustBeAwesome(ErrorMessage = "Your profile description needs more awesome!")]
    // public string ProfileDescription { get; set; }
}
```

### Razor Component Form (`SignupForm.razor`)

```razor
@using System.ComponentModel.DataAnnotations
@using Rizzy; // Assuming Rizzy components are imported

<div id="signup-form-container">
    <h3>Sign Up</h3>

    <EditForm Model="Model" FormName="Signup" OnValidSubmit="HandleValidSubmit" hx-post="/signup/submit" hx-target="#signup-form-container" hx-swap="outerHTML">
        <DataAnnotationsValidator />
        <RzModelStateProvider />

        <RzValidationSummaryBase class="alert alert-danger" />

        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <RzInputTextBase id="username" @bind-Value="Model.Username" class="form-control" />
            <RzValidationMessageBase For="@(() => Model.Username)" class="text-danger" />
        </div>

        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <RzInputTextBase id="email" @bind-Value="Model.Email" class="form-control" type="email" />
            <RzValidationMessageBase For="@(() => Model.Email)" class="text-danger" />
        </div>

        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <RzInputTextBase id="password" @bind-Value="Model.Password" class="form-control" type="password" />
            <RzValidationMessageBase For="@(() => Model.Password)" class="text-danger" />
        </div>

        <div class="mb-3">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <RzInputTextBase id="confirmPassword" @bind-Value="Model.ConfirmPassword" class="form-control" type="password" />
            <RzValidationMessageBase For="@(() => Model.ConfirmPassword)" class="text-danger" />
        </div>

         <div class="mb-3">
            <label for="age" class="form-label">Age (Optional)</label>
            <RzInputNumberBase id="age" @bind-Value="Model.Age" class="form-control" />
            <RzValidationMessageBase For="@(() => Model.Age)" class="text-danger" />
        </div>

        <div class="mb-3 form-check">
            <RzInputCheckboxBase id="acceptTerms" @bind-Value="Model.AcceptTerms" class="form-check-input" />
            <label for="acceptTerms" class="form-check-label">I accept the Terms and Conditions</label>
            <RzValidationMessageBase For="@(() => Model.AcceptTerms)" class="text-danger d-block" /> 
            @* Use d-block for checkbox message alignment if needed *@
        </div>

        <button type="submit" class="btn btn-primary">Sign Up</button>
    </EditForm>
</div>

@code {
    // Model can be supplied via [Parameter] or [SupplyParameterFromForm]. Don't give a
    // [SupplyParameterFromForm] property an initializer (it can be overwritten with null during
    // posts, warning BL0008); create the model in OnInitialized instead.
    [SupplyParameterFromForm(FormName = "Signup")]
    public SignupViewModel? Model { get; set; }

    // Example handler for Blazor-based valid submission (optional if using pure HTMX post)
    private void HandleValidSubmit()
    {
        Console.WriteLine("Form submitted successfully within Blazor context (if OnValidSubmit is used).");
        // This might not be hit if only hx-post is used for submission
    }

    protected override void OnInitialized() => Model ??= new();
}
```

## Client-Side Validation Flow

1.  **Annotations:** You define rules on your model using Data Annotations (`[Required]`, `[StringLength]`, `[Compare]`, etc.).
2.  **Rizzy Component Rendering:** `RzInput*Base` components read these annotations via the `EditContext` (populated by `DataAnnotationsValidator`).
3.  **`data-val-*` Attributes:** Rizzy generates the standard `data-val="true"`, `data-val-required="Error message"`, `data-val-length-min="5"`, etc., attributes on the HTML input elements.
4.  **JavaScript Library:** A client-side JavaScript validation library (like jQuery Unobtrusive Validation, the `aspnet-validation` script that RizzyUI includes, or others; the Rizzy client script does not validate) is required to *interpret* these `data-val-*` attributes. This library hooks into form events (like input changes or blur) and displays/hides validation messages (`<span>` elements typically generated alongside inputs or targeted by `RzValidationMessageBase`) *without* a server roundtrip.
5.  **`RzValidationMessageBase` / `RzValidationSummaryBase`:** These components render the necessary HTML elements (usually `<span>` or `<div>`) that client-side libraries use to display the error messages defined in your annotations or added dynamically.

## Server-Side Validation Flow (HTMX Post)

1.  **HTMX submission:** the user submits the form through `hx-post` (or similar). rizzy.js adds the antiforgery token.
2.  **Model binding:** your controller action receives the model. ASP.NET Core binds and validates it against the Data Annotations and fills `ModelState`. Blazor names the inputs after the bound expression (`Model.Username`), so name the action parameter to match (`model`), or use `[FromForm(Name = "Model")]`. Add your own rules with `ModelState.AddModelError("Model.Username", "That name is taken.")`; keys with the binding prefix are mapped to the field.
3.  **Invalid:** mark the response as a validation failure and re-render the form:

    ```csharp {title="SignupController.cs"}
    public class SignupController : RzController
    {
        [HttpPost, ValidateAntiForgeryToken]
        public IResult Submit([FromForm] SignupViewModel model)
        {
            if (!ModelState.IsValid)
            {
                Response.Htmx().ValidationFailed();   // status 422
                return View<SignupForm>();            // ModelState is passed automatically
            }

            // Save...
            return PartialView<SignupComplete>();
        }
    }
    ```

    htmx 4 swaps 4xx responses like any other, so the re-rendered form (with its errors) replaces the old one. `<RzModelStateProvider />` shows each error next to its field and in the summary. To send the errors somewhere else, pass a selector (`ValidationFailed("#errors")`) or route it from the page with `hx-status:422="target:#errors"`.
4.  **Valid:** process the data and return a different response (a success fragment, `Response.Htmx().Redirect(...)`, and so on).

{{< callout context="note" title="MVC antiforgery" icon="info-circle" >}}
`[ValidateAntiForgeryToken]` needs MVC registered with `AddControllersWithViews()` (or `AddMvcCore().AddViews()`); `AddControllers()` alone does not provide its filter.
{{< /callout >}}

This combination gives immediate feedback via client-side validation (if you add a JS library) and guarantees data integrity through server-side validation.
