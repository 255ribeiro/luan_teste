import ifcopenshell
import ifcopenshell.util.element
import uuid

def create_guid():
    return ifcopenshell.guid.compress(uuid.uuid4().hex)

# Create a new IFC file
ifc_file = ifcopenshell.file()

# Create IfcProject
project = ifc_file.create_entity("IfcProject", GlobalId=create_guid(), Name="Sample Project")
context = ifc_file.create_entity(
    "IfcGeometricRepresentationContext",
    GlobalId=create_guid(),
    ContextType="Model",
    ContextIdentifier="3D",
    CoordinateSpaceDimension=3,
    Precision=1e-5,
)
project.RepresentationContexts = [context]
project.UnitsInContext = ifc_file.create_entity("IfcUnitAssignment")

# Create IfcSite
site = ifc_file.create_entity("IfcSite", GlobalId=create_guid(), Name="Default Site")

# Create IfcBuilding
building = ifc_file.create_entity("IfcBuilding", GlobalId=create_guid(), Name="Default Building")

# Create IfcBuildingStorey
storey = ifc_file.create_entity("IfcBuildingStorey", GlobalId=create_guid(), Name="Ground Floor", Elevation=0.0)

# Establish relationships
ifc_file.create_entity("IfcRelAggregates", GlobalId=create_guid(), RelatingObject=project, RelatedObjects=[site])
ifc_file.create_entity("IfcRelAggregates", GlobalId=create_guid(), RelatingObject=site, RelatedObjects=[building])
ifc_file.create_entity("IfcRelAggregates", GlobalId=create_guid(), RelatingObject=building, RelatedObjects=[storey])

# Create a slab
slab = ifc_file.create_entity("IfcSlab", GlobalId=create_guid(), Name="Floor Slab", PredefinedType="FLOOR")
slab_placement = ifc_file.create_entity(
    "IfcLocalPlacement",
    PlacementRelTo=None,
    RelativePlacement=ifcopenshell.util.element.create_ifcaxis2placement(ifc_file, (0.0, 0.0, 0.0)),
)
slab.ObjectPlacement = slab_placement

# Create a wall
wall = ifc_file.create_entity("IfcWall", GlobalId=create_guid(), Name="External Wall")
wall_placement = ifc_file.create_entity(
    "IfcLocalPlacement",
    PlacementRelTo=slab_placement,
    RelativePlacement=ifcopenshell.util.element.create_ifcaxis2placement(ifc_file, (0.0, 0.0, 0.0)),
)
wall.ObjectPlacement = wall_placement

# Relate construction elements to the storey
ifc_file.create_entity("IfcRelContainedInSpatialStructure", 
    GlobalId=create_guid(),
    RelatingStructure=storey,
    RelatedElements=[slab, wall]
)

# Add a custom property set to the wall
property_set = ifc_file.create_entity("IfcPropertySet", GlobalId=create_guid(), Name="Pset_CustomWallProperties")

# Add properties
area_property = ifc_file.create_entity(
    "IfcPropertySingleValue",
    Name="Area",
    NominalValue=ifc_file.create_entity("IfcAreaMeasure", 10.0),
)
volume_property = ifc_file.create_entity(
    "IfcPropertySingleValue",
    Name="Volume",
    NominalValue=ifc_file.create_entity("IfcVolumeMeasure", 2.5),
)
description_property = ifc_file.create_entity(
    "IfcPropertySingleValue",
    Name="Description",
    NominalValue=ifc_file.create_entity("IfcText", "External load-bearing wall"),
)
property_set.HasProperties = [area_property, volume_property, description_property]

# Relate property set to the wall
ifc_file.create_entity("IfcRelDefinesByProperties", 
    GlobalId=create_guid(), 
    RelatedObjects=[wall], 
    RelatingPropertyDefinition=property_set
)

# Save the file
ifc_file.write("output.ifc")
print("IFC file created as output.ifc")
