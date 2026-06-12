---
title: "Swapping"
description: ""
summary: ""
date: 2024-03-05T09:45:12-05:00
lastmod: 2024-03-05T09:45:12-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "swapping-630bb6a52f3b92ae49b01e8abad5e57c"
  weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

Swapping with HTMX involves dynamically replacing a portion of your webpage's content with new data from the server without a full page reload, utilizing custom `hx-swap` attributes to define how the content should be transitioned. Out‑of‑band swapping extends this concept by allowing parts of the webpage outside the target element to be updated simultaneously, specified by the `hx-swap-oob` attribute, which is useful for updating multiple sections of a page in response to a single HTMX request. This mechanism facilitates more interactive and responsive web applications by minimizing the need for full page refreshes and enabling precise control over which parts of the page are updated.

{{< callout context="info" title="HTMX 4 Update" icon="info-circle" >}}
In HTMX 4 the main swap is performed first and any out‑of‑band (`hx-swap-oob`) or `<hx-partial>` swaps occur afterwards【381859254872383†L194-L204】. Consider structuring your response accordingly if you rely on OOB content to prepare the DOM before the main fragment arrives. HTMX 4 also introduces the `<hx-partial>` element, which can target multiple elements in a single response and specify its own `hx-target` and `hx-swap` strategy【381859254872383†L461-L475】.
{{< /callout >}}

Rizzy provides a component called `HtmxSwappable` along with a scoped service called `HtmxSwapService` to make this easier for you.

{{< link-card
  title="Out of Band Swapping"
  description="Please see \"Out of Band Swapping\" for full details"
  href="/docs/htmx/out-of-band-swapping/"
  target="_blank"
>}}