---
title: "Overview"
description: ""
summary: ""
date: 2024-02-09T09:25:07-05:00
lastmod: 2024-02-09T09:25:07-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "overview-c06291d1454dd0c3b1757edc0038319c"
weight: 1
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Rizzy is designed to seamlessly integrate with Htmx, offering dynamic interactions using Razor Components. To accommodate the unique aspects of working with Htmx, Rizzy introduces equivalent components for the built-in Blazor components, ensuring a smooth development experience. These Rizzy components sometimes need to implement subtle differences in behavior behind the scenes to utilize HTMX correctly.

Below is a list of Blazor built-in components alongside their Rizzy equivalents. Each Rizzy component is designed to work in a manner that is nearly identical to it's Blazor counterpart while embracing Htmx's dynamic loading and partial updates.

| Blazor | Rizzy Equivalent |
| ------------ | ------------------ |
| [AntiforgeryToken](https://learn.microsoft.com/en-us/aspnet/core/blazor/forms/?view=aspnetcore-8.0#antiforgery-support) | AntiforgeryToken |
| [AuthorizeView](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#authorizeview) | AuthorizeView |
| [CascadingValue](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#cascadingvalue-and-cascadingparameter) | CascadingValue |
| [DataAnnotationsValidator](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#dataannotationsvalidator) | RzDataAnnotationsValidator |
| [DynamicComponent](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#dynamiccomponent) | DynamicComponent |
| Editor<T> | Editor<T> |
| [EditForm](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#editform) | RzEditForm |
| [ErrorBoundary](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#errorboundary) | ErrorBoundary |
| [FocusOnNavigate](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#focusonnavigate) | N/A |
| [HeadContent](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#headcontent) | RzHeadContent |
| [HeadOutlet](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#headoutlet) | RzHeadOutlet |
| [InputCheckbox](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputcheckbox) | RzInputCheckbox |
| [InputDate](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputdate) | RzInputDate |
| [InputFile](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputfile) | RzInputFile |
| [InputNumber](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputnumber) | RzInputNumber |
| [InputRadio](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputradio-and-inputradiogroup) | RzInputRadio |
| [InputRadioGroup](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputradio-and-inputradiogroup) | RzInputRadioGroup |
| [InputSelect](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputselect) | RzInputSelect |
| [InputText](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputtext) | RzInputText |
| [InputTextArea](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#inputtextarea) | RzInputTextArea |
| [LayoutView](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#layoutview) | RzLayoutView |
| NavigationLock | N/A |
| [NavLink](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#navlink) | RzNavLink |
| [PageTitle](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#pagetitle) | RzPageTitle |
| QuickGrid | QuickGrid |
| [Router](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#router) | N/A |
| [RouteView](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#routeview) | N/A |
| SectionContent | RzSectionContent |
| SectionOutlet | RzSectionOutlet |
| [ValidationSummary](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#validationsummary) | RzValidationSummary |
| [Virtualize](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components#virtualize) | N/A |


For detailed documentation on each Blazor component, refer to the original [Blazor Microsoft documentation](https://learn.microsoft.com/en-us/aspnet/core/blazor/components/built-in-components?view=aspnetcore-8.0).
