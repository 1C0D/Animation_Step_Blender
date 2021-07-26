import bpy
bl_info = {
    "name": "Animation step",
    "author": "1C0D",
    "version": (1, 2, 0),
    "blender": (2, 83, 0),
    "location": "View3D > dopesheet/timeline top bar ",
    "description": "add a step setting to move animation cursor right/left arrow + Ctrl",
    "category": "Object",
}


class MY_OT_STEP(bpy.types.Operator):
    bl_idname = "my.step"
    bl_label = "My step"

    back: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        scene = context.scene
        if self.back:
            bpy.ops.screen.frame_offset(delta=scene.delta_set)
        else:
            bpy.ops.screen.frame_offset(delta=-(scene.delta_set))
        context.area.tag_redraw()

        return {'FINISHED'}


def drawstep(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.scale_x = 0.75
    scene = context.scene
    row.prop(scene, "delta_set", text="Step")


class Inc_OT_step(bpy.types.Operator):
    bl_idname = "inc.step"
    bl_label = "inc step"

    inc: bpy.props.BoolProperty(default=False)

    def execute(self, context):

        if self.inc:
            context.scene.delta_set += 1
        else:
            if context.scene.delta_set > 1:
                context.scene.delta_set -= 1
        context.area.tag_redraw()

        return {'FINISHED'}


addon_keymaps = []

classes = (MY_OT_STEP, Inc_OT_step)


def register():

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.delta_set = bpy.props.IntProperty(
        default=1,
        min=1,
        max=100000,
    )

    bpy.types.DOPESHEET_HT_header.append(drawstep)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is not None:
        km = kc.keymaps.new(name='Frames', space_type='EMPTY')

        kmi = km.keymap_items.new('my.step', 'RIGHT_ARROW', 'PRESS', ctrl=True)
        kmi.properties.back = True
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('my.step', 'LEFT_ARROW', 'PRESS', ctrl=True)
        kmi.properties.back = False
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('inc.step', 'RIGHT_ARROW', 'PRESS', alt=True)
        kmi.properties.inc = True
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('inc.step', 'LEFT_ARROW', 'PRESS', alt=True)
        kmi.properties.inc = False
        addon_keymaps.append((km, kmi))


def unregister():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is not None:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    bpy.types.DOPESHEET_HT_header.remove(drawstep)
    del bpy.types.Scene.delta_set

    for c in classes:
        bpy.utils.unregister_class(c)
