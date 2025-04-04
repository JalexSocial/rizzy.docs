---
title: "Project Goals"
description: ""
summary: ""
date: 2024-02-05T12:06:48-05:00
lastmod: 2024-02-05T12:06:48-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "goals-1d556dae29cf5c18476d4edede8e8940"
weight: 20
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---


The goal of Rizzy is to allow developers to use server-rendered Blazor components as views within ASP.NET Core MVC or Minimal API applications, using HTMX to handle partial page updates. Key objectives include:

## Integration, Not Replacement
- Provide tools to use Blazor components for views within existing ASP.NET Core structures (MVC/Minimal API), not requiring a full rewrite.

## Blazor Components as Views
- Enable returning Blazor components (.razor) as `IResult` from controller actions or Minimal API endpoints, rendered server-side to HTML.

## HTMX Compatibility
- Ensure server-rendered Blazor component responses work correctly when requested and swapped by HTMX. Provide helpers for HTMX request/response headers.

## Server-Driven Content Swapping
- Provide mechanisms (like `HtmxSwapService`) allowing server-side logic (potentially outside the main component being rendered) to add extra HTML fragments to the response for HTMX Out-of-Band swaps.

## Enhance Documentation and Examples
- Provide comprehensive documentation and real-world examples demonstrating how to integrate the new library into existing MVC applications, covering common use cases and best practices.
