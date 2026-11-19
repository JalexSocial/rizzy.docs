---
title: "Upgrading RizzyUI"
description: "Move a RizzyUI app from Rizzy 5 and htmx 2 to RizzyUI 1.0 on Rizzy 6 and htmx 4."
summary: "The setup and component changes needed to upgrade RizzyUI to 1.0 on Rizzy 6 and htmx 4."
date: 2026-11-18T12:00:00-05:00
lastmod: 2026-11-18T19:00:00-05:00
draft: false
weight: 910
toc: true
seo:
  title: "Upgrading RizzyUI to Rizzy 6"
  description: "Upgrade guide for RizzyUI apps moving from Rizzy 5 (htmx 2) to RizzyUI 1.0 on Rizzy 6 (htmx 4): setup, scripts and breaking component changes."
---

RizzyUI 1.0 targets **Rizzy 6**, **htmx 4.0.1+** and **.NET 10**. Most of the work of upgrading is
Rizzy's, so start with [Upgrading to Rizzy 6]({{<ref "/docs/reference/upgrading.md">}}). This page
lists what changes in RizzyUI itself. The complete reference, with the audit finding behind each
change, is the
[migration guide in the RizzyUI repository](https://github.com/JalexSocial/RizzyUI/blob/main/docs/migration/rizzy5-to-rizzy6.md),
and the [changelog](https://github.com/JalexSocial/RizzyUI/blob/main/CHANGELOG.md) lists every change.

## Compatibility

| RizzyUI | Rizzy | htmx | .NET |
|---|---|---|---|
| 1.0.0-preview.2 | 6.0.0-preview.3 | 4.0.1+ | 10 (apps on 11 work) |
| 1.0.0-preview.1 | 6.0.0-preview.3 | 4.0.1+ | 10 (apps on 11 work) |
| 0.9.x and earlier | 5.3.x | 2.x | 10 |

The `RizzyUI` package depends on `Rizzy`, which brings the matching `Rizzy.Htmx`; you do not need
to reference `Rizzy` yourself.

## Upgrade steps

1. **Update the packages.** Until 1.0.0 is released, include `--prerelease` and `@next`:

   ```sh
   dotnet add package RizzyUI --prerelease
   npm install @jalexsocial/rizzyui@next
   ```

   `htmx.org` is no longer a dependency of `@jalexsocial/rizzyui`. Rizzy's `<RzScripts />` loads
   htmx; if you bundle htmx yourself, install `htmx.org@^4.0.1`.

2. **Register Rizzy and RizzyUI.** `AddRizzy()` now also registers htmx support and Razor
   components. Remove `GenerateStyleNonce`/`InlineStyleNonce` from `AddHtmx(...)`.

   ```csharp
   builder.Services.AddRizzy();
   builder.Services.AddRizzyUI(config => config.DefaultTheme = RzTheme.ArcticTheme);
   ```

3. **Replace the head setup in your root layout.** `<RzHeadOutlet />` replaces `<HeadOutlet />` and
   `<HtmxConfigHeadOutlet />`; `<RzScripts />` replaces your htmx and `rizzy.js` script tags. Keep the
   RizzyUI module after them and remove any `hx-ext="rizzy-nonce"` attribute.

   ```razor
   <RzHeadOutlet />
   <RzScripts />
   <script type="module" nonce="@Nonce" src="/_content/RizzyUI/js/rizzyui.min.js"></script>
   ```

   With a Content Security Policy, load `rizzyui-csp.min.js` instead.

4. **No `<base href="/">` in your layout?** Add it, or give Rizzy an absolute script URL:
   `builder.Services.AddRizzy(o => o.ClientScriptUrl = "/_content/Rizzy/js/rizzy.js");`

5. **Remove `antiforgerySnippet.js`.** It does nothing with htmx 4; Rizzy 6 attaches the
   antiforgery token itself.

6. **Update your own htmx markup and event names** as described in
   [Upgrading to Rizzy 6]({{<ref "/docs/reference/upgrading.md">}}). RizzyUI's components need no
   change. The one most often missed in RizzyUI apps is the swap modifier `show:window:top`, which
   becomes `show:top showTarget:window`.

## Who loads which script

| Script | Loaded by |
|---|---|
| htmx 4, `rizzy.js` and Rizzy's htmx extensions | `<RzScripts />` (Rizzy) |
| Alpine.js and its plugins | RizzyUI (`rizzyui.min.js` / `rizzyui-csp.min.js`). Do not load Alpine yourself; RizzyUI starts it. |
| Component code | RizzyUI, on demand, when a component appears on the page |
| Third-party libraries (Chart.js, Tom Select, flatpickr, ...) | RizzyUI components, on demand, from pinned CDN URLs with Subresource Integrity. Override `RizzyUIConfig.AssetUrls` to self-host. |

## Breaking changes in 1.0.0-preview.1

- **`RzButton` has no default `aria-label`.** The visible text names the button. Set
  `AssistiveLabel` on icon-only buttons; checkers will otherwise report them.
- **`RzMarkdown` escapes raw HTML by default.** Set `AllowUnsafeHtml="true"` only for Markdown you
  trust; enabling it for user content allows script injection.
- **Dialog triggers** render `x-on:click` instead of an inline `onclick` (so they work under a CSP).
- **npm entry points** are `dist/js/rizzyui.js` and `dist/js/rizzyui-csp.js`.

Behavior you may notice: dialogs and sheets close on Escape and return focus to their trigger (set
`CloseOnEscape="false"` to keep the old behavior); forms and `hx-*` buttons inside dialogs use htmx;
labels no longer render resource keys.

## Changes in 1.0.0-preview.2

Apps already on preview.1 may need to adjust for these changes in 1.0.0-preview.2
([release notes]({{<ref "/docs/release/rizzyui/rizzyui-1.0.0-preview.2.md">}})):

| Change | What to do |
|---|---|
| `RzCombobox` sends only `value` and `text` for each item to the page | If an item or option template reads other fields, list them with `ItemDataSelector="@(u => new { u.Name, u.Email })"` |
| `RzSwitch` and `RzInputOTP` no longer set a default `aria-label` | Label them with `FieldLabel For` or `<label for>`; pass `aria-label` when there is no visible label |
| The toast runtime loads on first use | `Rizzy.toast` calls still work immediately; `await Rizzy.toast.ready()` before code that needs a return value |
| The `CanvasConfetti` and `SliderScript` asset keys are gone | Remove them from any `ComponentAssetKeys` |
| highlight.js ships common languages only | Register `vendor/highlightjs/languages/<name>.min.js` as an asset for other languages |
| `Element` is honored on every component | Remove `Element` where you passed it without effect |
| Attributes can override only `role`, `data-slot` and `type` | Use the component's parameter (for example `AriaLabel`) instead of the attribute |
| `AsChild`: the child's own classes win Tailwind conflicts | Check `AsChild` children whose classes conflict with the component's |
| Generated ids such as dialog titles are `{Id}-title` | Nothing, unless CSS or scripts matched the old ids; `RzIdScope` gives deterministic ids |

The full list, including fixes and additions such as `x-indeterminate`, is in the changelog under
"1.0.0-preview.2".

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Components render but nothing is interactive | The RizzyUI module is missing or not `type="module"`, or the console shows a script error. See the RizzyUI [Getting Started guide](https://rizzyui.jalex.io/docs/getting-started). |
| Components initialized twice | Remove your own Alpine.js script. |
| 404 for `.../_content/Rizzy/js/rizzy.js` on nested routes | Add `<base href="/">` or set `ClientScriptUrl` to an absolute URL. |
| Unsafe htmx requests fail with 400 | Render `<RzHeadOutlet />` before `<RzScripts />` and call `app.UseAntiforgery()`. |
| Icon-only buttons flagged by accessibility checkers | Set `AssistiveLabel`. |
