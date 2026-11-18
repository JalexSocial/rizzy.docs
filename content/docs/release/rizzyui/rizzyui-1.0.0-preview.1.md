---
title: "RizzyUI 1.0.0 Preview 1"
description: "The first RizzyUI release for Rizzy 6 and htmx 4, with a dotnet new template."
summary: ""
date: 2026-11-17T12:00:00-05:00
lastmod: 2026-11-17T12:00:00-05:00
draft: false
weight: 10
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

RizzyUI 1.0.0-preview.1 is the first RizzyUI release for **Rizzy 6** and **htmx 4**. It ships three
packages with the same version:

| Package | Where | What it is |
|---|---|---|
| `RizzyUI` | [NuGet](https://www.nuget.org/packages/RizzyUI) | The components |
| `RizzyUI.Templates` | [NuGet](https://www.nuget.org/packages/RizzyUI.Templates) | `dotnet new rizzyui` |
| `@jalexsocial/rizzyui` | [npm](https://www.npmjs.com/package/@jalexsocial/rizzyui) (`next` tag) | Tailwind plugin and client scripts |

RizzyUI 0.9.x stays on Rizzy 5 and htmx 2.

## Start a new app

```sh
dotnet new install RizzyUI.Templates
dotnet new rizzyui -o MyApp
cd MyApp
dotnet run
```

The template needs a .NET 10 or .NET 11 SDK and Node.js 20 or newer. The first build runs
`npm install` and Tailwind for you. The app has:

- a collapsible sidebar layout with light and dark mode
- a dashboard, a searchable and paged table, and a settings form that is validated on the server
  and posted with htmx (a failed post returns 422 and keeps what the user typed)
- 404 and error pages
- `RzController` pages and minimal API endpoints that return fragments

Options: `--framework net10.0|net11.0` and `--theme Arctic|Vercel`. The
[RizzyUI Getting Started guide](https://rizzyui.jalex.io/docs/getting-started) walks through the
project and how to add a page.

## Add RizzyUI to an existing app

```sh
dotnet add package RizzyUI --prerelease
npm install @jalexsocial/rizzyui@next
```

Until 1.0.0 is released, include `--prerelease` and `@next`; without them you get 0.9.x, which needs
Rizzy 5.

## Breaking changes

- **Rizzy 6 and htmx 4 are required.** Upgrade Rizzy first ([Upgrading to Rizzy 6]({{<ref "/docs/reference/upgrading.md">}})),
  then RizzyUI ([Upgrading RizzyUI]({{<ref "/docs/reference/upgrading-rizzyui.md">}})).
- **htmx is no longer an npm dependency** of `@jalexsocial/rizzyui`. Load it with Rizzy's
  `<RzScripts />` or install `htmx.org` 4 yourself.
- **`antiforgerySnippet.js` does nothing.** Rizzy 6 attaches the antiforgery token itself; remove the
  script tag.
- **`RzButton` has no default `aria-label`.** The visible text names the button. Set
  `AssistiveLabel` on icon-only buttons.
- **`RzMarkdown` escapes raw HTML by default.** Set `AllowUnsafeHtml="true"` only for trusted
  content.

## Notable fixes

- Inputs render the value of the field named by `For`, so a form re-rendered after a failed post
  keeps what the user entered.
- A `FieldLabel` with `For` points at its input whether the label comes before or after it.
- Dialogs, alert dialogs and sheets close on Escape, trap focus and return focus to the trigger.
- htmx attributes work inside dialogs, sheets, popovers and dropdowns.
- `RzDateEdit` submits its value with the form, respects its `Options` and `DateFormat`, and cleans
  up when an htmx swap removes it.
- Default CDN assets are pinned to exact versions and load with Subresource Integrity.

The [full changelog](https://github.com/JalexSocial/RizzyUI/blob/main/CHANGELOG.md) and the
[GitHub release](https://github.com/JalexSocial/RizzyUI/releases/tag/v1.0.0-preview.1) list every
change.
