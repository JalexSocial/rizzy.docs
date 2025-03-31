---
title: "Overview"
description: "An overview of Rizzy components and their Blazor counterparts, explaining why specialized versions are sometimes needed."
summary: "Learn about the Rizzy component library, how it maps to standard Blazor components, and why `Rz*` versions exist, particularly for HTMX integration and enhanced form validation."
date: 2024-02-09T09:25:07-05:00
lastmod: 2024-07-27T10:30:00-05:00 # Updated timestamp
draft: false
menu:
  docs:
    parent: "" # Assuming this belongs at the top level of components
    identifier: "overview-c06291d1454dd0c3b1757edc0038319c" # Keep original identifier if needed
weight: 1 # Keep as first item in Components section
toc: true
seo:
  title: "Rizzy Component Overview" # Custom title
  description: "Explore Rizzy's component library, understand its relationship with Blazor components, and learn the reasons for the `Rz` prefixed variants, including HTMX compatibility and client-side validation." # Custom description
  canonical: "" # Optional
  noindex: false # Default
---

Rizzy is designed to seamlessly integrate server-rendered Blazor components with the dynamic capabilities of HTMX. It achieves this by providing equivalent components for many of Blazor's built-in ones. These Rizzy-specific components, often prefixed with `Rz`, sometimes implement subtle differences behind the scenes to function correctly within an HTMX-driven workflow, which relies on standard HTTP requests and HTML fragments rather than Blazor's typical SignalR or WebAssembly interactivity models.

**Why the `Rz*` Components?** They make standard Blazor components compatible with HTMX and common web techniques. For example, the `RzInput*` components add the standard `data-val-*` attributes needed for client-side validation libraries familiar to Asp.net MVC users, based on your model's Data Annotations. This provides instant validation feedback alongside HTMX updates. Other `Rz` components handle specific HTMX integration points, like ensuring `RzPageTitle` updates correctly after swaps, or ensuring Blazor sections (`RzSection*`) work within Rizzy.

Below is a list of Blazor built-in components alongside their Rizzy equivalents or how they are typically used within Rizzy. Each Rizzy component aims to provide a developer experience nearly identical to its Blazor counterpart while embracing HTMX's dynamic loading and partial updates.

| Blazor Component             | Rizzy Equivalent / Usage                                    | Notes                                                                 |
| :--------------------------- | :---------------------------------------------------------- | :-------------------------------------------------------------------- |
| `AntiforgeryToken`           | `AntiforgeryToken`                                          | Used directly; Rizzy manages token generation via config/middleware.  |
| `AuthorizeView`              | `AuthorizeView`                                             | Authorization should be implemented at the controller level.          |
| `CascadingValue<TValue>`     | `CascadingValue<TValue>`                                    | Used directly.                                                        |
| `DataAnnotationsValidator` | `DataAnnotationsValidator`                                | Used directly within `EditForm`.                                      |
| `DynamicComponent`           | `DynamicComponent`                                          | Used directly (e.g., internally by `RzPage`/`RzPartial`).           |
| `Editor<T>`                  | `Editor<T>`                                                 | Used directly.                                                        |
| `EditForm`                   | `EditForm`                                                  | Used directly; often paired with `RzInitialValidator`.                |
| `ErrorBoundary`              | `ErrorBoundary`                                             | Used directly.                                                        |
| `FocusOnNavigate`            | N/A                                                         | HTMX manages focus/scrolling differently post-swap.                   |
| `HeadContent`                | `RzHeadContent`                                             | Ensures head content updates work with HTMX partials.                 |
| `HeadOutlet`                 | `RzHeadOutlet`                                              | Renders content from `RzHeadContent` and `RzPageTitle`.               |
| `InputCheckbox`              | `RzInputCheckbox`                                           | Adds `data-val-*` attributes, ID handling.                            |
| `InputDate<TValue>`          | `RzInputDate<TValue>`                                       | Adds `data-val-*` attributes, ID handling.                            |
| `InputFile`                  | `RzInputFile`                                               | Standard component, ID handling.                                      |
| `InputNumber<TValue>`        | `RzInputNumber<TValue>`                                     | Adds `data-val-*` attributes, ID handling.                            |
| `InputRadio<TValue>`         | `RzInputRadio<TValue>`                                      | Standard component, ID handling (validation often on group).          |
| `InputRadioGroup<TValue>`    | `RzInputRadioGroup<TValue>`                                 | Adds `data-val-*` attributes, ID handling for the group.              |
| `InputSelect<TValue>`        | `RzInputSelect<TValue>`                                     | Adds `data-val-*` attributes, ID handling.                            |
| `InputText`                  | `RzInputText`                                               | Adds `data-val-*` attributes, ID handling.                            |
| `InputTextArea`              | `RzInputTextArea`                                           | Adds `data-val-*` attributes, ID handling.                            |
| `NavigationLock`             | N/A                                                         | HTMX handles navigation state differently.                            |
| `NavLink`                    | `NavLink`                                                   | Used directly; often combined with `hx-boost` for HTMX navigation.    |
| `PageTitle`                  | `RzPageTitle`                                               | Handles title updates correctly during HTMX swaps.                    |
| `Router`                     | N/A                                                         | Routing handled by ASP.NET Core (MVC/Minimal API).                    |
| `RouteView`                  | N/A                                                         | Routing handled by ASP.NET Core.                                      |
| `SectionContent`             | `RzSectionContent`                                          | Ensures section content integrates with Rizzy's rendering.            |
| `SectionOutlet`              | `RzSectionOutlet`                                           | Ensures section outlets integrate with Rizzy's rendering.             |
| `ValidationSummary`          | `RzValidationSummary`                                       | Displays summary compatible with standard client-side validation.     |
| `Virtualize<TItem>`          | N/A                                                         | Virtualization typically relies on Blazor's interactive runtimes.     |

For detailed documentation on the standard Blazor components, refer to the official [Blazor Microsoft documentation](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components?view=aspnetcore-8.0). Rizzy's components aim to align closely with these while enabling HTMX integration.