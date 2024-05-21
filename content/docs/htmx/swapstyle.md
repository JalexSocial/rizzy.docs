---
title: "Swapstyle"
description: ""
summary: ""
date: 2024-02-05T12:10:35-05:00
lastmod: 2024-02-05T12:10:35-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "swapstyle-62ebe8c1dcbe3a08e7cf1a03c3fff9ab"
weight: 300
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Specifies how the response will be swapped into the target element. This allows for fine-grained control over how parts of the page are updated with server responses.

### SwapStyle Options

Here are the `SwapStyle` options that define how the response is swapped into the target element on the page:

- `Default`: Uses the application's default swap style or htmx's default.
- `innerHTML`: Replace the inner HTML of the target element.
- `outerHTML`: Replace the entire target element with the response.
- `beforebegin`: Insert the response before the target element.
- `afterbegin`: Insert the response inside the target element, before its first child.
- `beforeend`: Insert the response inside the target element, after its last child.
- `afterend`: Insert the response after the target element.
- `delete`: Deletes the target element, regardless of the response.
- `none`: Does not append content from the response (though out-of-band items will still be processed).

### Using the SwapStyleBuilder

Modifiers enhance swap styles with additional behaviors, such as delays, scrolling, and dynamic targeting. The `SwapStyleBuilder` extension methods provide a fluent API to specify these behaviors. The resulting strings can be used directly within markup as well!

```html
<div hx-swap=SwapStyle.innerHTML.AfterSwapDelay(TimeSpan.FromSeconds(2))>
// hx-swap value: "innerHTML swap:2s"    
```

#### Applying a Single Modifier

```csharp
var result = SwapStyle.beforebegin.ShowWindow(ScrollDirection.top);
// result value: "beforebegin show:window:top"
```

#### Delaying the Swap

Modifies the amount of time that htmx will wait after receiving a response to swap the content by including the modifier swap:**time**. The time will be converted to milliseconds if less than 1000, otherwise seconds, meaning the resulting modifier will be swap:500ms for a TimeSpan of 500 milliseconds or swap:2s for a TimeSpan of 2 seconds.

```csharp
var result = SwapStyle.innerHTML.AfterSwapDelay(TimeSpan.FromSeconds(1));
// result value: "innerHTML swap:1s"
```

#### Delaying the Settle

Modifies the amount of time that htmx will wait between the swap and the settle logic by including the modifier settle:**time**. The time will be converted to milliseconds if less than 1000, otherwise seconds, meaning the resulting modifier will be settle:500ms for a TimeSpan of 500 milliseconds or settle:2s for a TimeSpan of 2 seconds.

```csharp
var result = SwapStyle.innerHTML.AfterSettleDelay(TimeSpan.FromSeconds(1));
// result value: "innerHTML settle:1s"
```

#### Specifying Scroll Behavior

Sets the scrollbar position after the swap. For instance, using ScrollDirection.bottom will add the modifier scroll:bottom which sets the scrollbar position to the bottom of swap content after the swap. If a CSS selector is present, then the page is scrolled to the direction of the content identified by the CSS selector.

```csharp
var result = SwapStyle.afterend.Scroll(ScrollDirection.bottom);
// result value: "afterend scroll:bottom"
```

#### Setting Scroll Position to Top

Sets the content scrollbar position to the top of the swapped content after a swap. This method adds the modifier scroll:top to the swap commands, instructing the page to scroll to the top of the content after content is swapped immediately and without animation. If a CSS selector is present, then the page is scrolled to the top of the content identified by the CSS selector.

```csharp
var result = SwapStyle.afterend.ScrollTop();
// result value: "afterend scroll:top"
```

#### Setting Scroll Position to Bottom

Sets the content scrollbar position to the bottom of the swapped content after a swap. This method adds the modifier scroll:bottom to the swap commands, instructing the page to scroll to the bottom of the content after content is swapped immediately and without animation. If a CSS selector is present, then the page is scrolled to the bottom of the content identified by the CSS selector.

```csharp
var result = SwapStyle.afterend.ScrollBottom();
// result value: "afterend scroll:bottom"
```

#### Ignoring the Document Title

Determines whether to ignore the document title in the swap response by appending the modifier ignoreTitle:**ignore**. When set to true, the document title in the swap response will be ignored by adding the modifier ignoreTitle:true. This keeps the current title unchanged regardless of the incoming swap content's title tag.

```csharp
var result = SwapStyle.afterend.IgnoreTitle(true);
// result value: "afterend ignoreTitle:true"
```

#### Including the Document Title

Ensures the title of the document is updated according to the swap response by removing any ignoreTitle modifiers, effectively setting ignoreTitle:false.

```csharp
var result = SwapStyle.afterend.IncludeTitle();
// result value: "afterend ignoreTitle:false"
```

#### Enabling Transition Effects

Enables or disables transition effects for the swap by appending the modifier transition:**show**. Controls the display of transition effects during the swap. For example, setting show to true will add the modifier transition:true to enable smooth transitions.

```csharp
var result = SwapStyle.innerHTML.Transition(true);
// result value: "innerHTML transition:true"
```

#### Including Transition Effects

Explicitly includes transition effects for the swap by adding the modifier transition:true.

```csharp
var result = SwapStyle.innerHTML.IncludeTransition();
// result value: "innerHTML transition:true"
```

#### Ignoring Transition Effects

Explicitly ignores transition effects for the swap by adding the modifier `transition:false`.

```csharp
var result = SwapStyle.innerHTML.IgnoreTransition();
// result value: "innerHTML transition:false"
```

#### Focusing and Scrolling to Content

Allows you to specify that htmx should scroll to the focused element when a request completes. htmx preserves focus between requests for inputs that have a defined id attribute. By default, htmx prevents auto-scrolling to focused inputs between requests which can be unwanted behavior on longer requests when the user has already scrolled away. When true, the modifier will be focus-scroll:true, otherwise focus-scroll:false.

```csharp
var result = SwapStyle.afterend.ScrollFocus(true);
// result value: "afterend focus-scroll:true"
```

#### Preserving Focus

Explicitly preserves focus between requests for inputs that have a defined id attribute without scrolling by adding a modifier of `focus-scroll:false`.

```csharp
var result = SwapStyle.innerHTML.PreserveFocus();
// result value: "innerHTML focus-scroll:false"
```

#### Dynamic Element Targeting

Specifies a CSS selector to target for the swap operation with a scroll direction. Adds a show modifier with the specified CSS selector and scroll direction. For example, if the CSS selector is ".item" and the direction is ScrollDirection.top, the modifier show:.item:top is added.

```csharp
var result = SwapStyle.innerHTML.ShowOn(ScrollDirection.top, ".item");
// result value: "innerHTML show:.item:top"
```

#### Showing Element at the Top

Specifies that the swap should show the element matching the CSS selector at the top of the window by adding the modifier show:{cssSelector}:top.

```csharp
var result = SwapStyle.innerHTML.ShowOnTop(".item");
// result value: "innerHTML show:.item:top"
```

#### Showing Element at the Bottom

Specifies that the swap should show the element matching the CSS selector at the bottom of the window by adding the modifier show:{cssSelector}:bottom.

```csharp
var result = SwapStyle.innerHTML.ShowOnBottom(".item");
// result value: "innerHTML show:.item:bottom"
```

#### Showing Window Scroll

Specifies that the swap should show in the window by smoothly scrolling to either the top or bottom of the window. Adds the modifier `show:window:<direction>`.

```csharp
var result = SwapStyle.innerHTML.ShowWindow(ScrollDirection.top);
// result value: "innerHTML show:window:top"
```

#### Showing Window at the Top

Specifies that the swap should smoothly scroll to the top of the window.

```csharp
var result = SwapStyle.innerHTML.ShowWindowTop();
// result value: "innerHTML show:window:top"
```

#### Showing Window at the Bottom

Specifies that the swap should smoothly scroll to the bottom of the window.

```csharp
var result = SwapStyle.innerHTML.ShowWindowBottom();
// result value: "innerHTML show:window:bottom"
```

#### Turning Off Scrolling After Swap

Turns off scrolling after swap by setting the modifier `show:none`, ensuring the page position remains unchanged after the swap.

```csharp
var result = SwapStyle.innerHTML.ShowNone();
// result value: "innerHTML show:none"
```
