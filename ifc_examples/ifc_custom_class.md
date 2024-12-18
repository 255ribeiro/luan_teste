# IfcOpenShell Custom IFC Class Properties Psets Specification
## Introduction
To create custom IFC class properties psets in IfcOpenShell, you can use the `ifcopenshell.api.pset` module.

## Creating Custom IFC Class Properties Psets
To create custom IFC class properties psets, you can use the `ifcopenshell.api.pset.add_pset` function.

### Example Code
```python
import ifcopenshell
import ifcopenshell.api

# Create a new IFC file
model = ifcopenshell.api.project.create_file()

# Create a custom IFC class
custom_class = ifcopenshell.api.root.create_entity(model, ifc_class="IfcCustomType")

# Add a custom property set
pset = ifcopenshell.api.pset.add_pset(model, custom_class, "MyCustomPset")

# Add properties to the custom property set
ifcopenshell.api.pset.edit_pset(
    model,
    pset=pset,
    properties={
        "MyCustomProperty1": "Hello World",
        "MyCustomProperty2": 42.0,
        "MyCustomProperty3": True,
    },
)


------------


Specifying Variable Types
To specify variable types, you can use Python type hints or annotations.

Example Code
import ifcopenshell
import ifcopenshell.api
from typing import Dict

# Create a new IFC file
model = ifcopenshell.api.project.create_file()

# Create a custom IFC class
custom_class = ifcopenshell.api.root.create_entity(model, ifc_class="IfcCustomType")

# Add a custom property set
pset = ifcopenshell.api.pset.add_pset(model, custom_class, "MyCustomPset")

# Define properties with type hints
properties: Dict[str, type] = {
    "MyCustomProperty1": str,  # IfcLabel (string)
    "MyCustomProperty2": float,  # IfcReal (float)
    "MyCustomProperty3": bool,  # IfcBoolean (boolean)
    "MyCustomProperty4": int,  # IfcInteger (integer)
}

# Add properties to the custom property set
ifcopenshell.api.pset.edit_pset(
    model,
    pset=pset,
    properties={
        "MyCustomProperty1": "Hello World",
        "MyCustomProperty2": 42.0,
        "MyCustomProperty3": True,
        "MyCustomProperty4": 24,
    },
)

Creating Custom Property Set Templates
To create custom property set templates, you can use the ifcopenshell.api.pset_template.add_pset_template function.

Example Code
import ifcopenshell
import ifcopenshell.api

# Create a new IFC file
model = ifcopenshell.api.project.create_file()

# Create a custom IFC class
custom_class = ifcopenshell.api.root.create_entity(model, ifc_class="IfcCustomType")

# Create a custom property set template
pset_template = ifcopenshell.api.pset_template.add_pset_template(
    model,
    name="MyCustomPsetTemplate",
    applicable_entity="IfcCustomType",
    template_type="PSET_TYPEDRIVEN",
    properties=[
        {
            "name": "MyCustomProperty1",
            "primary_measure_type": "IfcLabel",  # string
            "description": "My custom property 1",
        },
        {
            "name": "MyCustomProperty2",
            "primary_measure_type": "IfcReal",  # float
            "description": "My custom property 2",
        },
        {
            "name": "MyCustomProperty3",
            "primary_measure_type": "IfcBoolean",  # boolean
            "description": "My custom property 3",
        },
        {
            "name": "MyCustomProperty4",
            "primary_measure_type": "IfcInteger",  # integer
            "description": "My custom property 4",
        },
    ],
)