---
title: "Upgrading to Rizzy 6"
description: "Move a Rizzy 5 / htmx 2 application to Rizzy 6 and htmx 4."
summary: "The setup, markup and API changes needed to upgrade from Rizzy 5 to Rizzy 6."
date: 2026-11-08T12:00:00-05:00
lastmod: 2026-11-08T12:00:00-05:00
draft: false
weight: 900
toc: true
seo:
  title: "Upgrading to Rizzy 6"
  description: "Upgrade guide from Rizzy 5 (htmx 2) to Rizzy 6 (htmx 4): setup, markup and breaking API changes."
---

Rizzy 6 targets **htmx 4.0.1+** and **.NET 10**. This page lists the steps most apps need. The
complete reference, with every breaking change and the audit finding behind it, is the
[upgrade guide in the Rizzy repository](https://github.com/JalexSocial/Rizzy/blob/main/docs/migration/htmx2-to-htmx4.md),
and the [changelog](https://github.com/JalexSocial/Rizzy/blob/main/CHANGELOG.md) summarizes the release.

## Upgrade steps

1. **Update the packages.** Reference `Rizzy` 6.x; it brings the matching `Rizzy.Htmx`. If you use the
   npm package, install `@jalexsocial/rizzy` 6.x and `htmx.org` 4.0.1 or later (`htmx.org` is now a
   peer dependency).
2. **Replace `<HeadOutlet />` with `<RzHeadOutlet />`** in your root layout, and replace your htmx and
   Rizzy script tags with `<RzScripts />` right after it (it loads htmx 4 with SRI, rizzy.js and any
   [extensions]({{<ref "/docs/htmx/extensions.md">}}) you enable):

   ```razor {title="AppLayout.razor"}
   <head>
       <RzHeadOutlet />
       <RzScripts />
   </head>
   ```

   Rizzy 5 added the htmx config meta tag (and the antiforgery token) through `<HeadContent>`, and a
   page with its own `<HeadContent>` silently removed it. See [Head]({{<ref "/docs/components/head.md">}}).
3. **Simplify registration.** `AddRizzy()` now registers htmx support and Razor components; you can
   drop `AddRazorComponents()` and keep `AddHtmx(...)` only to change the htmx configuration.
4. **Register MVC with `AddControllersWithViews()`** if your actions use `[ValidateAntiForgeryToken]`.
   Rizzy no longer injects MVC's antiforgery filters through reflection.
5. **Run the htmx upgrade checker** on your templates:

   ```bash
   npx -p htmx.org@4 upgrade-check --ext .razor --ext .cshtml ./
   ```

6. **Click through the app with the browser console open.** htmx 4 logs every error, and Rizzy warns
   about a missing config tag or a script/server version mismatch.

## Markup changes (htmx 4)

| htmx 2 | htmx 4 |
|---|---|
| Attributes inherited implicitly | Add `:inherited` (`hx-boost:inherited`, `hx-target:inherited`, …) or set `HtmxConfig.ImplicitInheritance = true` |
| `hx-ext="..."` | Removed: extensions register when their script loads. Enable them with `HtmxConfig.UseExtensions(...)`; `<RzScripts />` loads them and Rizzy keeps the allow-list in step |
| `hx-disable` to skip processing | `hx-ignore` |
| History cache in localStorage | No cache: back/forward re-fetch the page. Mark the element to restore with `hx-history-elt`, or set `HtmxConfig.History = HtmxHistoryMode.Reload` |
| 4xx/5xx responses not swapped | Swapped by default. Use it for validation (status 422) and `app.UseHtmxErrorHandling()` for server errors, or set `HtmxConfig.NoSwap = [204, 304, "4xx", "5xx"]` |
| `queue` trigger modifier | Removed: use `hx-sync` |

## Behavior changes in Rizzy

- **Layouts:** fragments (no layout) are returned only for htmx requests that target one element.
  Boosted body swaps, `hx-select` and back/forward restores get the full page. See [Layouts]({{<ref "/docs/components/layout.md">}}).
- **Validation:** return status 422 with the re-rendered form (`Response.Htmx().ValidationFailed()`);
  htmx 4 swaps it. `RzModelStateProvider` (not `RzInitialValidator`) shows `ModelState` errors, and
  `RzController` passes its `ModelState` automatically. See [Validation]({{<ref "/docs/forms/validation.md">}}).
- **Raw markup is explicit:** `AddSwappableContent`, `AddRawContent` and `AddChildContent` take a
  `MarkupString`; use `AddSwappableText`/`AddChildText` for text, which is HTML-encoded.
- **Streaming rendering** cooperates with htmx core: swaps, `HX-*` headers, `hx-status` and triggers
  work while updates stream in. See [Streaming]({{<ref "/docs/htmx/streaming.md">}}).
- **CSP nonces:** server-rendered scripts in htmx responses run under a nonce-based policy while
  injected ones stay blocked; `GenerateStyleNonce` is gone. See [Content Security Policy]({{<ref "/docs/introduction/contentsecurity.md">}}).
- **Confirm dialogs:** `hx-confirm` uses the browser's `confirm()` unless a custom dialog handles
  `rz:confirm-dialog`.
- **`[RizzyParameterize]`** works in your own projects: the source generator ships in the Rizzy package.
