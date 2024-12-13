1. Define a Custom Type
In IFC, custom types can be created using IfcTypeObject. These types allow you to standardize properties across multiple elements.

Here’s how you define a custom type in IfcOpenShell:

python
Copiar código
import ifcopenshell
import uuid

# Function to generate a unique GlobalId
def generate_guid():
    return str(uuid.uuid4().hex.upper())

# Open or create an IFC file
ifc = ifcopenshell.file()

# Create an IfcProject for context (required)
project = ifc.create_entity("IfcProject", GlobalId=generate_guid(), Name="Example Project")
site = ifc.create_entity("IfcSite", GlobalId=generate_guid(), Name="Example Site")
building = ifc.create_entity("IfcBuilding", GlobalId=generate_guid(), Name="Example Building")
storey = ifc.create_entity("IfcBuildingStorey", GlobalId=generate_guid(), Name="Example Storey")

# Establish relationships
ifc.create_entity("IfcRelAggregates", RelatingObject=project, RelatedObjects=[site])
ifc.create_entity("IfcRelAggregates", RelatingObject=site, RelatedObjects=[building])
ifc.create_entity("IfcRelAggregates", RelatingObject=building, RelatedObjects=[storey])

# Define a custom type (e.g., MyCustomType)
custom_type = ifc.create_entity(
    "IfcBuildingElementType",
    GlobalId=generate_guid(),
    Name="MyCustomType",
    PredefinedType="NOTDEFINED"  # Use NOTDEFINED if it’s truly custom
)

# Add the type to the IfcRelDefinesByType relationship
ifc.create_entity(
    "IfcRelDefinesByType",
    GlobalId=generate_guid(),
    RelatingType=custom_type,
    RelatedObjects=[]
)
2. Create a Custom Property Set
Property sets are containers for properties. Each property can store values such as text, numbers, or more complex data.

Here’s how to create a property set:

python
Copiar código
# Create a custom property set
pset = ifc.create_entity(
    "IfcPropertySet",
    GlobalId=generate_guid(),
    Name="MyCustomPset"
)

# Add properties to the property set
property_1 = ifc.create_entity(
    "IfcPropertySingleValue",
    Name="Property1",
    Description="Description of Property1",
    NominalValue=ifcopenshell.entity_instance.double(42.0)  # Example value
)
property_2 = ifc.create_entity(
    "IfcPropertySingleValue",
    Name="Property2",
    Description="Description of Property2",
    NominalValue=ifcopenshell.entity_instance.text("Example Text")
)

# Link properties to the property set
pset.HasProperties += [property_1, property_2]

# Define the relationship between the custom type and the property set
ifc.create_entity(
    "IfcRelDefinesByProperties",
    GlobalId=generate_guid(),
    RelatedObjects=[custom_type],
    RelatingPropertyDefinition=pset
)
3. Create an Element of the Custom Type
Once the type and its property set are defined, you can create an element and assign it to the custom type:

python
Copiar código
# Create an instance of the custom type
element = ifc.create_entity(
    "IfcBuildingElementProxy",  # Replace with the appropriate entity type
    GlobalId=generate_guid(),
    Name="Instance of MyCustomType"
)

# Assign the element to the custom type
ifc.create_entity(
    "IfcRelDefinesByType",
    GlobalId=generate_guid(),
    RelatingType=custom_type,
    RelatedObjects=[element]
)

# Place the element in the spatial structure
ifc.create_entity(
    "IfcRelContainedInSpatialStructure",
    GlobalId=generate_guid(),
    RelatingStructure=storey,
    RelatedElements=[element]
)
4. Fill and Access the Custom Properties
The properties added to the custom type through the property set can now be accessed or modified.

Accessing Properties:
python
Copiar código
# Access the custom property set
for pset in custom_type.IsDefinedBy:
    if pset.RelatingPropertyDefinition.is_a("IfcPropertySet"):
        for prop in pset.RelatingPropertyDefinition.HasProperties:
            print(f"{prop.Name}: {prop.NominalValue.wrappedValue}")
Modifying Properties:
python
Copiar código
# Modify a property value
property_1.NominalValue = ifcopenshell.entity_instance.double(100.0)
5. Save the IFC File
Finally, save the file to ensure your changes are preserved:

python
Copiar código
ifc.write("output.ifc")
Result
This process will:

Define a custom type (MyCustomType).
Create a property set (MyCustomPset) linked to the type.
Create an element of the custom type and place it in the spatial structure.
Populate and access properties for the custom type.
Let me know if you need further assistance or explanations!