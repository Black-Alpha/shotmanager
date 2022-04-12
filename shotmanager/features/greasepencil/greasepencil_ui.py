# GPLv3 License
#
# Copyright (C) 2021 Ubisoft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
To do: module description here.
"""

# from shotmanager.utils import utils
from shotmanager.utils import utils_ui
from shotmanager.utils import utils_greasepencil


def draw_greasepencil_shot_properties(sm_ui, context, shot):
    layout = sm_ui.layout
    props = context.scene.UAS_shot_manager_props
    prefs = context.preferences.addons["shotmanager"].preferences
    scene = context.scene

    if shot is None:
        return

    propertiesModeStr = "Selected " if "SELECTED" == props.current_shot_properties_mode else "Current "
    hSepFactor = 0.5

    devDebug_displayAdv = config.devDebug and True

    gp_child = None
    if shot is not None:
        shotIndex = props.getShotIndex(shot)
        if shot.camera is None:
            pass
        else:
            gp_child = utils.get_greasepencil_child(shot.camera)

    panelIcon = "TRIA_DOWN" if prefs.shot_greasepencil_expanded and gp_child is not None else "TRIA_RIGHT"

    box = layout.box()
    box.use_property_decorate = False
    col = box.column()
    row = col.row(align=True)

    # grease pencil
    ################

    # if props.display_storyboard_in_properties:  # and props.expand_greasepencil_properties:
    #     gp.draw_greasepencil_play_tools(layout, context, shot, layersListDropdown=prefs.layersListDropdown)

    extendSubRow = row.row(align=True)
    extendSubRow.prop(prefs, "shot_greasepencil_expanded", text="", icon=panelIcon, emboss=False)
    # row.separator(factor=1.0)

    subRow = row.row(align=False)
    # subRow.scale_x = 0.6
    subRow.label(text="Grease Pencil:")

    if gp_child is None:
        extendSubRow.enabled = False
        row.operator(
            "uas_shot_manager.add_grease_pencil", text="", icon="ADD", emboss=True
        ).cameraGpName = shot.camera.name

        # subSubRow.separator(factor=1.0)
        row.prop(props, "display_greasepencil_in_shotlist", text="")
        # subSubRow.separator(factor=0.5)  # prevents stange look when panel is narrow

    else:
        subRow.label(text=gp_child.name)
        subRow.operator("uas_shot_manager.select_grease_pencil", text="", icon="RESTRICT_SELECT_OFF").index = shotIndex
        subSubRow = subRow.row(align=True)
        subSubRow.prop(gp_child, "hide_select", text="")
        subSubRow.prop(gp_child, "hide_viewport", text="")
        subSubRow.prop(gp_child, "hide_render", text="")

        subRow = row.row(align=True)
        subRow.operator("uas_shot_manager.remove_grease_pencil", text="", icon="PANEL_CLOSE").shotIndex = shotIndex
        subRow.separator()
        subRow.prop(props, "display_greasepencil_in_shotlist", text="")

        # name and visibility tools
        ################
        # extendSubRow.alignment = "EXPAND"

        subRow = col.row(align=False)
        # subRow.scale_x = 0.8
        leftSubRow = subRow.row(align=True)
        leftSubRow.alignment = "LEFT"
        leftSubRow.label(text="GP: ")
        leftSubRow.label(text=gp_child.name)

        rightSubRow = subRow.row(align=True)
        rightSubRow.alignment = "RIGHT"

        # Grease Pencil tools
        ################
        if devDebug_displayAdv:
            # subSubRow = rightSubRow.row()
            # subSubRow.alignment = "RIGHT"
            # gpToolsSplit = subSubRow.split(factor=0.4)
            # gpToolsRow = gpToolsSplit.row(align=True)

            gpToolsRow = rightSubRow
            gpToolsRow.alignment = "RIGHT"
            gpToolsRow.scale_x = 2
            gpToolsRow.operator(
                "uas_shot_manager.select_shot_grease_pencil", text="", icon="RESTRICT_SELECT_OFF"
            ).index = shotIndex

            if gp_child.mode == "PAINT_GPENCIL":
                icon = "GREASEPENCIL"
                gpToolsRow.alert = True
                gpToolsRow.operator("uas_shot_manager.toggle_grease_pencil_draw_mode", text="", icon=icon)
                gpToolsRow.alert = False
                # bpy.ops.gpencil.paintmode_toggle()
            else:
                gpToolsRow.operator("uas_shot_manager.draw_on_grease_pencil", text="", icon="OUTLINER_OB_GREASEPENCIL")

            gpToolsRow.operator(
                "uas_shot_manager.update_grease_pencil", text="", icon="FILE_REFRESH"
            ).shotIndex = shotIndex

        # distance ##############
        #############
        # subRow.alignment = "LEFT"
        # gpDistRow = gpToolsSplit.row(align=True)
        # gpDistRow.scale_x = 1.2
        # gpDistRow.use_property_split = True
        # gpDistRow.alignment = "RIGHT"
        # # gpDistRow.label(text="Distance:")
        # gpDistRow.prop(gpProperties, "distanceFromOrigin", text="Distance:", slider=True)

        # Debug settings
        ################
        if devDebug_displayAdv:
            subRow = box.row(align=False)
            leftSubRow = subRow.row(align=True)
            leftSubRow.alignment = "LEFT"

            rightSubRow = subRow.row(align=True)
            rightSubRow.alignment = "RIGHT"
            rightSubRow.prop(gp_child, "hide_select", text="")
            rightSubRow.prop(gp_child, "hide_viewport", text="")
            rightSubRow.prop(gp_child, "hide_render", text="")

        row = col.row()
        row.separator(factor=hSepFactor)

        row = col.row()

        canvasSplitRow = row.split(factor=0.3)
        utils_ui.collapsable_panel(canvasSplitRow, prefs, "stb_canvas_props_expanded", alert=False, text="Canvas")
        # canvasSplitRow.label(text=" ")
        # canvasSplitRow.separator(factor=0.1)

        canvasLayer = utils_greasepencil.get_grease_pencil_layer(
            gp_child, gpencil_layer_name="GP_Canvas", create_layer=False
        )
        if canvasLayer is None:
            # utils_greasepencil.get_grease_pencil_layer
            canvasSplitRow.operator("uas_shot_manager.add_canvas_to_grease_pencil", text="+").gpName = gp_child.name
        else:
            rightCanvasSplitRow = canvasSplitRow.row()
            rightCanvasSplitRow.prop(gpProperties, "canvasOpacity", slider=True, text="Opacity")
            rightCanvasSplitRow.prop(canvasLayer, "hide", text="")

        if prefs.stb_canvas_props_expanded:

            sepRow = col.row()
            sepRow.separator(factor=0.5)

            splitRow = col.split(factor=0.3)
            splitRow.label(text="   Size:")
            rightSplitRow = splitRow.row(align=True)
            # rightSplitRow.use_property_split = False
            # rightSplitRow.use_property_decorate = False
            rightSplitRow.prop(gpProperties, "canvasSize", text="", slider=True)

            splitRow = col.split(factor=0.3)
            # splitRow.separator(factor=2)
            splitRow.label(text="   Distance:")
            splitRow.prop(gpProperties, "distanceFromOrigin", text="", slider=True)

        # animation
        ################
        # panelIcon = "TRIA_DOWN" if prefs.stb_anim_props_expanded else "TRIA_RIGHT"
        animRow = col.row()
        utils_ui.collapsable_panel(
            animRow, prefs, "stb_anim_props_expanded", alert=False, text="Animate Frame Transformation"
        )
        if prefs.stb_anim_props_expanded:
            transformRow = col.row()
            transformRow.separator(factor=hSepFactor)
            # or prefs.shot_greasepencil_expanded:
            transformRow = col.row()
            # transformRow.label(text="Location:")
            transformRow.use_property_split = True
            transformRow.use_property_decorate = True
            transformRow.prop(gp_child, "location")

            transformRow = col.row()
            transformRow.use_property_split = True
            transformRow.use_property_decorate = True
            transformRow.prop(gp_child, "rotation_euler")

            transformRow = col.row()
            transformRow.use_property_split = True
            transformRow.use_property_decorate = True
            transformRow.prop(gp_child, "scale")

            # transformRow = col.row()
            # transformRow.label(text="test")
            # transformRow.use_property_split = True
            # transformRow.use_property_decorate = True
            # transformRow.prop(gp_child.location, "x")

            transformRow = col.row()
            transformRow.separator(factor=0.6)
            transformRow = col.row(align=True)
            transformRow.separator(factor=5)
            transformRowSplit = transformRow.split(factor=0.32)
            # transformRow.alignment = "RIGHT"
            # transformRow.ui_units_x = 2
            transformRowSplit.label(text="Motion Path:")
            if gp_child.motion_path is None:
                transformRowSplit.operator("object.paths_calculate", text="Calculate...", icon="OBJECT_DATA")
            else:
                transformRowSplitRow = transformRowSplit.row()
                # transformRow.operator("object.paths_update", text="Update Paths", icon="OBJECT_DATA")
                transformRowSplitRow.operator("object.paths_update_visible", text="Update All Paths", icon="WORLD")
                transformRowSplitRow.operator("object.paths_clear", text="", icon="X")

            row = col.row()
            row.separator(factor=0.4)

        # row = col.row()
        # row.separator(factor=0.5)

    # row = box.row()
    # row.operator("uas_shot_manager.change_grease_pencil_opacity").gpObjectName = gp_child
