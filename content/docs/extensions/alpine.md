---
title: "Alpine.js Data"
description: ""
summary: ""
date: 2024-03-05T08:08:19-05:00
lastmod: 2024-03-05T08:08:19-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "alpine-c19164d543173361f76fbb7f91b54388"
weight: 200
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Alpine.js and HTMX are a powerful combination for creating interactive web applications with minimal complexity. Alpine.js provides a simple and lightweight framework for managing the behavior and state of elements on the page, using a declarative syntax that is easy to read and understand. On the other hand, HTMX allows you to enhance your HTML with AJAX, CSS Transitions, and WebSocket features, enabling you to update content dynamically without writing much JavaScript. Together, they allow developers to build modern, dynamic web applications with clean, maintainable code, while keeping the focus on simplicity and performance. This pairing is especially well-suited for projects where you want the interactivity of a single-page application without the overhead of a more complex JavaScript framework.

One of the core features of Alpine.js is the `x-data` attribute, which allows you to define a JavaScript object that holds the state and methods for a particular part of your HTML. In this tutorial, we'll go through a simple example to demonstrate how to use the `x-data` attribute in Alpine.js.

## Prerequisites

Ensure you have included Alpine.js in your project. See [Alpine.js Installation](https://alpinejs.dev/essentials/installation).

## Setting Up the HTML Structure

Create a simple HTML structure where you want to utilize Alpine.js. For this example, we'll create a div element that will display a message and a button to update that message:

```html
<div x-data="{ message: 'Hello, Alpine.js!' }">
    <p x-text="message"></p>
    <button @click="message = 'Message updated!'">Update Message</button>
</div>
```

This simple example is great for demo purposes but falls short once we try to build bigger applications powered by actual data.  For example, what if you want to serialize an existing POCO object server-side? Rizzy provides an Object extension method called `SerializeAsAlpineData` for this purpose.

## POCO Model Definition

```csharp {title="MessageViewModel.cs"}

public class MessageViewModel
{
  public string Message { get; set; }
}

```

Now instead of having to hard code the Json-encoded POCO object inside of the x-data attribute you can call the extension method to do the same.

## Full Example

Here's the complete HTML with Alpine.js:

```html
  @using Rizzy.Extensions

  @code {
    var model = new MessageViewModel {
      Message = "Hello, Alpine.js!"
    };
  }
    <div x-data="@model.SerializeAsAlpineData()">
        <p x-text="message"></p>
        <button @click="message = 'Message updated!'">Update Message</button>
    </div>
```

## The Rendered Result

```html
<div x-data="{ message: 'Hello, Alpine.js!' }">
    <p x-text="message"></p>
    <button @click="message = 'Message updated!'">Update Message</button>
</div>
```

## Conclusion

In this tutorial, we've seen how to use the `x-data` attribute in Alpine.js with the `SerializeAsAlpineData` extension method. This allows us to easily manage the state and behavior of our elements without needing a more complex JavaScript framework.