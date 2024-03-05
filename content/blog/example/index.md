---
title: "Welcome to Rizzy"
description: "We are just getting started."
summary: "So it turns out Razor Components do a pretty good job as a replacement for Razor Views."
date: 2023-09-07T16:27:22+02:00
lastmod: 2023-09-07T16:27:22+02:00
draft: false
weight: 50
categories: []
tags: []
contributors: []
pinned: false
homepage: false
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

This project was started based off of my early experiences using Htmx with Razor Views and more specifically Razor View Components. Razor View Components are kind of like mini controllers and can be embedded inside of Razor Views using tag helpers. The syntax is fairly clumsy and there isn't any support for nested child content. That was a bit rough to work with as HTML itself as a markup language utilizes nesting to great effect. 

<img src="/images/network.webp" style="width: 100%; margin-top: 2em; margin-bottom: 2em;">

## So how did we get here?

Most of the thanks for this whole project should go to the Blazor team who revamped Blazor SSR in a way that makes all of this possible.

[Khalid Abuhakmeh](https://github.com/khalidabuhakmeh) has been an excellent advocate of using Asp.net with Htmx. He's a developer advocate for Jetbrains and has published quite a few articles on various integration techniques between the two technologies. Khalid also has a nice library called [Htmx.net](https://github.com/khalidabuhakmeh/Htmx.Net) that encapsulates the Request and Response header management that Htmx utilizes. While I've contributed to that library for Rizzy I worked with Egil Hansen who created the basis for Htmx Request/Response management. He wrote the Request code and I wrote all the Response management code.

[Htmx.net](https://github.com/khalidabuhakmeh/Htmx.Net) also has some Tag Helpers which are useful to Views, but just won't work with Razor Components and never will. As a result, much of his library couldn't be used for Rizzy but there are still a lot of cool bells and whistles that come with the Rizzy implementation that wouldn't have been possible if it integrated Htmx.net. 

Rizzy was inspired by a lot of different projects, not all of them asp.net related. [htmx-go](https://github.com/angelofallars/htmx-go), a type-safe library for working with HTMX in Go, provided inspiration for the [fluent HTMX response Reswap modifiers](https://github.com/angelofallars/htmx-go).

```csharp
ViewContext.Htmx.Response.Reswap(SwapStyle.InnerHTML
    .ShowOn("#dynamic-area", ScrollDirection.Top)
    .After(TimeSpan.FromMilliseconds(500)));
// Reswap output: "innerHTML show:#dynamic-area:top swap:500ms"
```

[Alexander Zeitler](https://alexanderzeitler.com/articles/serializing-dotnet-csharp-object-for-use-with-alpine-x-data-attribute/) created an awesome tag helper for Asp.net views that serialized POCO objects so they could be utilized within the Alpine.js x-data attribute. I created a variant of his tag helper that could be used within Razor Components as [seen here](https://jalexsocial.github.io/rizzy.docs/docs/extensions/alpine.js-data/).

```csharp
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

[Egil Hansen](https://github.com/egil) started a project called [Htmxor](https://github.com/egil/Htmxor) that I contributed some code to but it didn't get too far into development. Nonetheless, it had some excellent ideas for dealing with HTMX configuration that I extended to utilize the Options pattern for managing both default and named configurations. There is quite a bit of code from that project that exists as the starting core of Rizzy. In fact, a lot of ideas from Rizzy came from conversations with Egil. Egil is notable because of his work as a developer on [bUnit](https://github.com/bUnit-dev/bUnit), which is a testing library for Blazor components.

Along the way I had a few contributions of my own. I created a [small HTMX extension](https://github.com/JalexSocial/BlazorHtmx) that allows a developer to perform streaming rendering of Razor Components with HTMX. I also created an [Htmx.Net Toast](https://github.com/JalexSocial/Htmx.Net.Toast) library to make it easy to integrate Toast messages with Asp.net Views.

## And where are we going?

At the moment I'm kind of dog-fooding my own library as I work on a passion project of my own that has a pretty sizeable scope. As I go through the process it's helping me discover pain points with Rizzy, which has been helpful to building up the library. At the moment I'd say the library is very much in active development and is at a point in time where the API should not be considered to be stable. There is a lot more to come, but I think this library should hopefully be useful to others who can join in and share ideas about the combination of technologies.
