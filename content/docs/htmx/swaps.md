---
title: "Out of Band Swapping"
description: ""
summary: ""
date: 2024-02-07T11:42:24-05:00
lastmod: 2024-02-07T11:42:24-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "swaps-086a15288eb2dfe181e188ca652740e2"
weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Out of band swaps in HTMX allow you to update content in the Document Object Model (DOM) outside the direct target of an operation. This feature enables you to make updates to multiple elements in response to a single event, facilitating more dynamic and interactive web applications by piggybacking updates across different parts of your page.

{{< callout context="note" title="Note" icon="info-circle" >}}
The HtmxSwappable component and HtmxSwapService were based on HTMX usage of Out of Band swaps.  You can find more information about HTMX out of band swaps on the official [Htmx documentation site](https://htmx.org/attributes/hx-swap-oob/).
{{< /callout >}}

## Using the HtmxSwappable Component

The `HtmxSwappable` component is designed for seamlessly integrating out of band swaps in your Blazor applications. Htmx allows for this component to be used anywhere on the page that you like. Please note that when using this component it does not publish itself to the `HtmxSwapService`, but will still work as expected.

Parameters:
- `TargetId`: Specifies the HTML ID of the element to be swapped. This should be an element already present on the page.
- `SwapStyle`: (optional) Defines the method used for swapping in the new content. It defaults to `SwapStyle.OuterHTML`. For further documentation on `SwapStyle`, visit [SwapStyle Options](/rizzy.docs/docs/htmx/response/#swapstyle-options).
- `Selector`: (optional) A valid CSS selector targeting the element(s) within `TargetId` where the swap should occur.

Here's a simple example that demonstrates how to use `HtmxSwappable` to display a Bootstrap alert message.

```html
<HtmxSwappable TargetId="alert-container" SwapStyle="SwapStyle.InnerHTML" Selector=".alert-message">
    <div class="alert alert-info" role="alert">
        This is an important message!
    </div>
</HtmxSwappable>
```

The example provided uses the `HtmxSwappable` component to perform an out of band swap into an existing HTML structure. Let's break down what the original HTML might look like before the swap occurs and the role of the `.alert-message` CSS selector within this process.

### Original HTML Structure

Before the swap, the HTML structure should contain an element with an ID matching the `TargetId` specified in the `HtmxSwappable` component. This element serves as the container where the new content will be swapped in. Additionally, within this container, there might be an existing element identified by the `.alert-message` CSS selector that the swap operation targets.

Here's an example of what the original HTML structure might look like that you can place in your Layout page:

```html
<div id="alert-container">
    <div class="alert-message">
        Original alert message here.
    </div>
    <!-- Other elements can also exist here -->
</div>
```

In this structure:
- The `div` with the ID `alert-container` is the container targeted by `HtmxSwappable` for content swapping.
- Inside this container, there's a `div` with the class `.alert-message`, which is the specific target for the content defined within the `HtmxSwappable` component, based on the `Selector` property.

### Role of `.alert-message`

The `.alert-message` CSS selector plays a crucial role in precisely targeting where within the `alert-container` the new content should be inserted or replaced. When the swap occurs:
- If the `SwapStyle` is set to `SwapStyle.InnerHTML`, the inner HTML of the `.alert-message` element is replaced with the new content defined within the `HtmxSwappable` component.
- The presence of the `.alert-message` selector allows for more granular control over which part of the `alert-container` gets updated, enabling scenarios where you might want to update only a specific message within a larger container without affecting other content.

### After the Swap

After the swap operation completes, the HTML might look like this:

```html
<div id="alert-container">
    <div class="alert-message">
        <div class="alert alert-info" role="alert">
            This is an important message!
        </div>
    </div>
</div>
```

Here, the original content within the `.alert-message` div is replaced with the new alert message defined in the `HtmxSwappable` component. This demonstrates how out of band swaps enable updating specific portions of the page in response to certain events, enhancing interactivity of web applications without requiring a full page reload or direct interaction with the targeted container element.

## Using the HtmxSwapService

`HtmxSwapService` is a service registered as a scoped dependency implementing `IHtmxSwapService`. It facilitates injecting Razor Components, RenderFragments, and raw HTML content into various parts of your application or services.

This service is useful because it provides an ability to inject content into the page from *anywhere*.  This opens up the door for the creation of services that can create content that is swapped into place that exist outside of your razor component views.

## Features

- **Dynamic Content Swapping:** Easily swap content in your application with Razor components, RenderFragments, or raw HTML during HTMX requests.
- **Customizable Swap Styles:** Offers various content swap styles to choose from, allowing for flexible content rendering based on your needs.
- **Selector Support:** Utilize CSS selectors to precisely define where the content swap should occur within the DOM.
- **Support for Raw HTML:** Directly inject raw HTML into your application

### Adding Content with HtmxSwapService

{{< callout context="caution" title="Caution" icon="alert-triangle" >}}
You must include the `HtmxSwapContent` component somewhere in your template for swappable content to render correctly.
{{< /callout >}}

To render the content managed by `HtmxSwapService`, include an `HtmxSwapContent` component where you want the dynamic content to appear:

```html
<HtmxSwapContent/>
```

Here's how you can use `HtmxSwapService` in your components to perform dynamic content swaps:

```csharp
@inject IHtmxSwapService HtmxSwapService

@code {
    protected override void OnInitialized()
    {
        HtmxSwapService.AddRawContent("<p>Hello, world!</p>");
        HtmxSwapService.AddSwappableComponent<AlertComponent>("alert-container", new Dictionary<string, object>
        {
            {"Message", "This is an important message!"}
        }), SwapStyle.InnerHTML, ".alert-message", ;
    }
}
```

In this example, `AddRawContent` is used to add simple HTML content to the SectionOutlet, while `AddSwappableComponent` dynamically adds a Razor component (`AlertComponent`) that could represent a Bootstrap alert message. The `AlertComponent` is expected to accept a parameter named "Message".

#### Adding a Swappable Razor Component

```csharp
@inject IHtmxSwapService HtmxSwapService

HtmxSwapService.AddSwappableComponent<MyComponent>(
    targetId: "targetElementId",
    parameters: new Dictionary<string, object> { { "ParameterName", "Value" } },
    swapStyle: SwapStyle.OuterHTML,
    selector: ".css-selector"
);
```

#### Adding a RenderFragment

```csharp
HtmxSwapService.AddSwappableFragment(
    targetId: "targetElementId",
    renderFragment: builder => builder.AddContent(0, "Dynamic content here"),
    swapStyle: SwapStyle.OuterHTML,
    selector: ".css-selector"
);
```

#### Adding Raw HTML Content

```csharp
HtmxSwapService.AddRawContent(
    "<div>Raw HTML content</div>"
);
```

#### Rendering Added Content

As an alternate way to render all added content, you can also simply invoke the `RenderToFragment` method:

```csharp
RenderFragment contentFragment = HtmxSwapService.RenderToFragment();
```


Typically you would add this to the very end of your template just before the closing body tag.

This approach allows for a flexible way to manage and update your application's UI dynamically.