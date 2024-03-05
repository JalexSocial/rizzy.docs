---
title: "General Methods"
description: ""
summary: ""
date: 2024-03-05T08:29:43-05:00
lastmod: 2024-03-05T08:29:43-05:00
draft: false
menu:
  docs:
    parent: ""
    identifier: "general-761894e3d2411fc91b95bc8504594be2"
weight: 400
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## ToDictionary

The `ToDictionary` extension method is a utility method that allows you to convert a Plain Old CLR Object (POCO) into a dictionary representation, where each property name-value pair of the POCO becomes a key-value pair in the dictionary.

### Method Signature

```csharp
public static Dictionary<string, object?> ToDictionary(this object? values)
```

#### Parameters

- `values`: The POCO object to be converted into a dictionary. It is marked as nullable, indicating that `null` can be passed as an argument.

#### Return Value

- Returns a `Dictionary<string, object?>`: A dictionary containing keys and values representing the properties of the input POCO object. The dictionary uses a case-insensitive string comparer.

### Example

```csharp
public class Employee
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Department { get; set; }
}

// ...

var employee = new Employee
{
    Name = "Jane Doe",
    Age = 28,
    Department = "Human Resources"
};

Dictionary<string, object?> employeeDict = employee.ToDictionary();

```
