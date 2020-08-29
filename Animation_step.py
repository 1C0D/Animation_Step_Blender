'''
v1.3 modifications for more clean code

'''
bl_info = {
    "name": "Animation step",
    "author": "1C0D",
    "version": (1, 0, 0),
    "blender": (2, 83, 0),
    "location": "View3D > dopesheet/timeline top bar ",
    "description": "add a step setting to move animation cursor right/left arrow + Ctrl",    
    "category": "Object",
}

import bpy

def get_step1(self):
    return bpy.context.scene.delta_set

def set_step1(self,value):
    bpy.context.scene.Temp_step=value
    
def update_step1(self,context):
    
    if context.scene.delta_set != context.scene.Temp_step:
        context.scene.delta_set = context.scene.delta_set1    

bpy.types.Scene.delta_set1=bpy.props.IntProperty(default=1,min=1,max=100000,
get=get_step1,
set=set_step1, 
update=update_step1
)

bpy.types.Scene.Temp_step=bpy.props.IntProperty(default=1, min=1,max=100000) 
    

class MY_OT_STEP(bpy.types.Operator):
    bl_idname = "my.step0"
    bl_label = "My step"

    def execute(self, context):
        scene = context.scene
        bpy.ops.screen.frame_offset(delta=scene.delta_set)
        
        return {'FINISHED'}

class MY_OT_STEP1(bpy.types.Operator):
    bl_idname = "my.step01"
    bl_label = "My step1"

    def execute(self, context):
        scene = context.scene
        bpy.ops.screen.frame_offset(delta=-(scene.delta_set))
        
        return {'FINISHED'}
        
    
def drawstep(self, context):
    layout = self.layout
    row=layout.row(align=True)
    row.scale_x = 0.75 
    scene = context.scene
    row.prop(scene, "delta_set",text="Step")
    
    
class Inc_OT_step(bpy.types.Operator):
    bl_idname = "inc.step"
    bl_label = "inc step"
    
    
    def execute(self, context):
        
        context.scene.delta_set+=1
        
        return {'FINISHED'}
    
class Dec_OT_step(bpy.types.Operator):
    bl_idname = "dec.step"
    bl_label = "dec step"
    
    def execute(self, context):
        
        if context.scene.delta_set >1:
            context.scene.delta_set-=1
        else:
            pass
        
        return {'FINISHED'}

addon_keymaps = []     
   
def register(): 

    bpy.utils.register_class(MY_OT_STEP)
    bpy.utils.register_class(MY_OT_STEP1)   
    bpy.utils.register_class(Inc_OT_step) 
    bpy.utils.register_class(Dec_OT_step)  
    
    bpy.types.Scene.delta_set=bpy.props.IntProperty(
    default=1,
    min=1,
    max=100000,
    update=update_step1
    )
        
    bpy.types.DOPESHEET_HT_header.append(drawstep)    
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is not None:
        km = kc.keymaps.new(name='Frames', space_type='EMPTY')
        
        kmi = km.keymap_items.new('my.step0', 'RIGHT_ARROW', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))
    
        kmi = km.keymap_items.new('my.step01', 'LEFT_ARROW', 'PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))
        
        
        kmi = km.keymap_items.new('inc.step', 'RIGHT_ARROW', 'PRESS',alt=True)
        addon_keymaps.append((km, kmi))
        
        kmi = km.keymap_items.new('dec.step', 'LEFT_ARROW', 'PRESS',alt=True)
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
    

    bpy.utils.unregister_class(MY_OT_STEP1)
    bpy.utils.unregister_class(MY_OT_STEP)  
    bpy.utils.unregister_class(Inc_OT_step)  
    bpy.utils.unregister_class(Dec_OT_step)  
    
if __name__ == "__main__":
    register()


