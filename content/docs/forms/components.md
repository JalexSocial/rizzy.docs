
---
title: "Input Components"
description: ""
summary: ""
date: 2024-03-06T07:25:03-05:00
lastmod: 2024-03-06T07:25:03-05:00
draft: false
weight: 50
toc: true
seo:
  title: "" # custom title (optional)
  description: "" # custom description (recommended)
  canonical: "" # custom canonical URL (optional)
  noindex: false # false (default) or true
---

## Realtime Input Validation

Rizzy provides a number of replacement components for standard Blazor input components that generate markup that is identical to the Asp.net form helper tags to facilitate realtime input validation. As long
as your models have Data Annotation attributes to mark them up you can take advantage of this feature.

## RzInputCheckboxBase

`RzInputCheckboxBase` is a component for rendering a checkbox input. It binds to a boolean property in the model, allowing the user to toggle between true and false states.

```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputCheckboxBase @bind-Value="model.AcceptTerms" />
</EditForm>
```

## RzInputDateBase

`RzInputDateBase` allows users to input a date. It binds to a `DateTime` or `DateTime?` property in the model, providing a user-friendly date picker interface.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputDateBase @bind-Value="model.BirthDate" />
</EditForm>
```

## RzInputFileBase



`RzInputFileBase` enables file selection for upload. Although it does not support interactive methods, it is essential for capturing file input from the user.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputFileBase />
</EditForm>
```

## RzInputNumberBase



`RzInputNumberBase` is designed for numerical input, binding to numeric types such as `int`, `float`, `decimal`, etc. It ensures that users can only enter valid numbers.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputNumberBase @bind-Value="model.Quantity" />
</EditForm>
```

## RzInputRadioBase and RzInputRadioGroupBase



`RzInputRadioBase` represents an individual radio button, whereas `RzInputRadioGroupBase` groups multiple radio buttons, binding their selected value to a model property.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputRadioGroupBase @bind-Value="model.SelectedOption">
        <RzInputRadioBase Value="Option1" /> Option 1
        <RzInputRadioBase Value="Option2" /> Option 2
    </RzInputRadioGroupBase>
</EditForm>
```

## RzInputSelectBase



`RzInputSelectBase` renders a dropdown list, binding its selected value to a property in the model. It is useful for selections where the user must choose from a list of predefined options.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputSelectBase @bind-Value="model.SelectedOption">
        <option value="Option1">Option 1</option>
        <option value="Option2">Option 2</option>
    </RzInputSelectBase>
</EditForm>
```

## RzInputTextBase



`RzInputTextBase` is used for single-line text inputs, binding to a string property in the model. It's a fundamental component for collecting textual data from the user.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputTextBase @bind-Value="model.TextProperty" />
</EditForm>
```

## RzInputTextAreaBase



`RzInputTextAreaBase` provides a multi-line text input area, also binding to a string property in the model. It is suited for textual input that requires more space, like comments or descriptions.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <RzInputTextAreaBase @bind-Value="model.MultilineText" />
</EditForm>
```

## RzValidationSummaryBase



`RzValidationSummaryBase` displays a summary of validation messages for the entire form, aiding in presenting errors or validation messages that arise from data annotations or custom validation logic in a centralized location.



```html
@code {
    private ExampleModel model = new ExampleModel();
}

<EditForm Model="model">
    <DataAnnotationsValidator>
    <RzValidationSummaryBase />

        <div class="form-group">
            <label for="name">Property:</label>
            <RzInputTextBase class="form-control" @bind-Value="model.Property" />
            <RzValidationMessageBase For="@(() => model.Property)"/>
        </div>

        <button type="submit" class="btn btn-primary">Submit</button>

</EditForm>

```