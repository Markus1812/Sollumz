import bpy
from ..sollumz_properties import items_from_enums, ArchetypeType, AssetType


class Room(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    bb_min: bpy.props.FloatVectorProperty(name="Bounds Min", subtype="XYZ")
    bb_max: bpy.props.FloatVectorProperty(name="Bounds Max", subtype="XYZ")
    blend: bpy.props.IntProperty(name="Blend", default=1)
    timecycle: bpy.props.StringProperty(
        name="Timecycle", default="int_GasStation")
    secondary_timecycle: bpy.props.StringProperty(
        name="Secondary Timecycle")
    flags: bpy.props.IntProperty(name="Flags")
    floor_id: bpy.props.IntProperty(name="Floor ID")
    exterior_visibility_depth: bpy.props.IntProperty(
        name="Exterior Visibility Depth", default=-1)


class Portal(bpy.types.PropertyGroup):
    corner1: bpy.props.FloatVectorProperty(name="Corner 1", subtype="XYZ")
    corner2: bpy.props.FloatVectorProperty(name="Corner 2", subtype="XYZ")
    corner3: bpy.props.FloatVectorProperty(name="Corner 3", subtype="XYZ")
    corner4: bpy.props.FloatVectorProperty(name="Corner 4", subtype="XYZ")


class TimecycleModifier(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    sphere: bpy.props.FloatVectorProperty(
        name="Sphere", subtype="QUATERNION", size=4)
    percentage: bpy.props.IntProperty(name="Percentage")
    start_hour: bpy.props.IntProperty(name="Start Hour")
    end_hour: bpy.props.IntProperty(name="End Hour")


class ArchetypeProperties(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(
        items=items_from_enums(ArchetypeType), name="Type")
    flags: bpy.props.IntProperty(name="Flags")
    special_attribute: bpy.props.IntProperty(name="Special Attribute")
    name: bpy.props.StringProperty(name="Name")
    texture_dictionary: bpy.props.StringProperty(name="Texture Dictionary")
    clip_dictionary: bpy.props.StringProperty(name="Clip Dictionary")
    drawable_dictionary: bpy.props.StringProperty(name="Drawable Dictionary")
    physics_dictionary: bpy.props.PointerProperty(
        name="Physics Dictionary (Collision)", type=bpy.types.Object)
    asset_type: bpy.props.EnumProperty(
        items=items_from_enums(AssetType), name="Asset Type")
    asset: bpy.props.PointerProperty(name="Asset", type=bpy.types.Object)
    # Time archetype
    time_flags: bpy.props.IntProperty(name="Time Flags")
    # Mlo archetype
    mlo_flags: bpy.props.IntProperty(name="MLO Flags")
    rooms: bpy.props.CollectionProperty(type=Room, name="Rooms")
    portals: bpy.props.CollectionProperty(type=Portal, name="Portals")
    timecycle_modifiers: bpy.props.CollectionProperty(
        type=TimecycleModifier, name="Timecycle Modifiers")


class CMapTypesProperties(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    # extensions
    archetypes: bpy.props.CollectionProperty(
        type=ArchetypeProperties, name="Archetypes")


def register():
    bpy.types.Scene.ytyps = bpy.props.CollectionProperty(
        type=CMapTypesProperties, name="YTYPs")
    bpy.types.Scene.ytyp_index = bpy.props.IntProperty(name="YTYP Index")
    bpy.types.Scene.archetype_index = bpy.props.IntProperty(
        name="Archetype Index")
    bpy.types.Scene.room_index = bpy.props.IntProperty(name="Room Index")
    bpy.types.Scene.portal_index = bpy.props.IntProperty(name="Portal Index")
    bpy.types.Scene.tcm_index = bpy.props.IntProperty(
        name="Timecycle Modifier Index")


def unregister():
    del bpy.types.Scene.ytyps
    del bpy.types.Scene.ytyp_index
    del bpy.types.Scene.room_index
    del bpy.types.Scene.portal_index
    del bpy.types.Scene.tcm_index
