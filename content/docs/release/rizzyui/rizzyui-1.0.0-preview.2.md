---
title: "RizzyUI 1.0.0 Preview 2"
description: "Accessibility, CSP and payload improvements, with the breaking changes planned before 1.0."
summary: ""
# DRAFT until 1.0.0-preview.2 is published to NuGet and npm: set draft to false and update the
# dates and the GitHub release link when the release is cut.
date: 2026-11-18T12:00:00-05:00
lastmod: 2026-11-18T12:00:00-05:00
draft: true
weight: 9
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

RizzyUI 1.0.0-preview.2 collects the changes planned before 1.0: components tested on real pages
under the standard and CSP runtimes, accessibility fixes found by those tests, a smaller download,
and the breaking changes that had to happen before a stable release. Update all three packages:

```sh
dotnet add package RizzyUI --prerelease
dotnet new install RizzyUI.Templates
npm install @jalexsocial/rizzyui@next
```

## Breaking changes

[Upgrading RizzyUI]({{<ref "/docs/reference/upgrading-rizzyui.md">}}) lists what to change for each.

- **`RzCombobox` sends only `value` and `text`** for each item to the page. Choose other fields
  with `ItemDataSelector`.
- **`RzSwitch` and `RzInputOTP` have no default `aria-label`**, so a `FieldLabel` or `<label>` names
  them.
- **The toast runtime loads on first use.** `Rizzy.toast` still works immediately;
  `await Rizzy.toast.ready()` when you need a return value.
- **Asset keys `CanvasConfetti` and `SliderScript` are gone**, and highlight.js ships its common
  languages (others are available as separate files).
- **One rule for attribute precedence:** attributes can override `role`, `data-slot` and `type`;
  everything else comes from parameters. `Element` is honored on every component.

## Highlights

- **Works with a strict Content Security Policy.** Components, including `RzDataTable` and its
  documented patterns, are tested in the browser under `rizzyui-csp.js` without `unsafe-eval` or
  `unsafe-inline`. A new `x-indeterminate` directive replaces `$el.indeterminate = ...`.
- **Accessibility fixes** from real-component tests: tooltips, menubar and command keyboard
  behavior, navigation menu semantics, labels for switch, OTP and combobox, dialog references,
  tab ids, and contrast in destructive buttons and toasts.
- **Smaller:** 33 KB of JavaScript on first load (was 37 KB), and a NuGet package of 2.9 MB
  (was 6.1 MB).
- **`RzIdScope`** gives components deterministic ids for fragments that are re-rendered.
- **`RzDataTable`** documents its contract: a headless table engine for markup you write, and you
  decide which data reaches the browser.

The [changelog](https://github.com/JalexSocial/RizzyUI/blob/main/CHANGELOG.md) lists every change.
