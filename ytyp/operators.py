import bpy
from ..sollumz_helper import SOLLUMZ_OT_base
from ..sollumz_properties import SOLLUMZ_UI_NAMES, ArchetypeType


class SOLLUMZ_OT_create_ytyp(SOLLUMZ_OT_base, bpy.types.Operator):
    """Add a ytyp to the project"""
    bl_idname = "sollumz.createytyp"
    bl_label = "Create YTYP"

    def run(self, context):
        item = context.scene.ytyps.add()
        item.name = f"YTYP.{len(context.scene.ytyps)}"


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
        item.name = f"{SOLLUMZ_UI_NAMES[ArchetypeType.BASE]}.{len(selected_ytyp.archetypes)}"


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
        item.name = f"Room.{len(selected_archetype.rooms)}"


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
        item.name = f"Portal.{len(selected_archetype.rooms)}"


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
        item.name = f"Timecycle Modifier.{len(selected_archetype.rooms)}"


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
