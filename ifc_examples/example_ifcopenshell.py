import ifcopenshell
import uuid

# Function to generate a unique GlobalId
def generate_guid():
    return str(uuid.uuid4().hex.upper())

# Open or create an IFC file
new_ifc = ifcopenshell.file()

# Create or retrieve the spatial structure
project = new_ifc.create_entity("IfcProject", GlobalId=generate_guid(), Name="Project Name")
site = new_ifc.create_entity("IfcSite", GlobalId=generate_guid(), Name="Site Name")
building = new_ifc.create_entity("IfcBuilding", GlobalId=generate_guid(), Name="Building Name")
storey = new_ifc.create_entity("IfcBuildingStorey", GlobalId=generate_guid(), Name="Storey Name")

# Establish relationships
new_ifc.create_entity("IfcRelAggregates", RelatingObject=project, RelatedObjects=[site])
new_ifc.create_entity("IfcRelAggregates", RelatingObject=site, RelatedObjects=[building])
new_ifc.create_entity("IfcRelAggregates", RelatingObject=building, RelatedObjects=[storey])

# Create your object (mesh)
mesh = new_ifc.create_entity(
    "IfcBuildingElementProxy", 
    GlobalId=generate_guid(), 
    Name="Example Mesh"
)

# Link the object to the spatial structure using IfcRelContainedInSpatialStructure
new_ifc.create_entity(
    "IfcRelContainedInSpatialStructure",
    GlobalId=generate_guid(),
    RelatingStructure=storey,  # Link to the storey
    RelatedElements=[mesh]  # List of elements to link
)

# Save the file (if needed)
new_ifc.write("output.ifc")
