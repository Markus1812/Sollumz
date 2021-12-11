import bpy
from ..sollumz_properties import items_from_enums, ArchetypeType, AssetType
from ..sollumz_properties import EntityProperties
from mathutils import Vector


class RoomProperties(bpy.types.PropertyGroup):
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

    # Blender usage only
    id: bpy.props.IntProperty(name="Id")


class PortalProperties(bpy.types.PropertyGroup):
    def get_room_index(self, room_from):
        selected_ytyp = bpy.context.scene.ytyps[bpy.context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        for index, room in enumerate(selected_archetype.rooms):
            if room_from:
                if room.id == self.room_from_id:
                    return index
            else:
                if room.id == self.room_to_id:
                    return index
        return 0

    def get_room_from_index(self):
        return self.get_room_index(True)

    def get_room_to_index(self):
        return self.get_room_index(False)

    def get_room_name(self, room_from):
        selected_ytyp = bpy.context.scene.ytyps[bpy.context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        if len(selected_archetype.rooms) < 1:
            return ""

        index = self.room_from_index if room_from else self.room_to_index

        if index < len(selected_archetype.rooms) and index >= 0:
            return selected_archetype.rooms[index].name
        else:
            return selected_archetype.rooms[0].name

    def get_room_from_name(self):
        return self.get_room_name(True)

    def get_room_to_name(self):
        return self.get_room_name(False)

    def get_name(self):
        return f"{self.room_from_name} to {self.room_to_name}"

    corner1: bpy.props.FloatVectorProperty(name="Corner 1", subtype="XYZ")
    corner2: bpy.props.FloatVectorProperty(name="Corner 2", subtype="XYZ")
    corner3: bpy.props.FloatVectorProperty(name="Corner 3", subtype="XYZ")
    corner4: bpy.props.FloatVectorProperty(name="Corner 4", subtype="XYZ")
    room_from_id: bpy.props.IntProperty(name="Room From Id")
    room_from_index: bpy.props.IntProperty(
        name="Room From Index", get=get_room_from_index)
    room_from_name: bpy.props.StringProperty(
        name="Room From", get=get_room_from_name)
    room_to_id: bpy.props.IntProperty(name="Room To Id")
    room_to_index: bpy.props.IntProperty(
        name="Room To Index", get=get_room_to_index)
    room_to_name: bpy.props.StringProperty(
        name="Room To", get=get_room_to_name)
    flags: bpy.props.IntProperty(name="Flags")
    mirror_priority: bpy.props.IntProperty(name="Mirror Priority")
    opacity: bpy.props.IntProperty(name="Opacity")
    audio_occlusion: bpy.props.IntProperty(name="Audio Occlusion")

    # Blender use only
    name: bpy.props.StringProperty(name="Name", get=get_name)
    id: bpy.props.IntProperty(name="Id")


class TimecycleModifierProperties(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    sphere: bpy.props.FloatVectorProperty(
        name="Sphere", subtype="QUATERNION", size=4)
    percentage: bpy.props.IntProperty(name="Percentage")
    range: bpy.props.FloatProperty(name="Range")
    start_hour: bpy.props.IntProperty(name="Start Hour")
    end_hour: bpy.props.IntProperty(name="End Hour")


class UnlinkedEntityProperties(bpy.types.PropertyGroup, EntityProperties):
    def update_linked_object(self, context):
        linked_obj = self.linked_object
        if linked_obj:
            linked_obj.location = self.position
            linked_obj.rotation_euler = self.rotation.to_euler()
            linked_obj.scale = Vector(
                (self.scale_xy, self.scale_xy, self.scale_z))

    def get_portal_index(self):
        selected_ytyp = bpy.context.scene.ytyps[bpy.context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        for index, portal in enumerate(selected_archetype.portals):
            if portal.id == self.attached_portal_id:
                return index
        return -1

    def get_portal_name(self):
        selected_ytyp = bpy.context.scene.ytyps[bpy.context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        index = self.attached_portal_index
        if index >= 0 and index < len(selected_archetype.portals):
            return selected_archetype.portals[self.attached_portal_index].name
        return ""

    # Transforms unused if no linked object
    position: bpy.props.FloatVectorProperty(name="Position")
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation", subtype="QUATERNION", size=4, default=(1, 0, 0, 0))
    scale_xy: bpy.props.FloatProperty(name="Scale XY", default=1)
    scale_z: bpy.props.FloatProperty(name="Scale Z", default=1)

    attached_portal_index: bpy.props.IntProperty(
        name="Attached Portal Index", get=get_portal_index)
    attached_portal_id: bpy.props.IntProperty(
        name="Attached Portal Id", default=-1)
    attached_portal_name: bpy.props.StringProperty(
        name="Attached Portal Name", get=get_portal_name)

    linked_object: bpy.props.PointerProperty(
        type=bpy.types.Object, name="Linked Object", update=update_linked_object)


class ArchetypeProperties(bpy.types.PropertyGroup):
    def update_asset_name(self, context):
        for obj in context.scene.collection.all_objects:
            if obj.name == self.asset_name:
                self.asset = obj
                return
        self.asset = None

    def set_asset_name(self, value):
        self["asset_name"] = value

    def new_portal(self):
        item = self.portals.add()
        self.portal_index = len(self.portals) - 1
        item.id = self.last_portal_id + 1
        self.last_portal_id = item.id
        return item

    def new_room(self):
        item = self.rooms.add()
        self.room_index = len(self.rooms) - 1
        item.name = f"Room.{self.room_index}"
        item.id = self.last_room_id + 1
        self.last_room_id = item.id
        return item

    bb_min: bpy.props.FloatVectorProperty(name="Bound Min")
    bb_max: bpy.props.FloatVectorProperty(name="Bound Max")
    bs_center: bpy.props.FloatVectorProperty(name="Bound Center")
    bs_radius: bpy.props.FloatProperty(name="Bound Radius")
    type: bpy.props.EnumProperty(
        items=items_from_enums(ArchetypeType), name="Type")
    lod_dist: bpy.props.FloatProperty(name="Lod Distance", default=100)
    flags: bpy.props.IntProperty(name="Flags")
    special_attribute: bpy.props.IntProperty(name="Special Attribute")
    hd_texture_dist: bpy.props.FloatProperty(
        name="HD Texture Distance", default=100)
    name: bpy.props.StringProperty(name="Name")
    texture_dictionary: bpy.props.StringProperty(name="Texture Dictionary")
    clip_dictionary: bpy.props.StringProperty(name="Clip Dictionary")
    drawable_dictionary: bpy.props.StringProperty(name="Drawable Dictionary")
    physics_dictionary: bpy.props.StringProperty(
        name="Physics Dictionary")
    asset_type: bpy.props.EnumProperty(
        items=items_from_enums(AssetType), name="Asset Type")
    asset: bpy.props.PointerProperty(name="Asset", type=bpy.types.Object)
    asset_name: bpy.props.StringProperty(
        name="Asset Name", update=update_asset_name)
    # Time archetype
    time_flags: bpy.props.IntProperty(name="Time Flags")
    # Mlo archetype
    mlo_flags: bpy.props.IntProperty(name="MLO Flags")
    rooms: bpy.props.CollectionProperty(type=RoomProperties, name="Rooms")
    portals: bpy.props.CollectionProperty(
        type=PortalProperties, name="Portals")
    entities: bpy.props.CollectionProperty(
        type=UnlinkedEntityProperties, name="Entities")
    timecycle_modifiers: bpy.props.CollectionProperty(
        type=TimecycleModifierProperties, name="Timecycle Modifiers")
    # Selected room index
    room_index: bpy.props.IntProperty(name="Room Index")
    # Selected portal index
    portal_index: bpy.props.IntProperty(name="Portal Index")
    # Unique portal id
    last_portal_id: bpy.props.IntProperty(name="")
    # Selected entity index
    entity_index: bpy.props.IntProperty(name="Entity Index")
    # Unique room id
    last_room_id: bpy.props.IntProperty(name="")
    # Selected timecycle modifier index
    tcm_index: bpy.props.IntProperty(
        name="Timecycle Modifier Index")


class CMapTypesProperties(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    # extensions
    archetypes: bpy.props.CollectionProperty(
        type=ArchetypeProperties, name="Archetypes")
    # Selected archetype index
    archetype_index: bpy.props.IntProperty(
        name="Archetype Index")


def register():
    bpy.types.Scene.ytyps = bpy.props.CollectionProperty(
        type=CMapTypesProperties, name="YTYPs")
    bpy.types.Scene.ytyp_index = bpy.props.IntProperty(name="YTYP Index")
    bpy.types.Scene.show_room_gizmo = bpy.props.BoolProperty(
        name="Show Room Gizmo")
    bpy.types.Scene.show_portal_gizmo = bpy.props.BoolProperty(
        name="Show Portal Gizmo")


def unregister():
    del bpy.types.Scene.ytyps
    del bpy.types.Scene.ytyp_index
    del bpy.types.Scene.show_room_gizmo
    del bpy.types.Scene.show_portal_gizmo
