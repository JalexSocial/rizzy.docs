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
-   **`RzInput*` Components**: (e.g., `RzInputText`, `RzInputNumber`) These components automatically generate standard HTML input elements along with `data-val-*` attributes based on the Data Annotations found on the bound model property. These attributes are essential for client-side validation libraries.
-   **`RzValidationMessage`**: Displays validation messages for a *specific* field, similar to `asp-validation-for`.
-   **`RzValidationSummary`**: Displays a summary of *all* validation messages for the form, similar to `asp-validation-summary`.
-   **`RzInitialValidator`**: A crucial component within the `EditForm`. On initial render or after a postback (like an HTMX form submission), it checks if the `ModelState` (cascaded from the `RzController`) contains errors.
    *   If `ModelState` has errors, it adds them to the `EditContext`.
    *   If `ModelState` is valid, it triggers the standard `EditContext` validation (based on Data Annotations) to ensure the form reflects the current model's validity state immediately.

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

    [Required(ErrorMessage = "You must agree to the terms.")]
    [Range(typeof(bool), "true", "true", ErrorMessage = "You must accept the terms and conditions.")]
    public bool AcceptTerms { get; set; }

    // Example of a custom validation attribute (implementation not shown here)
    // [MustBeAwesome(ErrorMessage = "Your profile description needs more awesome!")]
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
        <RzInitialValidator />

        <RzValidationSummary class="alert alert-danger" />

        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <RzInputText id="username" @bind-Value="Model.Username" class="form-control" />
            <RzValidationMessage For="@(() => Model.Username)" class="text-danger" />
        </div>

        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <RzInputText id="email" @bind-Value="Model.Email" class="form-control" type="email" />
            <RzValidationMessage For="@(() => Model.Email)" class="text-danger" />
        </div>

        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <RzInputText id="password" @bind-Value="Model.Password" class="form-control" type="password" />
            <RzValidationMessage For="@(() => Model.Password)" class="text-danger" />
        </div>

        <div class="mb-3">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <RzInputText id="confirmPassword" @bind-Value="Model.ConfirmPassword" class="form-control" type="password" />
            <RzValidationMessage For="@(() => Model.ConfirmPassword)" class="text-danger" />
        </div>

         <div class="mb-3">
            <label for="age" class="form-label">Age (Optional)</label>
            <RzInputNumber id="age" @bind-Value="Model.Age" class="form-control" />
            <RzValidationMessage For="@(() => Model.Age)" class="text-danger" />
        </div>

        <div class="mb-3 form-check">
            <RzInputCheckbox id="acceptTerms" @bind-Value="Model.AcceptTerms" class="form-check-input" />
            <label for="acceptTerms" class="form-check-label">I accept the Terms and Conditions</label>
            <RzValidationMessage For="@(() => Model.AcceptTerms)" class="text-danger d-block" /> 
            @* Use d-block for checkbox message alignment if needed *@
        </div>

        <button type="submit" class="btn btn-primary">Sign Up</button>
    </EditForm>
</div>

@code {
    // Model can be supplied via [Parameter] or [SupplyParameterFromForm]
    [SupplyParameterFromForm]
    private SignupViewModel Model { get; set; } = new();

    // Example handler for Blazor-based valid submission (optional if using pure HTMX post)
    private void HandleValidSubmit()
    {
        Console.WriteLine("Form submitted successfully within Blazor context (if OnValidSubmit is used).");
        // This might not be hit if only hx-post is used for submission
    }

    protected override void OnInitialized()
    {
       // Potential initialization logic
       base.OnInitialized();
    }
}
```

## Client-Side Validation Flow

1.  **Annotations:** You define rules on your model using Data Annotations (`[Required]`, `[StringLength]`, `[Compare]`, etc.).
2.  **Rizzy Component Rendering:** `RzInput*` components read these annotations via the `EditContext` (populated by `DataAnnotationsValidator`).
3.  **`data-val-*` Attributes:** Rizzy generates the standard `data-val="true"`, `data-val-required="Error message"`, `data-val-length-min="5"`, etc., attributes on the HTML input elements.
4.  **JavaScript Library:** A client-side JavaScript validation library (like jQuery Unobtrusive Validation, `aspnet-validation.js` included with RizzyUI, or others) is required to *interpret* these `data-val-*` attributes. This library hooks into form events (like input changes or blur) and displays/hides validation messages (`<span>` elements typically generated alongside inputs or targeted by `RzValidationMessage`) *without* a server roundtrip.
5.  **`RzValidationMessage` / `RzValidationSummary`:** These components render the necessary HTML elements (usually `<span>` or `<div>`) that client-side libraries use to display the error messages defined in your annotations or added dynamically.

## Server-Side Validation Flow (HTMX Post)

1.  **HTMX Submission:** The user submits the form using an element with `hx-post` (or similar).
2.  **Controller Action:** Your MVC controller action receives the submitted model. ASP.NET Core performs model binding and validates the model against the Data Annotations, populating `ModelState`.
3.  **`ModelState` Check:** Your controller action checks `ModelState.IsValid`.
4.  **Invalid `ModelState`:**
    *   The controller returns a Rizzy `PartialView<YourFormComponent>()` (or `View`).
    *   Rizzy cascades the `ModelState` dictionary down to the component.
    *   Inside the `EditForm`, `RzInitialValidator` detects the `ModelState` errors and adds them to the `EditContext`.
    *   `RzValidationMessage` and `RzValidationSummary` render the errors from the `EditContext`.
    *   The rendered partial HTML (including inputs potentially marked with error classes and the visible validation messages) is returned to HTMX to be swapped into the page.
5.  **Valid `ModelState`:** The controller processes the data and typically returns a different response (e.g., a redirect, a success message partial, etc.).

This combination ensures immediate feedback via client-side validation (if configured with a JS library) and guarantees data integrity through server-side validation, leveraging Rizzy components to bridge the gap.
