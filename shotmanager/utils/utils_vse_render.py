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
VSE
"""

import os
from pathlib import Path

import bpy

from bpy.types import Operator, PropertyGroup
from bpy.props import (
    IntVectorProperty,
    StringProperty,
    PointerProperty,
)

from ..config import config
from ..utils import utils

from shotmanager.config import sm_logging

_logger = sm_logging.getLogger(__name__)


# # ------------------------------------------------------------------------#
# #                                VSE tool Panel                             #
# # ------------------------------------------------------------------------#
# class UAS_PT_VSERender(Panel):
#     bl_idname = "UAS_PT_VSE_Render"
#     bl_label = "VSE Render"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "UAS VSE"
#     #  bl_options      = {'DEFAULT_CLOSED'}

#     def draw(self, context):
#         layout = self.layout

#         row = layout.row()
#         #     row.prop(scene.UAS_SM_StampInfo_Settings, "debugMode")

#         row = layout.row(align=True)
#         row.separator(factor=3)
#         # if not props.isRenderRootPathValid():
#         #     row.alert = True
#         row.prop(context.window_manager.UAS_vse_render, "inputOverMediaPath")
#         row.alert = False
#         row.operator("uasvse.openfilebrowser", text="", icon="FILEBROWSER", emboss=True).pathProp = "inputOverMediaPath"
#         row.separator()

#         row = layout.row(align=True)
#         row.prop(context.window_manager.UAS_vse_render, "inputOverResolution")

#         #    row.operator ( "uas_shot_manager.render_openexplorer", text="", icon='FILEBROWSER').path = props.renderRootPath
#         layout.separator()

#         row = layout.row(align=True)
#         row.separator(factor=3)
#         # if not props.isRenderRootPathValid():
#         #     row.alert = True
#         row.prop(context.window_manager.UAS_vse_render, "inputBGMediaPath")
#         row.alert = False
#         row.operator("uasvse.openfilebrowser", text="", icon="FILEBROWSER", emboss=True).pathProp = "inputBGMediaPath"
#         row.separator()

#         row = layout.row(align=True)
#         row.prop(context.window_manager.UAS_vse_render, "inputBGResolution")

#         layout.separator()
#         row = layout.row()

#         row.label(text="Render:")
#         #     row.prop(scene.UAS_SM_StampInfo_Settings, "debug_DrawTextLines")
#         # #    row.prop(scene.UAS_SM_StampInfo_Settings, "offsetToCenterHNorm")

#         #     row = layout.row()
#         row.operator("vse.compositevideoinvse", emboss=True)
#         # row.prop ( context.window_manager, "UAS_shot_manager_shots_play_mode",

#         #     row = layout.row()
#         #     row.operator("debug.lauchrrsrender", emboss=True)

#         #     if not utils_render.isRenderPathValid(context.scene):
#         #         row = layout.row()
#         #         row.alert = True
#         #         row.label( text = "Invalid render path")

#         #     row = layout.row()
#         #     row.operator("debug.createcomponodes", emboss=True)
#         #     row.operator("debug.clearcomponodes", emboss=True)

#         row = layout.row()
#         row.operator("uas_utils.run_script").path = "//../api/api_first_steps.py"


# This operator requires   from bpy_extras.io_utils import ImportHelper
# See https://sinestesia.co/blog/tutorials/using-blenders-filebrowser-with-python/
class UAS_VSE_OpenFileBrowser(Operator):  # from bpy_extras.io_utils import ImportHelper
    bl_idname = "uasvse.openfilebrowser"
    bl_label = "Open"
    bl_description = (
        "Open the file browser to define the image to stamp\n"
        "Relative path must be set directly in the text field and must start with ''//''"
    )

    pathProp: StringProperty()

    filepath: StringProperty(subtype="FILE_PATH")

    filter_glob: StringProperty(default="*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.tga;*.mp4", options={"HIDDEN"})

    def execute(self, context):
        """Use the selected file as a stamped logo"""
        filename, extension = os.path.splitext(self.filepath)
        #   print('Selected file:', self.filepath)
        #   print('File name:', filename)
        #   print('File extension:', extension)
        context.window_manager.UAS_vse_render[self.pathProp] = self.filepath

        return {"FINISHED"}

    def invoke(self, context, event):  # See comments at end  [1]

        if self.pathProp in context.window_manager.UAS_vse_render:
            self.filepath = context.window_manager.UAS_vse_render[self.pathProp]
        else:
            self.filepath = ""
        # https://docs.blender.org/api/current/bpy.types.WindowManager.html
        #    self.directory = bpy.context.scene.UAS_shot_manager_props.renderRootPath
        context.window_manager.fileselect_add(self)

        return {"RUNNING_MODAL"}


class ShotManager_Vse_Render(PropertyGroup):
    def get_inputOverMediaPath(self):
        val = self.get("inputOverMediaPath", "")
        return val

    def set_inputOverMediaPath(self, value):
        self["inputOverMediaPath"] = value

    inputOverMediaPath: StringProperty(
        name="Input Media Path Over", get=get_inputOverMediaPath, set=set_inputOverMediaPath, default=""
    )

    inputOverResolution: IntVectorProperty(size=2, default=(1280, 720))

    def get_inputBGMediaPath(self):
        val = self.get("inputBGMediaPath", "")
        return val

    def set_inputBGMediaPath(self, value):
        self["inputBGMediaPath"] = value

    inputBGMediaPath: StringProperty(
        name="Input Media Path BG", get=get_inputBGMediaPath, set=set_inputBGMediaPath, default=""
    )

    inputBGResolution: IntVectorProperty(size=2, default=(1280, 960))

    inputAudioMediaPath: StringProperty(name="Input Audio Media Path", default="")

    # resolution of the output media (usually the Over media res since it can be bigger when using StampInfo)
    outputResolution: IntVectorProperty(size=2, default=(1280, 720))

    outputMediaPath: StringProperty(name="Output Media Path", default="")

    def printMedia(self):
        mediaStr = "\nShot Manager: VSE_Render current media:\n"
        mediaStr += f"   - inputOverMediaPath:  '{self.inputOverMediaPath}'\n"
        mediaStr += "   - inputOverResolution: "
        mediaStr += (
            "None"
            if self.inputOverResolution is None
            else f"{self.inputOverResolution[0]} x {self.inputOverResolution[1]}"
        ) + f"  {self.inputOverResolution}\n"

        mediaStr += f"   - inputBGMediaPath:    '{self.inputBGMediaPath}'\n"
        mediaStr += "   - inputBGResolution:   "
        mediaStr += (
            "None" if self.inputBGResolution is None else f"{self.inputBGResolution[0]} x {self.inputBGResolution[1]}"
        ) + f"  {self.inputBGResolution}\n"

        mediaStr += f"   - inputAudioMediaPath: '{self.inputAudioMediaPath}'\n"
        mediaStr += f"   - outputMediaPath:     '{self.outputMediaPath}'\n"
        # mediaStr += "\n"

        _YELLOW = "\33[33m"
        _ENDCOLOR = "\033[0m"
        print(f"{_YELLOW}{mediaStr}{_ENDCOLOR}")

        # if bg_file is not None:
        #     self.inputBGMediaPath = bg_file
        # if bg_res is not None:
        #     self.inputBGResolution = bg_res

        # if fg_file is not None:
        #     self.inputOverMediaPath = fg_file
        # if fg_res is not None:
        #     self.inputOverResolution = fg_res

        # if audio_file is not None:
        #     self.inputAudioMediaPath = audio_file

    def clearMedia(self):
        self.inputOverMediaPath = ""
        self.inputOverResolution = (-1, -1)

        self.inputBGMediaPath = ""
        self.inputBGResolution = (-1, -1)

        self.inputAudioMediaPath = ""

    def getMediaList(self, scene, listVideo=True, listAudio=True):
        """Return the list of the media used in the VSE
        Return a dictionary made of "media_video" and "media_audio", both having an array of media filepaths
        Movies are not listed in audio media !
        """
        mediaList = {"media_video": None, "media_audio": None}
        audioFiles = []
        videoFiles = []
        for seq in scene.sequence_editor.sequences:
            mediaPath = self.getClipMediaPath(scene, seq)
            # print("  mediaPath: ", mediaPath)
            mediaType = self.getMediaType(mediaPath)
            # print("  mediaType: ", mediaType)
            if listAudio:
                if "SOUND" == mediaType:
                    if mediaPath not in audioFiles:
                        audioFiles.append(mediaPath)
            if listVideo:
                if "MOVIE" == mediaType:
                    if mediaPath not in videoFiles:
                        videoFiles.append(mediaPath)
        if listAudio:
            mediaList["media_audio"] = audioFiles
        if listVideo:
            mediaList["media_video"] = videoFiles

        return mediaList

    def getClipMediaPath(self, scene, clip):
        mediaPath = None
        # print(f"  clip: {clip.name}, type: {clip.type}")
        if "SOUND" == clip.type:
            # if clip.name in bpy.data.sounds:
            #     mediaPath = bpy.data.sounds[clip.name].filepath
            # elif clip.name in bpy.context.scene.sequence_editor.sequences_all:
            #     mediaPath = bpy.context.scene.sequence_editor.sequences_all[clip.name].filepath
            mediaPath = bpy.context.scene.sequence_editor.sequences[clip.name].sound.filepath

        elif "MOVIE" == clip.type:
            mediaPath = bpy.context.scene.sequence_editor.sequences_all[clip.name].filepath

        return bpy.path.abspath(mediaPath)

    def getMediaType(self, filePath):
        """Return the type of media according to the extension of the provided file path
        Rturned types: 'MOVIE', 'IMAGES_SEQUENCE', 'IMAGE', 'SOUND', 'UNKNOWN'
        """
        mediaType = "UNKNOWN"

        mediaExt = Path(filePath.lower()).suffix
        if mediaExt in (".mp4", ".avi", ".mov", ".mkv"):
            mediaType = "MOVIE"
        elif mediaExt in (".exr", ".jpg", ".jpeg", ".png", ".tga", ".tif", ".tiff"):
            # wkipwkipwkipwkip
            # if -1 != filePath.find("###"):
            if -1 != filePath.find("#"):
                mediaType = "IMAGES_SEQUENCE"
            else:
                mediaType = "IMAGE"
        elif mediaExt in (".mp3", ".wav", ".aif", ".aiff"):
            mediaType = "SOUND"
        return mediaType

    # a clip is called a sequence in VSE
    def createNewClipFromRange(
        self,
        scene,
        mediaPath,
        channelInd=1,
        frame_start=0,
        frame_final_start=0,
        frame_final_end=0,
        cameraScene=None,
        cameraObject=None,
        clipName="",
        importVideo=True,
        importAudio=False,
    ):

        atFrame = frame_start

        if importVideo:
            newClip = self.createNewClip(
                scene,
                mediaPath,
                200,
                atFrame,
                offsetStart=0,
                offsetEnd=0,
                cameraScene=cameraScene,
                cameraObject=cameraObject,
                clipName=clipName,
                importVideo=True,
                importAudio=False,
            )

            try:
                newClip.frame_final_end = frame_final_end
                newClip.frame_final_start = frame_final_start
                print(f"*** newClip video .frame_start: {newClip.frame_start}")

                newClip.channel = channelInd
            except Exception as e:
                _logger.error(f"*** Cannot create new clip: {e}")

        if importAudio:
            newClip = self.createNewClip(
                scene,
                mediaPath,
                201,
                atFrame,
                offsetStart=0,
                offsetEnd=0,
                cameraScene=cameraScene,
                cameraObject=cameraObject,
                clipName=clipName,
                importVideo=False,
                importAudio=True,
            )

            print(f"  02 at frame: {atFrame}")
            newClip.frame_start = atFrame
            print(f"*** newClip audio .frame_start: {newClip.frame_start}")

            newClip.frame_final_end = frame_final_end
            newClip.frame_final_start = frame_final_start
            newClip.channel = channelInd + 1

        return newClip

    # a clip is called a sequence in VSE
    def createNewClip(
        self,
        scene,
        mediaPath,
        channelInd=1,
        atFrame=0,
        offsetStart=0,
        offsetEnd=0,
        final_duration=-1,
        cameraScene=None,
        cameraObject=None,
        clipName="",
        importVideo=True,
        importAudio=False,
    ):
        """
        A strip is placed at a specified time in the edit by putting its media start at the place where
        it will be, in an absolute approach, and then by changing the handles of the clip with offsetStart
        and offsetEnd. None of these parameters change the position of the media frames in the edit time (it
        is like changing the position of the sides of a window, but not what the window sees).
        Both offsetStart and offsetEnd are relative to the start time of the media.
        audio_volume_keyframes is a list of paired values (Frame, Value)
        """

        def _new_camera_sequence(
            scene, name, channelInd, atFrame, offsetStart, offsetEnd, cameraScene, cameraObject, final_duration=-1
        ):
            """Create the camera sequence"""
            # !!! When the 3D scence range is not starting at zero the camera strip is clipped at the begining...
            # OriRangeStart = cameraScene.frame_start
            # OriRangeEnd = cameraScene.frame_end
            cameraScene.frame_start = 0
            cameraScene.frame_end = offsetEnd

            camSeq = scene.sequence_editor.sequences.new_scene(name, cameraScene, channelInd, atFrame)
            camSeq.scene_camera = cameraObject
            camSeq.frame_offset_start = offsetStart
            camSeq.frame_offset_end = 0

            # code not tested...
            if -1 != final_duration:
                camSeq.frame_final_duration = final_duration
            # cameraScene.frame_start = OriRangeStart
            # cameraScene.frame_end = OriRangeEnd

            return camSeq

        def _new_images_sequence(scene, clipName, images_path, channelInd, atFrame):
            """Find the name template for the specified images sequence in order to create it"""
            import re
            from pathlib import Path

            seq = None
            p = Path(images_path)
            folder, name = p.parent, str(p.name)

            mov_name = ""
            # Find frame padding. Either using # formating or printf formating
            file_re = ""
            padding_match = re.match(".*?(#+).*", name)
            if not padding_match:
                padding_match = re.match(".*?%(\d\d)d.*", name)
                if padding_match:
                    padding_length = int(padding_match[1])
                    file_re = re.compile(
                        r"^{1}({0}){2}$".format(
                            "\d" * padding_length, name[: padding_match.start(1) - 1], name[padding_match.end(1) + 1 :]
                        )
                    )
                    mov_name = (
                        str(p.stem)[: padding_match.start(1) - 1] + str(p.stem)[padding_match.end(1) + 1 :]
                    )  # Removes the % and d which are not captured in the re.
            else:
                padding_length = len(padding_match[1])
                file_re = re.compile(
                    r"^{1}({0}){2}$".format(
                        "\d" * padding_length, name[: padding_match.start(1)], name[padding_match.end(1) :]
                    )
                )
                mov_name = str(p.stem)[: padding_match.start(1)] + str(p.stem)[padding_match.end(1) :]

            if padding_match:
                # scene.render.filepath = str(folder.joinpath(mov_name))

                frames = dict()
                max_frame = 0
                min_frame = 999999999
                for f in sorted(list(folder.glob("*"))):
                    _folder, _name = f.parent, f.name
                    re_match = file_re.match(_name)
                    if re_match:
                        frame_nb = int(re_match[1])
                        max_frame = max(max_frame, frame_nb)
                        min_frame = min(min_frame, frame_nb)

                        frames[frame_nb] = f

                frame_keys = list(frames.keys())  # As of python 3.7 should be in the insertion order.
                if frames:
                    seq = scene.sequence_editor.sequences.new_image(
                        clipName, str(frames[frame_keys[0]]), channelInd, atFrame
                    )

                    for i in range(min_frame + 1, max_frame + 1):
                        pp = frames.get(i, Path(""))
                        seq.elements.append(pp.name)

                #   scene.frame_end = max_frame - min_frame + 1

            return seq

        ########################################################################
        ########################################################################

        trackType = (
            "ALL" if importVideo and importAudio else ("VIDEO" if importVideo else ("AUDIO" if importAudio else "NONE"))
        )

        # Clip creation
        ##########

        newClip = None
        mediaType = self.getMediaType(mediaPath)
        # print(f"Media type:{mediaType}, media:{mediaPath}")
        if "UNKNOWN" == mediaType:
            if cameraScene is not None and cameraObject is not None:
                mediaType = "CAMERA"

        if "MOVIE" == mediaType:
            newClipName = clipName if "" != clipName else "myMovie"
            audioChannel = channelInd - 1 if "ALL" == trackType else channelInd

            if importVideo:
                newClip = scene.sequence_editor.sequences.new_movie(
                    newClipName + " (video)", mediaPath, channelInd, atFrame
                )
                newClip.blend_type = "ALPHA_OVER"
                newClip.frame_offset_start = offsetStart
                newClip.frame_offset_end = offsetEnd
                if -1 != final_duration:
                    newClip.frame_final_duration = final_duration

            if importAudio:
                newClip = scene.sequence_editor.sequences.new_sound(
                    newClipName + " (sound)", mediaPath, audioChannel, atFrame
                )
                newClip.frame_offset_start = offsetStart
                newClip.frame_offset_end = offsetEnd
                if -1 != final_duration:
                    newClip.frame_final_duration = final_duration

        elif "IMAGE" == mediaType:
            newClipName = clipName if "" != clipName else "myImage"
            newClip = scene.sequence_editor.sequences.new_image(newClipName, mediaPath, channelInd, atFrame)
            newClip.blend_type = "ALPHA_OVER"
            newClip.frame_offset_start = offsetStart
            newClip.frame_offset_end = offsetEnd
            if -1 != final_duration:
                newClip.frame_final_duration = final_duration

        elif "IMAGES_SEQUENCE" == mediaType:
            newClipName = clipName if "" != clipName else "myImagesSequence"
            newClip = _new_images_sequence(scene, newClipName, mediaPath, channelInd, atFrame)
            # newClip = scene.sequence_editor.sequences.new_image("myVideo", mediaPath, channelInd, atFrame)
            newClip.blend_type = "ALPHA_OVER"
            newClip.frame_offset_start = offsetStart
            newClip.frame_offset_end = offsetEnd
            if -1 != final_duration:
                newClip.frame_final_duration = final_duration

        elif "SOUND" == mediaType:
            newClipName = clipName if "" != clipName else "mySound"
            newClip = scene.sequence_editor.sequences.new_sound(newClipName, mediaPath, channelInd, atFrame)
            newClip.frame_offset_start = offsetStart
            newClip.frame_offset_end = offsetEnd
            if -1 != final_duration:
                newClip.frame_final_duration = final_duration

        elif "CAMERA" == mediaType:
            newClipName = clipName if "" != clipName else "myCamera"
            newClip = _new_camera_sequence(
                scene,
                newClipName,
                channelInd,
                atFrame,
                offsetStart,
                offsetEnd,
                cameraScene,
                cameraObject,
            )
            newClip.blend_type = "ALPHA_OVER"

        elif "UNKNOWN" == mediaType:
            print("\n *** UNKNOWN media sent to Shot Manager - createNewClip(): ", mediaPath)
            pass

        if "UNKNOWN" != mediaType:
            mediaInfo = f"   - createNewClip(): Name: {newClip.name}, Media Type: {mediaType}, path: {mediaPath}"

            _logger.debug_ext(mediaInfo)

        # print(
        #     f"           frame_offset_start: {newClip.frame_offset_start}, frame_offset_end: {newClip.frame_offset_end}, frame_final_duration: {newClip.frame_final_duration}"
        # )

        # if newClip is not None and mediaType != "SOUNDS":
        #     newClip.frame_offset_start = offsetStart
        #     newClip.frame_offset_end = offsetEnd

        return newClip

    # wkip added to utils_vse
    def clearAllChannels(self, scene):
        for seq in scene.sequence_editor.sequences:
            scene.sequence_editor.sequences.remove(seq)

        bpy.ops.sequencer.refresh_all()

    # wkip added to utils_vse
    def clearChannel(self, scene, channelIndex):
        sequencesList = list()
        for seq in scene.sequence_editor.sequences:
            if channelIndex == seq.channel:
                sequencesList.append(seq)

        for seq in sequencesList:
            scene.sequence_editor.sequences.remove(seq)

        bpy.ops.sequencer.refresh_all()

    # wkip added to utils_vse
    def getChannelClips(self, scene, channelIndex):
        sequencesList = list()
        for seq in scene.sequence_editor.sequences:
            if channelIndex == seq.channel:
                sequencesList.append(seq)

        return sequencesList

    def deselectChannel(self, scene, channelIndex):
        for seq in scene.sequence_editor.sequences:
            if channelIndex == seq.channel:
                seq.select = False

    def deselectAllChannel(self, scene):
        for seq in scene.sequence_editor.sequences:
            seq.select = False

    # wkip mettre les mute: faut il les selectionner?
    def selectChannelClips(self, scene, channelIndex, mode="CLEARANDSELECT"):
        """Modes: "CLEARANDSELECT", "ADD", "REMOVE"
        Returns the resulting selected clips belonging to the track
        """
        sequencesList = list()
        for seq in scene.sequence_editor.sequences:
            if channelIndex == seq.channel:
                if "REMOVE" == mode:
                    seq.select = False
                else:
                    seq.select = True
                    sequencesList.append(seq)
            elif "CLEARANDSELECT" == mode:
                seq.select = False

        return sequencesList

    # wkip added to utils_vse
    def getChannelClipsNumber(self, scene, channelIndex):
        sequencesList = self.getChannelClips(scene, channelIndex)
        return len(sequencesList)

    # wkip added to utils_vse
    def changeClipsChannel(self, scene, sourceChannelIndex, targetChannelIndex):
        sourceSequencesList = self.getChannelClips(scene, sourceChannelIndex)
        targetSequencesList = list()

        if len(sourceSequencesList):
            targetSequencesList = self.getChannelClips(scene, targetChannelIndex)

            # we need to clear the target channel before doing the switch otherwise some clips may get moved to another channel
            if len(targetSequencesList):
                self.clearChannel(self.parentScene, targetChannelIndex)

            for clip in sourceSequencesList:
                clip.channel = targetChannelIndex

        return targetSequencesList

    # wkip added to utils_vse
    def swapChannels(self, scene, channelIndexA, channelIndexB):
        tempChannelInd = 0
        self.changeClipsChannel(scene, channelIndexA, tempChannelInd)
        self.changeClipsChannel(scene, channelIndexB, channelIndexA)
        self.changeClipsChannel(scene, tempChannelInd, channelIndexB)

    def cropClipToCanvas(
        self, canvasWidth, canvasHeight, clip, clipWidth, clipHeight, clipRenderPercentage=100, mode="FIT_ALL"
    ):
        """Mode can be FIT_ALL, FIT_WIDTH, FIT_HEIGHT, NO_RESIZE"""
        # clipRatio = clipWidth / clipHeight
        # canvasRatio = canvasWidth / canvasHeight

        clipRealWidth = int(clipWidth * (clipRenderPercentage / 100))
        clipRealHeight = int(clipHeight * (clipRenderPercentage / 100))

        if hasattr(clip, "use_crop"):
            if "FIT_ALL" == mode or (canvasWidth == clipRealWidth and canvasHeight == clipRealHeight):
                clip.use_crop = True
                clip.crop.min_x = clip.crop.max_x = clip.crop.min_y = clip.crop.max_y = 0
                clip.use_crop = False

            else:
                clip.use_crop = True
                clip.crop.min_x = clip.crop.max_x = 0
                clip.crop.min_y = clip.crop.max_y = 0

                if "FIT_WIDTH" == mode:
                    clipNewHeight = canvasWidth / clipRealWidth * clipRealHeight
                    clip.crop.min_y = clip.crop.max_y = (
                        -0.5 * (clipRenderPercentage / 100) * (canvasHeight - clipNewHeight)
                    )

                if "FIT_HEIGHT" == mode:
                    clipNewWidth = canvasHeight / clipRealHeight * clipRealWidth
                    clip.crop.min_x = clip.crop.max_x = (
                        -0.5 * (clipRenderPercentage / 100) * (canvasWidth - clipNewWidth)
                    )

                if "NO_RESIZE" == mode:
                    clip.crop.min_x = clip.crop.max_x = (
                        -0.5 * (clipRenderPercentage / 100) * (canvasWidth - clipRealWidth)
                    )
                    clip.crop.min_y = clip.crop.max_y = (
                        -0.5 * (clipRenderPercentage / 100) * (canvasHeight - clipRealHeight)
                    )
                    pass

    def get_frame_end_from_content(self, scene):
        # wkipwkipwkip erreur ici, devrait etre exclusive pour extre consistant et ne l'est pas
        """get_frame_end is exclusive in order to follow the Blender implementation of get_frame_end for its clips"""
        videoChannelClips = self.getChannelClips(scene, 1)
        scene_frame_start = scene.frame_start  # scene.sequence_editor.sequences

        frame_end = scene_frame_start
        if len(videoChannelClips):
            frame_end = videoChannelClips[len(videoChannelClips) - 1].frame_final_end

        frame_end = max(frame_end, scene_frame_start)

        return frame_end

    def printClipInfo(self, clip, printTimeInfo=False):
        infoStr = "\n\n------ VSE Render - Clip Info : "
        # infoStr += (
        #     f"\nNote: All the end values are EXCLUSIVE (= not the last used frame of the range but the one after)"
        # )
        infoStr += f"Clip: {clip.name}, type: {clip.type}, enabled: {not clip.mute}"

        if printTimeInfo:
            frameStart = clip.frame_start
            frameEnd = clip.frame_start + clip.frame_duration  # -1  # clip.frame_end
            frameFinalStart = clip.frame_final_start
            frameFinalEnd = clip.frame_final_end
            frameOffsetStart = clip.frame_offset_start
            frameOffsetEnd = clip.frame_offset_end
            frameDuration = clip.frame_duration
            frameFinalDuration = clip.frame_final_duration

            infoStr += f"\n   Abs clip values: frame_start: {frameStart}, frame_final_start:{frameFinalStart}, frame_final_end:{frameFinalEnd}, frame_end (excl): {frameEnd}"
            infoStr += (
                f"\n   Rel clip values: frame_offset_start: {frameOffsetStart}, frame_offset_end:{frameOffsetEnd}"
            )
            infoStr += (
                f"\n   Duration clip values: frame_duration: {frameDuration}, frame_final_duration:{frameFinalDuration}"
            )

        #        infoStr += f"\n    Start: {self.get_frame_start()}, End (incl.):{self.get_frame_end() - 1}, Duration: {self.get_frame_duration()}, fps: {self.get_fps()}, Sequences: {self.get_num_sequences()}"
        print(infoStr)

    # NOTE: This function has 2 different behaviors depending if we use mediaDictArr or mediaFiles
    # FIXME: wkipwkipwkip this has to be fixed to harmonize the behavior
    def buildSequenceVideoFromMedia(self, outputFile, handles, fps, mediaDictArr=None, mediaFiles=None):
        """Create a composited output (image sequence or video according to the extension of outputFile) from
        the bg, fg and audio media provided either by mediaDictArr or mediaFiles

        Args:
            mediaDictArr: dictionary specifying the source media and their resolution
            mediaFiles: list of 2 media and an audio
        """
        previousScene = bpy.context.window.scene

        sequenceScene = None
        if "VSE_SequenceRenderScene" in bpy.data.scenes:
            sequenceScene = bpy.data.scenes["VSE_SequenceRenderScene"]
            bpy.data.scenes.remove(sequenceScene, do_unlink=True)
        sequenceScene = bpy.data.scenes.new(name="VSE_SequenceRenderScene")

        createVseTab = False  # config.devDebug
        sequenceScene = utils.getSceneVSE(sequenceScene.name, createVseTab=createVseTab)  # config.devDebug)
        bpy.context.window.scene = sequenceScene

        if createVseTab:
            bpy.context.window.workspace = bpy.data.workspaces["Video Editing"]

        #     for area in bpy.context.screen.areas:
        #         print(f"area type: {area.type}")
        #         if area.type == "SEQUENCE_EDITOR":
        #             area.spaces.items()[0][1].show_seconds = True

        utils.setSceneFps(sequenceScene, fps)  # projectFps

        if mediaDictArr is not None:
            sequenceScene.render.resolution_x = mediaDictArr[0]["output_resolution"][0]
            sequenceScene.render.resolution_y = mediaDictArr[0]["output_resolution"][1]
            inputOverResolution = mediaDictArr[0]["fg_sequence_resolution"]
        else:
            # mediaFiles is not None
            # wkipwkipwkip
            sequenceScene.render.resolution_x = self.outputResolution[0]
            sequenceScene.render.resolution_y = self.outputResolution[1]

        sequenceScene.frame_start = 0
        # sequenceScene.frame_end = props.getEditDuration() - 1
        sequenceScene.render.image_settings.file_format = "FFMPEG"
        sequenceScene.render.ffmpeg.format = "MPEG4"
        sequenceScene.render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"  # "PERC_LOSSLESS"
        sequenceScene.render.ffmpeg.gopsize = 5  # keyframe interval, 2?
        sequenceScene.render.ffmpeg.audio_codec = "AAC"
        sequenceScene.render.filepath = outputFile

        # change color tone mode to prevent washout bug with "filmic" rendered image mode
        _logger.debug_ext(
            f"Changing sequenceScene Color from {sequenceScene.view_settings.view_transform} to Raw", col="PINK"
        )
        sequenceScene.view_settings.view_transform = "Raw"

        if mediaDictArr is not None:
            atFrame = 0
            for i, mediaDict in enumerate(mediaDictArr):
                # sequenceScene.sequence_editor
                frameToPaste = self.get_frame_end_from_content(sequenceScene)
                print("\n---- Importing image sequences ----")
                # print(f"  frametopaste: {frameToPaste}")

                bgClip = None
                shotDuration = 0
                if "bg" in mediaDict and mediaDict["bg"] is not None:
                    try:
                        print(f"self.inputBGMediaPath: {mediaDict['bg']}")
                        bgClip = self.createNewClip(sequenceScene, mediaDict["bg"], 2, atFrame)
                        shotDuration = bgClip.frame_final_duration
                    except Exception:
                        _logger.error_ext(f" *** Rendered shot not found: {mediaDict['bg']}")

                    # bgClip = None
                    # if os.path.exists(self.inputBGMediaPath):
                    #     bgClip = self.createNewClip(vse_scene, self.inputBGMediaPath, 1, 1)
                    # else:
                    #     print(f" *** Rendered shot not found: {self.inputBGMediaPath}")

                #    print(f"self.inputBGMediaPath: {self.inputOverMediaPath}")

                if "fg_sequence" in mediaDict and mediaDict["fg_sequence"] is not None:
                    overClip = None
                    try:
                        overClip = self.createNewClip(sequenceScene, mediaDict["fg_sequence"], 3, atFrame)
                        print("Over Media OK")
                    except Exception:
                        _logger.error_ext(f" *** Rendered shot not found: {mediaDict['fg_sequence']}")
                    # overClip = None
                    # if os.path.exists(self.inputOverMediaPath):
                    #     overClip = self.createNewClip(vse_scene, self.inputOverMediaPath, 2, 1)
                    # else:
                    #     print(f" *** Rendered shot not found: {self.inputOverMediaPath}")

                    if overClip is not None:
                        res_x = mediaDictArr[0]["bg_resolution"][0]
                        res_y = mediaDictArr[0]["bg_resolution"][1]
                        clip_x = inputOverResolution[0]
                        clip_y = inputOverResolution[1]
                        self.cropClipToCanvas(
                            res_x,
                            res_y,
                            overClip,
                            clip_x,
                            clip_y,
                            mode="FIT_WIDTH",
                        )
                        # overClip.use_crop = True
                        # overClip.crop.min_x = -1 * int((mediaDictArr[0]["bg_resolution"][0] - inputOverResolution[0]) / 2)
                        # overClip.crop.max_x = overClip.crop.min_x
                        # overClip.crop.min_y = -1 * int((mediaDictArr[0]["bg_resolution"][1] - inputOverResolution[1]) / 2)
                        # overClip.crop.max_y = overClip.crop.min_y

                        overClip.blend_type = "OVER_DROP"
                        shotDuration = overClip.frame_final_duration

                if "sound" in mediaDict and mediaDict["sound"] is not None:
                    audioClip = None
                    if os.path.exists(mediaDict["sound"]):
                        audioClip = self.createNewClip(
                            sequenceScene, mediaDict["sound"], 1, atFrame, final_duration=shotDuration
                        )
                        audioClip = self.createNewClipFromRange(
                            sequenceScene,
                            mediaDict["sound"],
                            1,
                        )
                    else:
                        _logger.error_ext(f" *** Rendered shot not found: {mediaDict['sound']}")

                # bpy.context.scene.sequence_editor.sequences
                # get res of video: bpy.context.scene.sequence_editor.sequences[1].elements[0].orig_width
                # ne marche que sur vidéos

                # sequenceScene.frame_end = self.get_frame_end_from_content(sequenceScene) - 1
                # print(f"sequenceScene.frame_end: {sequenceScene.frame_end}")
                atFrame += shotDuration
                print(f"atFrame: {atFrame}")

            # Make "My New Scene" the active one
            # bpy.context.window.scene = vse_scene

            sequenceScene.frame_end = atFrame - 1

            # fix to get even resolution values:
            # print(
            #     f"Render W: {sequenceScene.render.resolution_x} and H: {sequenceScene.render.resolution_y}, %: {sequenceScene.render.resolution_percentage}"
            # )
            if 100 != sequenceScene.render.resolution_percentage:
                sequenceScene.render.resolution_x = int(
                    sequenceScene.render.resolution_x * sequenceScene.render.resolution_percentage / 100.0
                )
                sequenceScene.render.resolution_y = int(
                    sequenceScene.render.resolution_y * sequenceScene.render.resolution_percentage / 100.0
                )
                sequenceScene.render.resolution_percentage = 100

            if 1 == sequenceScene.render.resolution_x % 2:
                sequenceScene.render.resolution_x += 1
            if 1 == sequenceScene.render.resolution_y % 2:
                sequenceScene.render.resolution_y += 1

            # print(
            #     f"Render New W: {sequenceScene.render.resolution_x} and H: {sequenceScene.render.resolution_y}, %: {sequenceScene.render.resolution_percentage}"
            # )

        # mediaFiles part
        else:
            for mediaPath in mediaFiles:
                # sequenceScene.sequence_editor
                frameToPaste = self.get_frame_end_from_content(sequenceScene)
                print("\n---- Importing video ----")
                # print(f"  frametopaste: {frameToPaste}")
                # video clip
                self.createNewClip(
                    sequenceScene,
                    mediaPath,
                    0,
                    frameToPaste - handles,  # shot.getEditStart() - handles,
                    offsetStart=handles,
                    offsetEnd=handles,
                    importVideo=True,
                    importAudio=False,
                )

                # audio clip
                self.createNewClip(
                    sequenceScene,
                    mediaPath,
                    1,
                    frameToPaste - handles,  # shot.getEditStart() - handles,
                    offsetStart=handles,
                    offsetEnd=handles,
                    importVideo=False,
                    importAudio=True,
                )

            sequenceScene.frame_end = self.get_frame_end_from_content(sequenceScene) - 1

        bpy.ops.render.opengl(animation=True, sequencer=True, write_still=False)

        # cleaning current file from temp scenes
        if not config.devDebug_keepVSEContent:
            # current scene is sequenceScene
            bpy.ops.scene.delete()
            pass

        # wkip changer ca fait que le time range n'est pas pris en compte...
        # if not config.devDebug:
        bpy.context.window.scene = previousScene
        # if config.devDebug:
        #     bpy.context.window.scene = sequenceScene

    def compositeVideoInVSE(
        self,
        fps,
        frame_start,
        frame_end,
        output_filepath,
        output_filename=None,
        compositedImgSeqPath=None,
        output_file_prefix="",
        postfixSceneName="",
        output_resolution=None,
        output_media_mode="VIDEO",
        importAtFrame=0,
        frame_padding=-1,
    ):
        """Low level function that will use the bg and fg media already held by this vse_render class to generate
        a media

        Args:
            output_resolution: array [width, height]
            output_media_mode: can be "IMAGE_SEQ", "VIDEO", "IMAGE_SEQ_AND_VIDEO". Specify the file format of the rendered
            media.
            frame_padding: THIS ARGUMENT MUST BE ENTERED. Usually it is 4 or 5.
        """

        def _setOutputMediaAndRender(output_media_type):
            """output_media_type can be "IMAGE", "IMAGE_SEQ" or "VIDEO" """
            # _logger.debug_ext(f"_setOutputMediaAndRender output_media_type: {output_media_type}")

            # get output file format from specified output (can be emtpy !!)
            fileExt = str(Path(output_filepath).suffix).upper()
            # get file name without extention
            # fileNoExt = output_filepath[: len(output_filepath) - len(fileExt)]
            if output_filename is None:
                fileNoExt = str(Path(output_filepath).stem)
            else:
                fileNoExt = output_filename
            # get file path only
            filePathOnly = str(Path(output_filepath).parent) + "\\"

            if "." == fileExt[0]:
                fileExt = fileExt[1:]

            # get either "#####" or a formated string for specificFrame
            if specificFrame is None:
                frameIndStr = "".rjust(frame_padding, "#")
            else:
                frameIndStr = str(specificFrame).rjust(frame_padding, "0")

            # TODO: add a separator as global parameter
            frameIndStr = "_" + frameIndStr

            # case where specificFrame is NOT none
            if "IMAGE" == output_media_type:
                vse_scene.render.image_settings.file_format = "PNG"  # wkipwkipwkip mettre project info

                if config.devDebug:
                    print(f"specificFrame: {specificFrame}")

                # remove the end digits if there are some
                # fileNoExt = fileNoExt.rstrip("0123456789")

                self.outputMediaPath = filePathOnly + output_file_prefix + fileNoExt + frameIndStr + ".png"
                vse_scene.render.filepath = self.outputMediaPath

                # vse_scene.frame_set(specificFrame)
                vse_scene.frame_set(importAtFrame)
                # specificFrame = importAtFrame

                vse_scene.render.use_file_extension = False
                # bpy.ops.render.render(write_still=True)
                bpy.ops.render.opengl(animation=False, sequencer=True, write_still=True)

            elif "IMAGE_SEQ" == output_media_type:
                if compositedImgSeqPath is not None:
                    ext = str(Path(compositedImgSeqPath).suffix).lower()

                elif len(fileExt):
                    # if "JPG" == fileExt:
                    #     vse_scene.render.image_settings.file_format = "JPEG"
                    #     ext = ".jpg"
                    # # if "PNG" == fileExt:
                    # else:
                    #     # output file is PNG otherwise
                    #     vse_scene.render.image_settings.file_format = "PNG"
                    #     ext = ".png"
                    ext = "." + fileExt.lower()

                else:
                    # output file is PNG otherwise
                    vse_scene.render.image_settings.file_format = "PNG"
                    ext = ".png"

                # self.outputMediaPath = (
                #     filePathOnly + fileNoExt + "\\" + output_file_prefix + fileNoExt + frameIndStr + ext
                # )
                # wkipwkipwkipmerge
                self.outputMediaPath = (
                    filePathOnly + fileNoExt + "\\" + output_file_prefix + fileNoExt + frameIndStr + ext
                )
                vse_scene.render.filepath = self.outputMediaPath

                vse_scene.render.filepath = self.outputMediaPath

                # since Blender starts the render indices at 1 and not 0 we have to rename the sequence
                # another approach than renaming is to render still images
                vse_scene.render.use_file_extension = False
                bpy.ops.render.opengl(animation=True, sequencer=True)

                # importAtFrame
                # if props.editStartFrame

            # "VIDEO" == output_media_type:
            else:
                # elif "MP4" == fileExt:
                vse_scene.render.image_settings.file_format = "FFMPEG"
                vse_scene.render.ffmpeg.format = "MPEG4"
                vse_scene.render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"  # "PERC_LOSSLESS"
                vse_scene.render.ffmpeg.gopsize = 5  # keyframe interval
                vse_scene.render.ffmpeg.audio_codec = "AAC"

                self.outputMediaPath = filePathOnly + output_file_prefix + fileNoExt + ".mp4"
                vse_scene.render.filepath = self.outputMediaPath

                vse_scene.render.use_file_extension = False
                bpy.ops.render.opengl(animation=True, sequencer=True)

            return

        if config.devDebug:
            self.printMedia()

        mediaStr = "VSE_Render  output_resolution:   "
        mediaStr += (
            "None" if output_resolution is None else f"{output_resolution[0]} x {output_resolution[1]}"
        ) + f"  {output_resolution}\n"
        # print(mediaStr)

        specificFrame = None
        if frame_start == frame_end:
            specificFrame = frame_start
            # specificFrame = importAtFrame

        previousScene = bpy.context.window.scene
        previousWorkspace = bpy.context.workspace.name
        # print(f"Previous Workspace: {previousWorkspace}")
        previousScreen = bpy.context.window.screen.name
        # print(f"Previous Screen: {previousScreen}")
        previousRenderView = None
        region = next(
            iter([area.spaces[0].region_3d for area in bpy.context.screen.areas if area.type == "VIEW_3D"]), None
        )
        if region:
            # print(f"current view: {region.view_perspective}")
            previousRenderView = region.view_perspective

        # Add new scene
        # vse_scene = bpy.data.scenes.new(name="Tmp_VSE_RenderScene" + postfixSceneName)
        vse_scene = utils.getSceneVSE("Tmp_VSE_RenderScene" + postfixSceneName, createVseTab=True)
        self.clearAllChannels(vse_scene)

        # vse_scene.render.fps = fps
        utils.setSceneFps(vse_scene, fps)

        # Make "My New Scene" the active one
        #    bpy.context.window.scene = vse_scene

        #    vse_scene = utils.getSceneVSE(vse_scene.name, createVseTab=config.devDebug)
        # if not vse_scene.sequence_editor:
        #     vse_scene.sequence_editor_create()

        # https://docs.blender.org/api/blender_python_api_2_77_0/bpy.types.Sequences.html
        # Path ( renderPath ).parent.mkdir ( parents = True, exist_ok = True )

        # resolution
        output_res = [vse_scene.render.resolution_x, vse_scene.render.resolution_y]
        if output_resolution is not None:
            output_res = output_resolution.copy()
        else:
            if "" != self.inputBGMediaPath:
                output_res = self.inputBGResolution.copy()
            elif "" != self.inputOverMediaPath:
                output_res = self.inputOverResolution.copy()

        vse_scene.render.resolution_x = output_res[0]
        vse_scene.render.resolution_y = output_res[1]
        # print(f"  * - * vse_scene.render.resolution: {vse_scene.render.resolution_x} x {vse_scene.render.resolution_y}")

        vse_scene.frame_start = frame_start
        vse_scene.frame_end = frame_end

        # change color tone mode to prevent washout bug (usually with "filmic" mode)
        _logger.debug_ext(
            f"Changing vse_scene Color from {vse_scene.view_settings.view_transform} to Standard", col="PINK"
        )
        vse_scene.view_settings.view_transform = "Standard"  # "Filmic"  # "raw"
        _logger.debug_ext(f"new color mode: {vse_scene.view_settings.view_transform}", col="PINK")

        bgClip = None
        if "" != self.inputBGMediaPath:
            try:
                #    print(f"self.inputBGMediaPath: {self.inputBGMediaPath}")
                bgClip = self.createNewClip(vse_scene, self.inputBGMediaPath, 1, atFrame=importAtFrame)
            #    print("BG Media OK")
            except Exception:
                _logger.error_ext(f" *** Rendered shot not found: {self.inputBGMediaPath}")

            # bgClip = None
            # if os.path.exists(self.inputBGMediaPath):
            #     bgClip = self.createNewClip(vse_scene, self.inputBGMediaPath, 1, 1)
            # else:
            #     print(f" *** Rendered shot not found: {self.inputBGMediaPath}")

            #    print(f"self.inputBGMediaPath: {self.inputOverMediaPath}")

            if bgClip is not None:
                if output_res[0] < self.inputBGResolution[0] or output_res[1] < self.inputBGResolution[1]:
                    bgClip.use_crop = True
                    bgClip.crop.min_x = int((self.inputBGResolution[0] - output_res[0]) / 2)
                    bgClip.crop.max_x = bgClip.crop.min_x
                    bgClip.crop.min_y = int((self.inputBGResolution[1] - output_res[1]) / 2)
                    bgClip.crop.max_y = bgClip.crop.min_y

        if "" != self.inputOverMediaPath:
            overClip = None
            _logger.debug_ext(f" *** Over media path: {self.inputOverMediaPath}", col="PURPLE")
            try:
                overClip = self.createNewClip(vse_scene, self.inputOverMediaPath, 2, atFrame=importAtFrame)
            #    print("Over Media OK")
            except Exception:
                _logger.error_ext(f" *** Rendered shot not found: {self.inputOverMediaPath}")
            # overClip = None
            # if os.path.exists(self.inputOverMediaPath):
            #     overClip = self.createNewClip(vse_scene, self.inputOverMediaPath, 2, 1)
            # else:
            #     print(f" *** Rendered shot not found: {self.inputOverMediaPath}")

            if overClip is not None:
                # if output_res[0] < self.inputOverResolution[0] or output_res[1] < self.inputOverResolution[1]:
                if output_res[0] != self.inputOverResolution[0] or output_res[1] != self.inputOverResolution[1]:
                    overClip.use_crop = True
                    overClip.crop.min_x = int((self.inputOverResolution[0] - output_res[0]) / 2)
                    overClip.crop.max_x = overClip.crop.min_x
                    overClip.crop.min_y = int((self.inputOverResolution[1] - output_res[1]) / 2)
                    overClip.crop.max_y = overClip.crop.min_y
                    overClip.blend_type = "OVER_DROP"

        if self.inputAudioMediaPath is not None:
            if specificFrame is None:
                audioClip = None
                if os.path.exists(self.inputAudioMediaPath):
                    audioClip = self.createNewClip(vse_scene, self.inputAudioMediaPath, 3, atFrame=importAtFrame)
                else:
                    _logger.error_ext(f" *** Rendered shot not found: {self.inputAudioMediaPath}")

        # bpy.context.scene.sequence_editor.sequences
        # get res of video: bpy.context.scene.sequence_editor.sequences[1].elements[0].orig_width
        # ne marche que sur vidéos

        # Make "My New Scene" the active one
        bpy.context.window.scene = vse_scene

        ### render
        ##################
        if specificFrame is None:
            if "IMAGE_SEQ" in output_media_mode:
                _setOutputMediaAndRender("IMAGE_SEQ")

            if "VIDEO" in output_media_mode:
                _setOutputMediaAndRender("VIDEO")
        else:
            _setOutputMediaAndRender("IMAGE")

        if config.devDebug:
            self.printMedia()

        if not config.devDebug_keepVSEContent:
            bpy.ops.scene.delete()
            pass

        bpy.context.window.scene = previousScene

        # print(f" *** Current Workspace: {bpy.context.workspace.name}")

        # bpy.context.window.screen.name = previousScreen
        bpy.context.window.workspace = bpy.data.workspaces[previousWorkspace]
        # print(f" *** Current Workspace: {bpy.context.workspace.name}")

        bpy.context.window.screen = bpy.context.window_manager.windows[0].screen
        bpy.context.window.screen = bpy.data.screens[previousScreen]
        # bpy.context.window_manager.windows[1].screen = bpy.data.screens[previousScreen]

        if region and previousRenderView is not None:
            region.view_perspective = previousRenderView

        # testDir = "Z:\\UAS_ShotManager_Data\\"
        # bpy.ops.image.open(filepath="//Main_Take0010.png", directory=testDir, files=[{"name":"Main_Take0010.png", "name":"Main_Take0010.png"}],
        #   relative_path=True, show_multiview=False)
        # bpy.ops.image.open(
        #     filepath="//SceneRace_Sh0020_0079.png",
        #     directory="C:\\tmp02\\Main_Take\\",
        #     files=[{"name": "SceneRace_Sh0020_0079.png", "name": "SceneRace_Sh0020_0079.png"}],
        #     relative_path=True,
        #     show_multiview=False,
        # )

        # open rendered media in a player
        if specificFrame is not None:
            utils.openMedia(output_filepath, inExternalPlayer=False)


_classes = (
    # UAS_PT_VSERender,
    UAS_VSE_OpenFileBrowser,
    ShotManager_Vse_Render,
)


def register():
    _logger.debug_ext("       - Registering Utils VSE Render Package", form="REG")

    for cls in _classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.UAS_vse_render = PointerProperty(type=ShotManager_Vse_Render)


def unregister():
    _logger.debug_ext("       - Unregistering Utils VSE Render Package", form="UNREG")

    for cls in reversed(_classes):
        #  print(f"           -- Utils_vse_render.py {str(cls)}")
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            _logger.error_ext(f"Error in Unregistering class {str(cls)}:  {e}")

    del bpy.types.WindowManager.UAS_vse_render
