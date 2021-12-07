import bpy
from ..sollumz_helper import SOLLUMZ_OT_base
from ..sollumz_properties import SOLLUMZ_UI_NAMES, ArchetypeType, AssetType
from ..tools.blenderhelper import get_selected_vertices
from ..tools.meshhelper import get_bound_extents, get_bound_center, get_obj_radius
from ..tools.utils import get_min_vector_list, get_max_vector_list
from ..resources.ytyp import *
from ..resources.ymap import *
from .properties import *
import os
import traceback


class SOLLUMZ_OT_create_ytyp(SOLLUMZ_OT_base, bpy.types.Operator):
    """Add a ytyp to the project"""
    bl_idname = "sollumz.createytyp"
    bl_label = "Create YTYP"

    def run(self, context):
        item = context.scene.ytyps.add()
        index = len(context.scene.ytyps)
        item.name = f"YTYP.{index}"
        context.scene.ytyp_index = index - 1


class SOLLUMZ_OT_delete_ytyp(SOLLUMZ_OT_base, bpy.types.Operator):
    """Delete a ytyp from the project"""
    bl_idname = "sollumz.deleteytyp"
    bl_label = "Delete YTYP"

    def run(self, context):
        context.scene.ytyps.remove(context.scene.ytyp_index)
        context.scene.ytyp_index = max(context.scene.ytyp_index - 1, 0)


class SOLLUMZ_OT_create_archetype(SOLLUMZ_OT_base, bpy.types.Operator):
    """Add an archetype to the selected ytyp"""
    bl_idname = "sollumz.createarchetype"
    bl_label = "Create Archetype"

    @classmethod
    def poll(cls, context):
        return len(context.scene.ytyps) > 0

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        item = selected_ytyp.archetypes.add()
        index = len(selected_ytyp.archetypes)
        item.name = f"{SOLLUMZ_UI_NAMES[ArchetypeType.BASE]}.{index}"
        context.scene.archetype_index = index - 1


class SOLLUMZ_OT_delete_archetype(SOLLUMZ_OT_base, bpy.types.Operator):
    """Delete archetype from selected ytyp"""
    bl_idname = "sollumz.deletearchetype"
    bl_label = "Delete Archetype"

    @classmethod
    def poll(cls, context):
        return len(context.scene.ytyps) > 0

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_ytyp.archetypes.remove(context.scene.archetype_index)
        context.scene.archetype_index = max(
            context.scene.archetype_index - 1, 0)


class SOLLUMZ_OT_create_room(SOLLUMZ_OT_base, bpy.types.Operator):
    """Add a room to the selected archetype"""
    bl_idname = "sollumz.createroom"
    bl_label = "Create Room"

    @classmethod
    def poll(cls, context):
        if len(context.scene.ytyps) > 0:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            return len(selected_ytyp.archetypes) > 0
        return False

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        item = selected_archetype.rooms.add()
        index = len(selected_archetype.rooms)
        item.name = f"Room.{index}"
        context.scene.room_index = index - 1


class SOLLUMZ_OT_set_bounds_from_selection(SOLLUMZ_OT_base, bpy.types.Operator):
    """Set room bounds from selection (must be in edit mode)"""
    bl_idname = "sollumz.setroomboundsfromselection"
    bl_label = "Set Bounds From Selection"

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == "EDIT"

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        selected_room = selected_archetype.rooms[context.scene.room_index]
        selected_verts = []
        for obj in context.objects_in_mode:
            selected_verts.extend(get_selected_vertices(obj))
        if not len(selected_verts) > 1:
            self.message("You must select at least 2 vertices!")
            return False
        if not selected_archetype.asset:
            self.message("You must set an asset for the archetype.")
            return False

        pos = selected_archetype.asset.location

        selected_room.bb_max = get_max_vector_list(
            selected_verts) - pos
        selected_room.bb_min = get_min_vector_list(
            selected_verts) - pos
        return True


class SOLLUMZ_OT_delete_room(SOLLUMZ_OT_base, bpy.types.Operator):
    """Delete room from selected archetype"""
    bl_idname = "sollumz.deleteroom"
    bl_label = "Delete Room"

    @classmethod
    def poll(cls, context):
        if len(context.scene.ytyps) > 0:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            return len(selected_ytyp.archetypes) > 0
        return False

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        selected_archetype.rooms.remove(context.scene.room_index)
        context.scene.room_index = max(context.scene.room_index - 1, 0)


class SOLLUMZ_OT_create_portal(SOLLUMZ_OT_base, bpy.types.Operator):
    """Add a portal to the selected archetype"""
    bl_idname = "sollumz.createportal"
    bl_label = "Create Portal"

    @classmethod
    def poll(cls, context):
        if len(context.scene.ytyps) > 0:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            return len(selected_ytyp.archetypes) > 0
        return False

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        item = selected_archetype.portals.add()
        index = len(selected_archetype.portals)
        item.name = f"Portal.{index}"
        context.scene.portal_index = index - 1


class SOLLUMZ_OT_create_portal_from_selection(SOLLUMZ_OT_base, bpy.types.Operator):
    """Create a portal from selected verts"""
    bl_idname = "sollumz.createportalfromselection"
    bl_label = "Create Portal From Verts"

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == "EDIT"

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        selected_verts = []

        for obj in context.objects_in_mode:
            selected_verts.extend(get_selected_vertices(obj))

        if len(selected_verts) != 4:
            self.message("You must select exactly 4 vertices.")
            return False

        if not selected_archetype.asset:
            self.message("You must select an asset.")
            return False

        corners = selected_verts
        corners.sort()

        pos = selected_archetype.asset.location
        new_portal = selected_archetype.portals.add()
        index = len(selected_archetype.portals)
        new_portal.name = f"Portal.{index}"
        context.scene.portal_index = index - 1
        new_portal.corner1 = corners[0] - pos
        new_portal.corner2 = corners[1] - pos
        new_portal.corner3 = corners[2] - pos
        new_portal.corner4 = corners[3] - pos

        return True


class SOLLUMZ_OT_delete_portal(SOLLUMZ_OT_base, bpy.types.Operator):
    """Delete portal from selected archetype"""
    bl_idname = "sollumz.deleteportal"
    bl_label = "Delete Portal"

    @classmethod
    def poll(cls, context):
        if len(context.scene.ytyps) > 0:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            return len(selected_ytyp.archetypes) > 0
        return False

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        selected_archetype.portals.remove(context.scene.portal_index)
        context.scene.portal_index = max(context.scene.portal_index - 1, 0)


class SOLLUMZ_OT_create_timecycle_modifier(SOLLUMZ_OT_base, bpy.types.Operator):
    """Add a timecycle modifier to the selected archetype"""
    bl_idname = "sollumz.createtimecyclemodifier"
    bl_label = "Create Timecycle Modifier"

    @classmethod
    def poll(cls, context):
        if len(context.scene.ytyps) > 0:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            return len(selected_ytyp.archetypes) > 0
        return False

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        item = selected_archetype.timecycle_modifiers.add()
        item.name = f"Timecycle Modifier.{len(selected_archetype.timecycle_modifiers)}"


class SOLLUMZ_OT_delete_timecycle_modifier(SOLLUMZ_OT_base, bpy.types.Operator):
    """Delete timecycle modifier from selected archetype"""
    bl_idname = "sollumz.deletetimecyclemodifier"
    bl_label = "Delete Timecycle Modifier"

    @classmethod
    def poll(cls, context):
        if len(context.scene.ytyps) > 0:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            return len(selected_ytyp.archetypes) > 0
        return False

    def run(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        selected_archetype.timecycle_modifiers.remove(context.scene.tcm_index)
        context.scene.tcm_index = max(context.scene.tcm_index - 1, 0)


class SOLLUMZ_OT_export_ymap(SOLLUMZ_OT_base, bpy.types.Operator):
    """Exports the selected YTYP."""
    bl_idname = "sollumz.exportytyp"
    bl_label = "Export ytyp.xml"
    bl_action = "Export a YTYP"

    filter_glob: bpy.props.StringProperty(
        default="*.ytyp.xml",
        options={'HIDDEN'},
        maxlen=255,
    )

    directory: bpy.props.StringProperty(
        name="Output directory",
        description="Select export output directory",
        subtype="DIR_PATH",
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    @classmethod
    def poll(cls, context):
        num_ytyps = len(context.scene.ytyps)
        return num_ytyps > 0 and context.scene.ytyp_index < num_ytyps

    def get_filepath(self, name):
        return os.path.join(self.directory, name + ".ytyp.xml")

    @staticmethod
    def init_archetype(arch_xml, arch):
        arch_xml.lod_dist = arch.lod_dist
        arch_xml.flags = arch.flags
        arch_xml.special_attribute = arch.special_attribute
        arch_xml.hd_texture_dist = arch.hd_texture_dist
        arch_xml.name = arch.name
        arch_xml.texture_dictionary = arch.texture_dictionary
        arch_xml.clip_dictionary = arch.clip_dictionary
        arch_xml.drawable_dictionary = arch.drawable_dictionary
        arch_xml.physics_dictionary = arch.physics_dictionary
        bbmin, bbmax = get_bound_extents(arch.asset, world=False)
        arch_xml.bb_min = bbmin
        arch_xml.bb_max = bbmax
        arch_xml.bs_center = get_bound_center(arch.asset, world=False)
        arch_xml.bs_radius = get_obj_radius(arch.asset, world=False)
        asset_type = arch.asset_type
        arch_xml.asset_name = arch.asset.name
        if asset_type == AssetType.UNITIALIZED:
            arch_xml.asset_type = "ASSET_TYPE_UNINITIALIZED"
        elif asset_type == AssetType.FRAGMENT:
            arch_xml.asset_type = "ASSET_TYPE_FRAGMENT"
        elif asset_type == AssetType.DRAWABLE:
            arch_xml.asset_type = "ASSET_TYPE_DRAWABLE"
        elif asset_type == AssetType.DRAWABLE_DICTIONARY:
            arch_xml.asset_type = "ASSET_TYPE_DRAWABLE_DICTIONARY"
        elif asset_type == AssetType.ASSETLESS:
            arch_xml.asset_type = "ASSET_TYPE_ASSETLESS"
        return arch_xml

    def run(self, context):
        try:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            ytyp = CMapTypes()
            ytyp.name = selected_ytyp.name
            for archetype in selected_ytyp.archetypes:
                archetype_xml = None
                if archetype.type == ArchetypeType.BASE:
                    archetype_xml = self.init_archetype(
                        BaseArchetype(), archetype)
                elif archetype.type == ArchetypeType.TIME:
                    archetype_xml = self.init_archetype(
                        TimeArchetype(), archetype)
                elif archetype.type == ArchetypeType.MLO:
                    archetype_xml = self.init_archetype(
                        MloArchetype(), archetype)
                    for room in archetype.rooms:
                        room_xml = Room()
                        room_xml.name = room.name
                        room_xml.bb_min = room.bb_min
                        room_xml.bb_max = room.bb_max
                        room_xml.blend = room.blend
                        room_xml.timecycle_name = room.timecycle
                        room_xml.secondary_timecycle_name = room.secondary_timecycle
                        room_xml.flags = room.flags
                        room_xml.floor_id = room.floor_id
                        room_xml.exterior_visibility_depth = room.exterior_visibility_depth
                        archetype_xml.rooms.append(room_xml)
                    for portal in archetype.portals:
                        portal_xml = Portal()

                        for i in range(4):
                            corner = portal[f"corner{i + 1}"]
                            corner_xml = Corner()
                            corner_xml.value = corner
                            portal_xml.corners.append(corner_xml)

                        portal_xml.room_from = portal.room_from
                        portal_xml.room_to = portal.room_to
                        portal_xml.flags = portal.flags
                        portal_xml.mirror_priority = portal.mirror_priority
                        portal_xml.opactity = portal.opacity
                        portal_xml.audio_occlusion = portal.audio_occlusion
                        archetype_xml.portals.append(portal_xml)
                else:
                    continue
                ytyp.archetypes.append(archetype_xml)
            filepath = self.get_filepath(ytyp.name)
            ytyp.write_xml(filepath)
            self.message(f"Successfully exported: {filepath}")
            return True
        except:
            self.error(f"Error during export: {traceback.format_exc()}")
            return False
