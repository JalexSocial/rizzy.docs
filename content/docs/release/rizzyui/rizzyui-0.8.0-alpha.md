---
title: "Rizzyui 0.8.0 Alpha"
description: ""
summary: ""
date: 2025-05-05T18:48:37-04:00
lastmod: 2025-05-05T18:48:37-04:00
draft: false
weight: 999
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

# 📦 Modal Dialogs, Localization, and Accessibility Upgrades

## ✨ New Features

* **🪟 Modal Dialog Component**
  Introduced a fully customizable modal built with Alpine.js and Razor Components:

  * Lifecycle events (`before-open`, `after-close`, etc.)
  * HTMX content swapping support
  * Accessibility compliance
  * Themed styling and full documentation

* **🌐 Localization & Culture Support**

  * Added support for **English**, **German**, **Spanish**, **French**, and **Portuguese**
  * Default culture set to English
  * Integrated `RizzyStringLocalizer` for culture-aware resource fallback

* **🔄 RzSpinner Component**

  * New spinner with customizable sizes and fill colors
  * Improved HTML encoding for component previews

* **🌓 Enhanced Dark Mode Toggle**

  * Dynamically responds to OS theme settings
  * Encapsulated theme logic with proper cleanup

* **🔔 Notification & Validation Styles**

  * Introduced success, error, warning, and info styles
  * Animated transitions and validation error enhancements

---

## 🛠 Improvements & Refactors

* **🧩 Alpine.js Refactor**

  * Shifted `x-data` from root to inner containers for better structure and reusability
  * Applied updates to all modal, alert, and heading components

* **♿ Accessibility Overhaul**

  * Improved semantic structure for `RzAlert`, `RzAvatar`, `RzDivider`, and layout components
  * Added ARIA roles and hidden attributes for screen reader compatibility

* **🧱 Component Architecture Revamp**

  * Simplified Razor component structure
  * Promoted two-file convention, Tailwind-based styling, and minimal code-behind
  * Removed redundant theme abstraction

* **🧭 Localization Service Enhancements**

  * Centralized service resolution with null safety and detailed error handling
  * Improved fallback logic to support both app-level and embedded resources

* **💅 UI/UX Polishing**

  * Cleaned up modal styles, wrappers, and unused props
  * Updated homepage headings and content structure
  * Streamlined `RzDivider` rendering logic

---

## 🐞 Fixes

* Resolved issues with Alpine `x-data` bindings across components
* Rewrote localization functions for proper local resource resolution
* Removed outdated safelist scripts
* Fixed build issues and improved CI reliability

---

## 📦 Build & Maintenance

* Updated CI workflow (npm registry, asset handling)
* Cleaned up project files and script references
* Reorganized base styles and code documentation
* Refreshed README with logo, clearer structure, and emoji ✨
* Added license attributions for PenguinUI and LoadJs

