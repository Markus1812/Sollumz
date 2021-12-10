import bpy

from ..tools.meshhelper import get_children_recursive
from ..sollumz_properties import ArchetypeType
from .properties import RoomProperties, PortalProperties, TimecycleModifierProperties
from mathutils import Vector


def can_draw_gizmos(context):
    num_ytyps = len(context.scene.ytyps)
    if num_ytyps > 0 and context.scene.ytyp_index < num_ytyps:
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        num_archtypes = len(selected_ytyp.archetypes)
        if num_archtypes > 0 and selected_ytyp.archetype_index < num_archtypes:
            selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
            return selected_archetype.asset and selected_archetype.type == ArchetypeType.MLO and (context.active_object in get_children_recursive(selected_archetype.asset) or context.active_object == selected_archetype.asset)
    return False


class SOLLUMZ_UL_YTYP_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_YTYP_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            row.label(text=item.name, icon="PRESET")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.prop(item, "name",
                        text=item.name, emboss=False, icon="PRESET")


class SOLLUMZ_PT_YTYP_TOOL_PANEL(bpy.types.Panel):
    bl_label = "Archetype Definition"
    bl_idname = "SOLLUMZ_PT_YTYP_TOOL_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = "Sollumz Tools"

    def draw_header(self, context):
        self.layout.label(text="", icon="OBJECT_DATA")

    def draw(self, context):
        layout = self.layout
        layout.label(text="YTYPS")
        layout.template_list(
            SOLLUMZ_UL_YTYP_LIST.bl_idname, "", context.scene, "ytyps", context.scene, "ytyp_index"
        )
        row = layout.row()
        row.operator("sollumz.createytyp")
        row.operator("sollumz.deleteytyp")
        row = layout.row()
        row.operator("sollumz.importytyp")
        row.operator("sollumz.exportytyp")


class SOLLUMZ_UL_ARCHETYPE_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_ARCHETYPE_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            row.label(text=item.name, icon="OBJECT_DATA")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.prop(item, "name",
                        text=item.name, emboss=False, icon="OBJECT_DATA")


class SOLLUMZ_PT_YTYP_PANEL(bpy.types.Panel):
    bl_label = "YTYP"
    bl_idname = "SOLLUMZ_PT_YTYP_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = SOLLUMZ_PT_YTYP_TOOL_PANEL.bl_idname

    @classmethod
    def poll(cls, context):
        return len(context.scene.ytyps) > 0

    def draw(self, context):
        layout = self.layout
        # layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        layout.prop(selected_ytyp, "name")
        layout.label(text="Archetypes:")
        layout.template_list(SOLLUMZ_UL_ARCHETYPE_LIST.bl_idname, "",
                             selected_ytyp, "archetypes", selected_ytyp, "archetype_index")
        row = layout.row()
        row.operator("sollumz.createarchetype")
        row.operator("sollumz.deletearchetype")


class SOLLUMZ_UL_ROOM_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_ROOM_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            row.label(text=item.name, icon="CUBE")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.prop(item, "name",
                        text=item.name, emboss=False, icon="CUBE")


class SOLLUMZ_UL_PORTAL_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_PORTAL_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        portal_index = list(selected_archetype.portals).index(item)
        name = f"{portal_index}: {item.room_from} to {item.room_to}"
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            row.label(text=name, icon="OUTLINER_OB_LIGHTPROBE")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.prop(item, "name",
                        text=name, emboss=False, icon="OUTLINER_OB_LIGHTPROBE")


class SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            row.label(text=item.name, icon="TIME")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.prop(item, "name",
                        text=item.name, emboss=False, icon="TIME")


class SOLLUMZ_PT_ARCHETYPE_PANEL(bpy.types.Panel):
    bl_label = "Archetype"
    bl_idname = "SOLLUMZ_PT_ARCHETYPE_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = SOLLUMZ_PT_YTYP_PANEL.bl_idname

    @classmethod
    def poll(cls, context):
        num_ytyps = len(context.scene.ytyps)
        if num_ytyps > 0 and context.scene.ytyp_index < num_ytyps:
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            return len(selected_ytyp.archetypes) > 0
        return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        layout.prop(selected_archetype, "type")
        layout.prop(selected_archetype, "name")
        layout.prop(selected_archetype, "flags")
        layout.prop(selected_archetype, "special_attribute")
        layout.prop(selected_archetype, "texture_dictionary")
        layout.prop(selected_archetype, "clip_dictionary")
        layout.prop(selected_archetype, "drawable_dictionary")
        layout.prop(selected_archetype, "physics_dictionary")
        layout.prop(selected_archetype, "asset_type")
        layout.prop(data=selected_archetype,
                    property="asset_name", text="Asset Name")
        if selected_archetype.asset_name and not selected_archetype.asset:
            row = layout.row()
            row.alignment = "RIGHT"
            layout.separator()
            row.label(text="Asset not found in scene",
                      icon="ERROR")
        if selected_archetype.type == ArchetypeType.TIME:
            layout.prop(selected_archetype, "time_flags")
        if selected_archetype.type == ArchetypeType.MLO:
            layout.prop(selected_archetype, "mlo_flags")
            layout.separator()


class RoomGizmo(bpy.types.Gizmo):
    bl_idname = "OBJECT_GT_room"

    def __init__(self):
        super().__init__()
        self.linked_room = None

    @staticmethod
    def get_verts(bbmin, bbmax):
        return [
            bbmin,
            Vector((bbmin.x, bbmin.y, bbmax.z)),

            bbmin,
            Vector((bbmax.x, bbmin.y, bbmin.z)),

            bbmin,
            Vector((bbmin.x, bbmax.y, bbmin.z)),

            Vector((bbmax.x, bbmin.y, bbmax.z)),
            Vector((bbmax.x, bbmin.y, bbmin.z)),

            Vector((bbmin.x, bbmin.y, bbmax.z)),
            Vector((bbmin.x, bbmax.y, bbmax.z)),

            Vector((bbmin.x, bbmax.y, bbmin.z)),
            Vector((bbmin.x, bbmax.y, bbmax.z)),

            Vector((bbmax.x, bbmin.y, bbmax.z)),
            Vector((bbmax.x, bbmin.y, bbmax.z)),

            Vector((bbmax.x, bbmin.y, bbmax.z)),
            Vector((bbmin.x, bbmin.y, bbmax.z)),

            Vector((bbmax.x, bbmin.y, bbmin.z)),
            Vector((bbmax.x, bbmax.y, bbmin.z)),

            Vector((bbmin.x, bbmax.y, bbmin.z)),
            Vector((bbmax.x, bbmax.y, bbmin.z)),

            Vector((bbmax.x, bbmin.y, bbmax.z)),
            bbmax,

            Vector((bbmin.x, bbmax.y, bbmax.z)),
            bbmax,

            Vector((bbmax.x, bbmax.y, bbmin.z)),
            bbmax
        ]

    def draw(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        selected_room = selected_archetype.rooms[selected_archetype.room_index]
        room = self.linked_room

        self.color = 0.31, 0.38, 1
        self.alpha = 0.7
        self.use_draw_scale = False

        if room == selected_room:
            self.color = self.color * 2
            self.alpha = 0.9

        asset = selected_archetype.asset
        if asset and room:
            self.custom_shape = self.new_custom_shape(
                "LINES", RoomGizmo.get_verts(room.bb_min, room.bb_max))
            self.draw_custom_shape(
                self.custom_shape, matrix=asset.matrix_world)


class RoomGizmoGroup(bpy.types.GizmoGroup):
    bl_idname = "OBJECT_GGT_Room"
    bl_label = "MLO Room"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT'}

    @classmethod
    def poll(cls, context):
        if can_draw_gizmos(context):
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
            return selected_archetype.room_index < len(selected_archetype.rooms)
        return False

    def setup(self, context):
        pass

    def draw_prepare(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        self.gizmos.clear()
        for room in selected_archetype.rooms:
            gz = self.gizmos.new(RoomGizmo.bl_idname)
            gz.linked_room = room


class PortalGizmo(bpy.types.Gizmo):
    bl_idname = "OBJECT_GT_portal"

    def __init__(self):
        super().__init__()
        self.linked_portal = None

    @staticmethod
    def get_verts(corners):
        return [
            corners[0],
            corners[1],
            corners[2],

            corners[3],
            corners[2],
            corners[1],
        ]

    def draw(self, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
        selected_portal = selected_archetype.portals[selected_archetype.portal_index]
        portal = self.linked_portal
        asset = selected_archetype.asset

        self.color = 0.45, 0.98, 0.55
        self.alpha = 0.5

        if selected_portal == portal:
            self.color = self.color * 1.5
            self.alpha = 0.7

        if portal and asset:
            corners = [portal.corner1, portal.corner2,
                       portal.corner3, portal.corner4]
            self.custom_shape = self.new_custom_shape(
                "TRIS", PortalGizmo.get_verts(corners))
            self.draw_custom_shape(
                self.custom_shape, matrix=asset.matrix_world)


class PortalGizmoGroup(bpy.types.GizmoGroup):
    bl_idname = "OBJECT_GGT_Portal"
    bl_label = "MLO Portal"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SELECT'}

    @classmethod
    def poll(cls, context):
        if can_draw_gizmos(context):
            selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
            selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]
            return selected_archetype.portal_index < len(selected_archetype.portals)
        return False

    def setup(self, context):
        pass

    def draw_prepare(self, context):
        self.gizmos.clear()
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]

        for portal in selected_archetype.portals:
            gz = self.gizmos.new(PortalGizmo.bl_idname)
            gz.linked_portal = portal


class SOLLUMZ_PT_ROOM_PANEL(bpy.types.Panel):
    bl_label = "Rooms"
    bl_idname = "SOLLUMZ_PT_ROOM_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = SOLLUMZ_PT_ARCHETYPE_PANEL.bl_idname
    bl_order = 0

    @classmethod
    def poll(cls, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]

        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]

        layout.template_list(SOLLUMZ_UL_ROOM_LIST.bl_idname, "",
                             selected_archetype, "rooms", selected_archetype, "room_index")
        row = layout.row()
        row.operator("sollumz.createroom")
        row.operator("sollumz.deleteroom")
        row = layout.row()
        row.use_property_split = False
        row.prop(context.scene, "show_room_gizmo")
        layout.separator()

        if len(selected_archetype.rooms) > 0:
            selected_room = selected_archetype.rooms[selected_archetype.room_index]
            for prop_name in RoomProperties.__annotations__:
                layout.prop(selected_room, prop_name)
            layout.separator()
            layout.operator("sollumz.setroomboundsfromselection")


class SOLLUMZ_PT_PORTAL_PANEL(bpy.types.Panel):
    bl_label = "Portals"
    bl_idname = "SOLLUMZ_PT_PORTAL_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = SOLLUMZ_PT_ARCHETYPE_PANEL.bl_idname
    bl_order = 1

    @classmethod
    def poll(cls, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        if selected_ytyp.archetype_index < len(selected_ytyp.archetypes):
            selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]

            return selected_archetype.type == ArchetypeType.MLO
        return False

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]

        layout.template_list(SOLLUMZ_UL_PORTAL_LIST.bl_idname, "",
                             selected_archetype, "portals", selected_archetype, "portal_index")
        row = layout.row()
        row.operator("sollumz.createportal")
        row.operator("sollumz.deleteportal")
        row = layout.row()
        row.operator("sollumz.createportalfromselection")
        row = layout.row()
        row.use_property_split = False
        row.prop(context.scene, "show_portal_gizmo")

        layout.separator()

        if len(selected_archetype.portals) > 0:
            selected_portal = selected_archetype.portals[selected_archetype.portal_index]

            for prop_name in PortalProperties.__annotations__:
                layout.prop(selected_portal, prop_name)


class SOLLUMZ_PT_TIMECYCLE_MODIFIER_PANEL(bpy.types.Panel):
    bl_label = "Timecycle Modifiers"
    bl_idname = "SOLLUMZ_PT_TIMECYCLE_MODIFIER_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = SOLLUMZ_PT_ARCHETYPE_PANEL.bl_idname
    bl_order = 2

    @classmethod
    def poll(cls, context):
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]

        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[selected_ytyp.archetype_index]

        layout.template_list(SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST.bl_idname, "",
                             selected_archetype, "timecycle_modifiers", selected_archetype, "tcm_index")
        row = layout.row()
        row.operator("sollumz.createtimecyclemodifier")
        row.operator("sollumz.deletetimecyclemodifier")

        layout.separator()

        if len(selected_archetype.timecycle_modifiers) > 0:
            selected_tcm = selected_archetype.timecycle_modifiers[selected_archetype.tcm_index]
            for prop_name in TimecycleModifierProperties.__annotations__:
                layout.prop(selected_tcm, prop_name)
