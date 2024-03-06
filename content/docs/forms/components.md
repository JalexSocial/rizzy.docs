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

## RzEditForm

`RzEditForm` is the core component for handling forms in Blazor using SSR rendering. It leverages `RzFormContext` for managing form submission and validation state. This approach enhances form handling by integrating the form's context directly.

```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <DataAnnotationsValidator />
    <RzInputText @bind-Value="model.Property" />
    <button type="submit">Submit</button>
</RzEditForm>
```

## RzInputCheckbox

`RzInputCheckbox` is a component for rendering a checkbox input. It binds to a boolean property in the model, allowing the user to toggle between true and false states.

```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputCheckbox @bind-Value="model.AcceptTerms" />
</RzEditForm>
```

## RzInputDate

`RzInputDate` allows users to input a date. It binds to a `DateTime` or `DateTime?` property in the model, providing a user-friendly date picker interface.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputDate @bind-Value="model.BirthDate" />
</RzEditForm>
```

## RzInputFile



`RzInputFile` enables file selection for upload. Although it does not support interactive methods, it is essential for capturing file input from the user.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputFile />
</RzEditForm>
```

## RzInputNumber



`RzInputNumber` is designed for numerical input, binding to numeric types such as `int`, `float`, `decimal`, etc. It ensures that users can only enter valid numbers.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputNumber @bind-Value="model.Quantity" />
</RzEditForm>
```

## RzInputRadio and RzInputRadioGroup



`RzInputRadio` represents an individual radio button, whereas `RzInputRadioGroup` groups multiple radio buttons, binding their selected value to a model property.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputRadioGroup @bind-Value="model.SelectedOption">
        <RzInputRadio Value="Option1" /> Option 1
        <RzInputRadio Value="Option2" /> Option 2
    </RzInputRadioGroup>
</RzEditForm>
```

## RzInputSelect



`RzInputSelect` renders a dropdown list, binding its selected value to a property in the model. It is useful for selections where the user must choose from a list of predefined options.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputSelect @bind-Value="model.SelectedOption">
        <option value="Option1">Option 1</option>
        <option value="Option2">Option 2</option>
    </RzInputSelect>
</RzEditForm>
```

## RzInputText



`RzInputText` is used for single-line text inputs, binding to a string property in the model. It's a fundamental component for collecting textual data from the user.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputText @bind-Value="model.TextProperty" />
</RzEditForm>
```

## RzInputTextArea



`RzInputTextArea` provides a multi-line text input area, also binding to a string property in the model. It is suited for textual input that requires more space, like comments or descriptions.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <RzInputTextArea @bind-Value="model.MultilineText" />
</RzEditForm>
```

## RzValidationSummary



`RzValidationSummary` displays a summary of validation messages for the entire form, aiding in presenting errors or validation messages that arise from data annotations or custom validation logic in a centralized location.



```html
@code {
    private ExampleModel model = new ExampleModel();
    private RzFormContext rzFormContext = new RzFormContext("exampleForm", model);
}

<RzEditForm FormContext="@rzFormContext">
    <DataAnnotationsValidator>
    <RzValidationSummary />

        <div class="form-group">
            <label for="name">Property:</label>
            <RzInputText  class="form-control" @bind-Value="model.Property" />
            <RzValidationMessage For="@(() => model.Property)"/>
        </div>

        <button type="submit" class="btn btn-primary">Submit</button>

</RzEditForm>

```