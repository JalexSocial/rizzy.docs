---
title: "Triggers"
description: ""
summary: ""
date: 2024-02-05T12:10:35-05:00
lastmod: 2024-02-05T12:10:35-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "triggers-62ebe8c1dcbe3a08e7cf1a03c3fff9ab"
weight: 302
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## HTMX Triggers

HTMX triggers are used to specify when an HTMX request should be initiated. Common use cases include triggering requests on events such as clicks, page load, element visibility, and custom-defined events.

The `Trigger` class in the HTMX Trigger Builder library provides a fluent API to specify various triggers for HTMX requests. This API simplifies the construction of HTMX triggers by offering a range of methods to define event-based, server-sent, and custom triggers, as well as modifiers to control their behavior.

## Creating Triggers with the `Trigger` Class

You can create triggers using the static methods provided by the `Trigger` class. Each method returns a `TriggerModifierBuilder` instance, allowing further configuration of the trigger.

### OnEvent

Specifies a standard event as the trigger by setting the event name. This method builds a JavaScript event trigger. For example, specifying "click" will trigger the request on a click event.

**Parameters:**
- `eventName` (string): The name of the standard event (e.g., "click").

```html
<div hx-get="/clicked" hx-trigger=@Trigger.OnEvent("click")>Click Me</div>
// Resulting hx-trigger: <div hx-get="/clicked" hx-trigger="click">Click Me</div>
```

### Sse

Specifies a Server-Sent Event (SSE) as the trigger by setting the event name and SSE event. This method sets the SSE trigger for an AJAX request. For example, specifying "message" will trigger the request on the message event.

**Parameters:**
- `sseEventName` (string): The name of the SSE event.

```html
<div hx-get="/updates" hx-trigger=@Trigger.Sse("message")>Update Me</div>
// Resulting hx-trigger: <div hx-get="/updates" hx-trigger="sse:message">Update Me</div>
```

### Load

Specifies that the trigger occurs on page load. This method sets the load event trigger, useful for lazy-loading content.

```html
<div hx-get="/load" hx-trigger=@Trigger.Load()>Load Me</div>
// Resulting hx-trigger: <div hx-get="/load" hx-trigger="load">Load Me</div>
```

### Revealed

Specifies that the trigger occurs when an element is scrolled into the viewport. This method sets the revealed event trigger for an AJAX request, useful for lazy-loading content as it enters the viewport.

```html
<div hx-get="/load" hx-trigger=@Trigger.Revealed()>Reveal Me</div>
// Resulting hx-trigger: <div hx-get="/load" hx-trigger="revealed">Reveal Me</div>
```

### Intersect

Specifies that the trigger occurs when an element intersects the viewport. This method sets the intersect event trigger for an AJAX request, which fires when the element first intersects the viewport. Additional options include `root` and `threshold`.

**Parameters:**
- `root` (string, optional): The CSS selector of the root element for intersection.
- `threshold` (float, optional): A floating point number between 0.0 and 1.0 indicating what amount of intersection to fire the event on.

```html
<div hx-get="/load" hx-trigger=@Trigger.Intersect(root: ".container", threshold: 0.5f)>Intersect Me</div>
// Resulting hx-trigger: <div hx-get="/load" hx-trigger="intersect root:.container threshold:0.5">Intersect Me</div>
```

### Every

Specifies that the trigger occurs at regular intervals. This method sets the polling interval for an AJAX request. For example, specifying an interval of 1 second will trigger the request every second.

**Parameters:**
- `interval` (TimeSpan): The interval at which to poll.

```html
<div hx-get="/updates" hx-trigger=@Trigger.Every(TimeSpan.FromSeconds(5))>Update Every 5s</div>
// Resulting hx-trigger: <div hx-get="/updates" hx-trigger="every 5s">Update Every 5s</div>
```

### Custom

Specifies a custom trigger that will be included without changes. This method sets a custom trigger definition.

**Parameters:**
- `triggerDefinition` (string): The custom trigger definition string.

```html
<div hx-get="/custom" hx-trigger=@Trigger.Custom("custom-event delay:2s")>Custom Event</div>
// Resulting hx-trigger: <div hx-get="/custom" hx-trigger="custom-event delay:2s">Custom Event</div>
```

## Modifiers

After creating a trigger, you can use the `TriggerModifierBuilder` to add various modifiers to the trigger. The available modifiers are:

### WithCondition

Adds a condition to the trigger by setting an event filter. This method adds a JavaScript expression as a condition for the event to be triggered.

**Parameters:**
- `condition` (string): The JavaScript expression to evaluate.

```html
<div hx-get="/clicked" hx-trigger=@Trigger.OnEvent("click").WithCondition("ctrlKey")>Control Click Me</div>
// Resulting hx-trigger: <div hx-get="/clicked" hx-trigger="click[ctrlKey]">Control Click Me</div>
```

### Once

Specifies that the event should trigger only once. This method adds the "once" modifier to the trigger, making it fire only the first time the event occurs.

```html
<div hx-get="/clicked" hx-trigger=@Trigger.OnEvent("click").Once()>Click Me Once</div>
// Resulting hx-trigger: <div hx-get="/clicked" hx-trigger="click once">Click Me Once</div>
```

### Changed

Specifies that the event should trigger only when the value changes. This method adds the "changed" modifier to the trigger, making it fire only when the value of the element has changed.

```html
<input hx-get="/search" hx-trigger=@Trigger.OnEvent("keyup").Changed().Delay(TimeSpan.FromSeconds(1))>
// Resulting hx-trigger: <input hx-get="/search" hx-trigger="keyup changed delay:1s"/>
```

### Delay

Adds a delay before the event triggers the request by adding the "delay" modifier. This method adds a delay to the trigger, resetting the delay if the event occurs again before the delay completes.

**Parameters:**
- `timing` (TimeSpan): The delay time.

```html
<div hx-get="/search" hx-trigger=@Trigger.OnEvent("keyup").Delay(TimeSpan.FromSeconds(1))>Search Me</div>
// Resulting hx-trigger: <div hx-get="/search" hx-trigger="keyup delay:1s">Search Me</div>
```

### Throttle

Adds a throttle after the event triggers the request by adding the "throttle" modifier. This method adds a throttle to the trigger, ignoring subsequent events until the throttle period completes.

**Parameters:**
- `timing` (TimeSpan): The throttle time.

```html
<div hx-get="/updates" hx-trigger=@Trigger.OnEvent("click").Throttle(TimeSpan.FromSeconds(2))>Click Me</div>
// Resulting hx-trigger: <div hx-get="/updates" hx-trigger="click throttle:2s">Click Me</div>
```

### From

Specifies that the event should trigger from another element by adding the "from" modifier. This method allows listening to events on a different element specified by the extended CSS selector.

**Parameters:**
- `extendedCssSelector` (string): The extended CSS selector of the element to listen for events from.

```html
<div hx-get="/hotkeys" hx-trigger=@Trigger.OnEvent("keydown").From("document")>Listen on Document</div>
// Resulting hx-trigger: <div hx-get="/hotkeys" hx-trigger="keydown from:document">Listen on Document</div>
```

### Target

Filters the event trigger to a specific target element by adding the "target" modifier. This method allows the event trigger to be filtered to a target element specified by the CSS selector.

**Parameters:**
- `cssSelector` (string): The CSS selector of the target element.

```html
<div hx-get="/dynamic" hx-trigger=@Trigger.OnEvent("click").Target(".child")>Click Child</div>
// Resulting hx-trigger: <div hx-get="/dynamic" hx-trigger="click target:.child">Click Child</div>
```

### Consume

Specifies that the event should not trigger any other HTMX requests on parent elements by adding the "consume" modifier. This method prevents the event from triggering other HTMX requests on parent elements.

```html
<div hx-get="/click" hx-trigger=@Trigger.OnEvent("click").Consume()>Click Me</div>
// Resulting hx-trigger: <div hx-get="/click" hx-trigger="click consume">Click Me</div>
```

### Queue

Specifies how events are queued when an event occurs while a request is in flight by adding the "queue" modifier. This method sets the event queuing option, such as "first", "last", "all", or "none".

**Parameters:**
- `option` (TriggerQueueOption, optional): The queue option.

```html
<div hx-get="/process" hx-trigger=@Trigger.OnEvent("click").Queue(TriggerQueueOption.All)>Queue All</div>
// Resulting hx-trigger: <div hx-get="/process" hx-trigger="click queue:all">Queue All</div>
```