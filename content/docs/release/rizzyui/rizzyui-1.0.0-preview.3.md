---
title: "RizzyUI 1.0.0 Preview 3"
description: "Alpine code-behind reworked and tested, a shadcn-style RzProgress, and CSP fixes."
summary: ""
date: 2026-11-19T19:00:00-05:00
lastmod: 2026-11-19T19:00:00-05:00
draft: false
weight: 8
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

RizzyUI 1.0.0-preview.3 reworks Alpine code-behind (a component's `Component.razor.js` module) so it
works everywhere and is easy to write, test and deploy, and redesigns `RzProgress` after
shadcn/ui. Update all three packages:

```sh
dotnet add package RizzyUI --prerelease
dotnet new install RizzyUI.Templates
npm install @jalexsocial/rizzyui@next
```

## Breaking changes

[Upgrading RizzyUI]({{<ref "/docs/reference/upgrading-rizzyui.md">}}) lists what to change for each.

- **Code-behind props keep their C# names.** `Props="@(new { InitialCount = 10 })"` is read as
  `this.$props.InitialCount` (it was converted to `initialCount`). One setting keeps camelCase for
  the whole app.
- **`RzAlpineComponent` renders no scripts**, `Name` is optional, and a component without
  `[RzAlpineCodeBehind]` throws with instructions.
- **`RzProgress`** is a track with a `ProgressIndicator`: `Value` (`double?`), `Min` and `Max`
  replace `CurrentValue`, `MinValue` and `MaxValue`; `Label` and `LabelPosition` are replaced by
  markup, `ValueText` and `ProgressLabel`; there is no English default `AriaLabel`.
- **`AsChild` with plain markup** keeps the child's own attribute values (such as its `id`) when
  they conflict with the component's.

## Highlights

- **Code-behind that works everywhere.** Components start in the first page load, in htmx swaps
  and under a strict Content Security Policy; they used to fail in the first page load with
  Rizzy 6. Read props with `this.$props`, and set up child components in the new `ready()` hook.
- **Built for deployment.** Modules load from fingerprinted URLs that browsers cache for a year,
  pages left open across a deployment load the matching module, and failures are reported once
  with the component's name.
- **Tooling.** TypeScript declarations for `this.$props` and the `Rizzy` global,
  `dotnet new rizzyui-codebehind`, an optional esbuild pipeline for `.razor.ts` modules and npm
  imports, and `@jalexsocial/rizzyui/testing` to unit-test modules.
- **`RzProgress`** styled per instance with `class` on the track and the bar, with decimal values,
  an indeterminate state and no layout measuring.
- **Fixes:** `RzEmbeddedPreview` under the CSP build, `RzQuickReference` showing tags in headings,
  and `Rizzy.$data` returning a parent's data for a component that had not started.

The [full changelog](https://github.com/JalexSocial/RizzyUI/blob/main/CHANGELOG.md) and the
[GitHub release](https://github.com/JalexSocial/RizzyUI/releases/tag/v1.0.0-preview.3) list every
change.
