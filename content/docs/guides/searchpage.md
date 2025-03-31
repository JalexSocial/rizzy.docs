---
title: "Tutorial: Building a Dynamic Search Page"
description: "How to build a dynamic search page."
summary: ""
date: 2023-09-07T16:04:48+02:00
lastmod: 2023-09-07T16:04:48+02:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "searchpage-6a1a6be4373e933280d78ea53de6158e"
weight: 810
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

**Goal:** This tutorial will walk you through creating a common web feature: a search box that dynamically updates a list of results below it as the user types, without requiring a full page reload. We'll use Rizzy to bridge ASP.NET Core MVC, Blazor Components for rendering, and HTMX for the dynamic updates.

**Final Result:** We'll have a page with a search input. As the user types into the input (after a short delay), an HTMX request will be sent to the server with the search term. The server will filter a list of items and return *only* the updated list HTML, which HTMX will swap into the results area on the page.

**Technologies Used:**

*   ASP.NET Core MVC
*   Rizzy (including Rizzy.Htmx)
*   Blazor Components (Server-Side Rendered)
*   HTMX

---

### Prerequisites

*   .NET 8 SDK or later installed.
*   A text editor or IDE (like Visual Studio, VS Code, Rider).
*   Basic understanding of ASP.NET Core MVC (Controllers, Actions, Routing).
*   Basic understanding of C# and HTML.
*   A working ASP.NET Core project with Rizzy configured. Follow the [Getting Started]({{< ref "/docs/introduction/getting-started.md" >}}) guide if you haven't already.

---

### Step 1: Project Setup Recap

Ensure your `Program.cs` has Rizzy and HTMX services configured, and the necessary middleware (`UseAntiforgery`, `UseRizzy`) is added in the correct order.

Your controllers should inherit from `RzController` (or `RzControllerWithViews`). We'll use `RzController` for this tutorial.

```csharp
// Example Controller Structure
using Microsoft.AspNetCore.Mvc;
using Rizzy.Framework.Mvc; // Make sure this is included

public class SearchController : RzController
{
    // Actions will go here
}
```

---

### Step 2: Create the Model

Let's define a simple model for the items we want to search. Create a new file `Models/Product.cs`:

```csharp
// Models/Product.cs
namespace YourApp.Models; // Adjust namespace as needed

public record Product(int Id, string Name, string Description);
```

---

### Step 3: Create the Controller Actions

In your `SearchController.cs`, we need two actions:

1.  `Index`: Displays the initial search page.
2.  `SearchProducts`: Handles the HTMX request triggered by typing in the search box, performs the search, and returns the results partial view.

```csharp
// Controllers/SearchController.cs
using Microsoft.AspNetCore.Mvc;
using Rizzy.Framework.Mvc;
using Rizzy.Htmx; // For [HtmxRequest] attribute
using YourApp.Models; // Adjust namespace
using YourApp.Controllers.Search.Views; // Adjust namespace for your views

public class SearchController : RzController
{
    // Sample data - replace with your actual data source (e.g., database)
    private static readonly List<Product> AllProducts =
    [
        new(1, "Laptop Pro", "High-performance laptop for professionals."),
        new(2, "Wireless Mouse", "Ergonomic wireless mouse."),
        new(3, "Mechanical Keyboard", "RGB Mechanical Keyboard."),
        new(4, "4K Monitor", "32-inch 4K UHD Monitor."),
        new(5, "Webcam HD", "1080p HD Webcam with microphone."),
        new(6, "Laptop Stand", "Adjustable aluminum laptop stand.")
    ];

    // Action to display the initial search page
    [HttpGet]
    public IResult Index()
    {
        // Pass the complete list initially, or an empty list if you prefer
        var initialProducts = AllProducts;
        return View<SearchView>(new { Products = initialProducts });
    }

    // Action to handle the HTMX search request
    [HttpGet("Search/SearchProducts")] // Explicit route for clarity
    [HtmxRequest] // Ensure this action only responds to HTMX requests
    public IResult SearchProducts([FromQuery] string searchTerm = "")
    {
        List<Product> filteredProducts;

        if (string.IsNullOrWhiteSpace(searchTerm))
        {
            filteredProducts = AllProducts; // Show all if search is empty
        }
        else
        {
            filteredProducts = AllProducts
                .Where(p => p.Name.Contains(searchTerm, StringComparison.OrdinalIgnoreCase) ||
                            p.Description.Contains(searchTerm, StringComparison.OrdinalIgnoreCase))
                .ToList();
        }

        // Return ONLY the SearchResults component as a partial view
        // Pass the filtered list as a parameter
        return PartialView<SearchResults>(new { Products = filteredProducts });
    }
}
```

**Explanation:**

*   We have sample `AllProducts` data.
*   `Index` returns the main `SearchView` component, passing the initial list.
*   `SearchProducts` is marked with `[HtmxRequest]` so it only responds to HTMX. It takes the `searchTerm` from the query string (HTMX GET request).
*   It filters the products based on the `searchTerm`.
*   Crucially, it returns `PartialView<SearchResults>`, passing *only* the filtered data. This sends just the HTML for the results list back to the browser.

---

### Step 4: Create the Main View Component (`SearchView.razor`)

This component will contain the search input and the container where results will be loaded. Create `Controllers/Search/Views/SearchView.razor`:

```razor {title="Controllers/Search/Views/SearchView.razor" hl_lines=["9-14"]}
@using YourApp.Models // Adjust namespace
@using Rizzy

@inherits ComponentBase

<RzPageTitle>Dynamic Product Search</RzPageTitle>

<h1>Search Products</h1>

<div class="mb-3">
    <input type="search"
           name="searchTerm" @* Name matches the parameter in SearchProducts action *@
           class="form-control"
           placeholder="Type to search..."
           hx-get="/Search/SearchProducts"  @* Target the HTMX action *@
           hx-trigger="keyup changed delay:500ms, search" @* Trigger on typing (debounced) or search event *@
           hx-target="#search-results"      @* Place results in the div below *@
           hx-swap="innerHTML"              @* Replace content inside the target div *@
           hx-indicator="#search-indicator" @* Show loading indicator during request *@
           />
    <span id="search-indicator" class="htmx-indicator"> Searching...</span>
</div>

@* Container where search results will be dynamically loaded *@
<div id="search-results">
    @* Render the initial results list *@
    <SearchResults Products="@Products" />
</div>

@code {
    // Parameter to receive initial products from the Index action
    [Parameter]
    public List<Product> Products { get; set; } = []; // Initialize to empty list
}

```

**Explanation:**

*   The `<input>` element is the key here.
*   `name="searchTerm"`: Makes the input's value available as a query parameter with this name.
*   `hx-get`: Specifies the URL endpoint to call when triggered.
*   `hx-trigger`: Defines *when* the request is sent. `keyup changed delay:500ms` means it sends 500ms after the user stops typing *if* the value changed. `search` allows triggering manually (e.g., if the browser adds a search icon).
*   `hx-target="#search-results"`: Tells HTMX where to put the HTML response from the server – inside the `div` with `id="search-results"`.
*   `hx-swap="innerHTML"`: Specifies *how* to put the content – it replaces the *inner HTML* of the target div.
*   `hx-indicator="#search-indicator"`: Shows the element with `id="search-indicator"` while the request is in progress.
*   The `div#search-results` initially renders the `SearchResults` component with the data passed from the `Index` action.

---

### Step 5: Create the Results Component (`SearchResults.razor`)

This component is responsible for displaying the list of products. Create `Controllers/Search/Views/SearchResults.razor`:

```razor {title="Controllers/Search/Views/SearchResults.razor"}
@using YourApp.Models // Adjust namespace

@if (Products is null || !Products.Any())
{
    <p>No products found.</p>
}
else
{
    <ul class="list-group">
        @foreach (var product in Products)
        {
            <li class="list-group-item">
                <strong>@product.Name</strong>: @product.Description
            </li>
        }
    </ul>
}

@code {
    // Parameter to receive the list of products to display
    [Parameter]
    public List<Product>? Products { get; set; }
}
```

**Explanation:**

*   This is a simple display component.
*   It takes a `List<Product>` as a `[Parameter]`.
*   It checks if the list is empty or null and displays a message.
*   Otherwise, it iterates through the list and renders each product.

---

### Step 6: Run the Application

1.  Build and run your project.
2.  Navigate to `/Search` (or whatever route leads to your `SearchController`'s `Index` action).
3.  You should see the search input and the initial list of all products.
4.  Start typing in the search box (e.g., "Laptop").
5.  After you stop typing for 500ms, you should see the "Searching..." indicator briefly, and then the list below should update to show only products matching your search term.
6.  Clear the search box; the full list should reappear.

---

### Step 7: Potential Enhancements (Optional)

*   **Styling:** Improve the look of the loading indicator and results.
*   **Error Handling:** Add basic error handling in the controller or display messages if the HTMX request fails.
*   **Accessibility:** Ensure the search input and results are accessible (e.g., using ARIA attributes if necessary).
*   **More Complex Filtering:** Add more filter options (e.g., dropdowns, checkboxes) and update the HTMX request and controller action accordingly.

---

### Conclusion

You have successfully built a dynamic search page using Rizzy! This tutorial demonstrated:

*   Using an ASP.NET Core MVC Controller inheriting from `RzController`.
*   Rendering an initial page using `View<YourMainComponent>`.
*   Creating a dedicated Blazor component (`SearchResults`) for the dynamic part of the UI.
*   Using HTMX attributes on an input element to trigger partial updates.
*   Handling the HTMX request in a separate controller action that returns `PartialView<YourResultsComponent>`.
*   Passing data (search term and results list) between the client, controller, and components.

This pattern is fundamental to building interactive applications with Rizzy and HTMX, allowing you to leverage Blazor's component model for server-rendered UI while achieving dynamic updates without full page reloads. You can explore other Rizzy features like [Forms]({{< ref "/docs/forms/overview.md" >}}), [Swapping]({{< ref "/docs/htmx/swaps.md" >}}), and [Triggers]({{< ref "/docs/htmx/triggers.md" >}}) to build even richer experiences.