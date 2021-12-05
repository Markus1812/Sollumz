import bpy
from ..sollumz_properties import SollumType, ArchetypeType
from .properties import Room, Portal, TimecycleModifier


class SOLLUMZ_UL_YTYP_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_YTYP_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # If the object is selected
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

    def draw(self, context):
        layout = self.layout
        # layout.use_property_split = True
        layout.label(text="YTYPS")
        layout.template_list(
            SOLLUMZ_UL_YTYP_LIST.bl_idname, "", context.scene, "ytyps", context.scene, "ytyp_index"
        )
        row = layout.row()
        row.operator("sollumz.createytyp")
        row.operator("sollumz.deleteytyp")


class SOLLUMZ_UL_ARCHETYPE_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_ARCHETYPE_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # If the object is selected
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
                             selected_ytyp, "archetypes", context.scene, "archetype_index")
        row = layout.row()
        row.operator("sollumz.createarchetype")
        row.operator("sollumz.deletearchetype")


class SOLLUMZ_UL_ROOM_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_ROOM_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # If the object is selected
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
        # If the object is selected
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            row = layout.row()
            row.label(text=item.name, icon="OUTLINER_OB_LIGHTPROBE")
        elif self.layout_type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.prop(item, "name",
                        text=item.name, emboss=False, icon="OUTLINER_OB_LIGHTPROBE")


class SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST(bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST"

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        # If the object is selected
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
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]
        layout.prop(selected_archetype, "type")
        layout.prop(selected_archetype, "name")
        layout.prop(selected_archetype, "flags")
        layout.prop(selected_archetype, "special_attribute")
        layout.prop(selected_archetype, "texture_dictionary")
        layout.prop(selected_archetype, "clip_dictionary")
        layout.prop(selected_archetype, "drawable_dictionary")
        layout.prop(selected_archetype, "physics_dictionary")
        layout.prop(selected_archetype, "asset_type")
        layout.prop(selected_archetype, "asset")
        if selected_archetype.type == ArchetypeType.TIME:
            layout.prop(selected_archetype, "time_flags")
        if selected_archetype.type == ArchetypeType.MLO:
            layout.prop(selected_archetype, "mlo_flags")
            layout.separator()


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
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]

        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]

        layout.template_list(SOLLUMZ_UL_ROOM_LIST.bl_idname, "",
                             selected_archetype, "rooms", context.scene, "room_index")
        row = layout.row()
        row.operator("sollumz.createroom")
        row.operator("sollumz.deleteroom")
        layout.separator()

        if len(selected_archetype.rooms) > 0:
            selected_room = selected_archetype.rooms[context.scene.room_index]
            for prop_name in Room.__annotations__:
                layout.prop(selected_room, prop_name)


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
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]

        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]

        layout.template_list(SOLLUMZ_UL_PORTAL_LIST.bl_idname, "",
                             selected_archetype, "portals", context.scene, "portal_index")
        row = layout.row()
        row.operator("sollumz.createportal")
        row.operator("sollumz.deleteportal")

        layout.separator()

        if len(selected_archetype.portals) > 0:
            selected_portal = selected_archetype.portals[context.scene.portal_index]

            for prop_name in Portal.__annotations__:
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
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]

        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        selected_ytyp = context.scene.ytyps[context.scene.ytyp_index]
        selected_archetype = selected_ytyp.archetypes[context.scene.archetype_index]

        layout.template_list(SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST.bl_idname, "",
                             selected_archetype, "timecycle_modifiers", context.scene, "tcm_index")
        row = layout.row()
        row.operator("sollumz.createtimecyclemodifier")
        row.operator("sollumz.deletetimecyclemodifier")

        layout.separator()

        if len(selected_archetype.timecycle_modifiers) > 0:
            selected_tcm = selected_archetype.timecycle_modifiers[context.scene.tcm_index]
            for prop_name in TimecycleModifier.__annotations__:
                layout.prop(selected_tcm, prop_name)
