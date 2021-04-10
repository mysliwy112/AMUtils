# #### Licence section ####
# Copyright (C) 2021  mysliwy112

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# #### Main section ####

import struct as st

class Reader:
  def __init__(self,data,offset=0):
    self.data = data
    self.off=offset

  def read(self,type):
    if isinstance(type, int):
        var=st.unpack_from(str(type-1)+"s", self.data, offset=self.off)[0].decode("utf-8") 
        self.off+=type
    else:
        var=st.unpack_from(type, self.data, offset=self.off)[0]
        self.off+=st.calcsize(type)
    return var

def loadKImodel(file):
    data=[]
    with open(file,"rb") as f:
        data=f.read()


    loopRead=Reader(data,st.unpack_from("<I", data, offset=16)[0])
    loopNum=st.unpack_from("<I", data, offset=16+8)[0]
    
    vertRead=Reader(data,st.unpack_from("<I", data, offset=28)[0])
    vertNum=st.unpack_from("<I", data, offset=28+8)[0]
    
    boneRead=Reader(data,st.unpack_from("<I", data, offset=256)[0])
    boneNum=st.unpack_from("<I", data, offset=256+8)[0]


    vertices = []
    loops = [] 
    uvs = []
    bones = {
        "name":[],
        "pos":[],
        "parent":[]
    }
    bonesP = []

    for i in range(0,vertNum):
        if(vertRead.off+16>len(data)):
            break
        x=vertRead.read("<f")
        y=vertRead.read("<f")
        z=vertRead.read("<f")
        
        vertices.append(x)
        vertices.append(z)
        vertices.append(y)
        vertRead.off+=4*4
        
        x=vertRead.read("<f")
        y=vertRead.read("<f")
        uvs.append((x,1-y))
        vertRead.off+=4*8

    for i in range(0,loopNum):
        loops.append(loopRead.read("<I"))
        
    for i in range(0,boneNum):
        nSize=boneRead.read("<I")
        bones["name"].append(boneRead.read(nSize))

        bones["parent"].append(boneRead.read("<I"))
        
        x=boneRead.read("<f")
        y=boneRead.read("<f")
        z=boneRead.read("<f")
        bones["pos"].append([x,z,y])
        
        boneRead.off+=7*4

    return vertices, loops, uvs, bones

# #### Your file exporter here ####


# #### Blender Section ####

bl_info = {
    "name": "KIengine kimodel format",
    "description": "Imports .kimodel from TTW to blender.",
    "blender": (2, 80, 0),
    "location": "File > Import",
    "category": "Import-Export",
}

try:
    import bpy
    from bpy_extras.io_utils import ImportHelper
    from bpy.props import (
            StringProperty,
            CollectionProperty )
    


    def blendCreateObject(name, vertices, loops, uvs, bones):
        vertNum=int(len(vertices)/3)
        loopNum=len(loops)
        bonesNum=len(bones["name"])
        
        mesh = bpy.data.meshes.new('KI')

        mesh.vertices.add(vertNum)
        mesh.vertices.foreach_set("co", vertices)

        mesh.loops.add(loopNum)
        mesh.loops.foreach_set("vertex_index", loops)

        mesh.polygons.add(int(loopNum/3))
        mesh.polygons.foreach_set("loop_start", range(0,loopNum,3))
        mesh.polygons.foreach_set("loop_total", [3]*int(loopNum/3))

        mesh.polygons.foreach_set("loop_total", [3]*int(loopNum/3))

        mesh.uv_layers.new(name="KI_uv")

        for face in mesh.polygons:
            for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                mesh.uv_layers.active.data[loop_idx].uv = uvs[vert_idx]

        mesh.update()

        object = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(object)
        
        
        
        arm_data = bpy.data.armatures.new("name")
        arm_ob = bpy.data.objects.new("name", arm_data)
        bpy.context.collection.objects.link(arm_ob)

        arm_ob.select_set(True)
        bpy.context.view_layer.objects.active = arm_ob

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        edit_bones = arm_data.edit_bones
        
        bBones=[]
        print(bones["name"])
        for b in range(0,bonesNum):
            bone=edit_bones.new(bones["name"][b])
            bone.head = bones["pos"][b]
            bone.tail = bones["pos"][b]
            bBones.append(bone)
        print(len(bBones)) 
        print(len(bones["name"])) 
        for b in range(0,bonesNum):
            if bones["parent"][b]<32:
                bBones[b].parent=bBones[bones["parent"][b]]
            bBones[b].use_connect = True
        bpy.ops.object.mode_set(mode='OBJECT')



    class ImportKImodel(bpy.types.Operator, ImportHelper):
        """Load a KIengine KImodel File"""
        bl_idname = "import_scene.kimodel"
        bl_label = "Import KImodel"
        bl_options = {'PRESET', 'UNDO'}

        filter_glob: StringProperty(
                default="*.kimodel",
                options={'HIDDEN'},
                )
        files: CollectionProperty(
                type=bpy.types.OperatorFileListElement,
                options={'HIDDEN', 'SKIP_SAVE'},
            )
        directory = StringProperty(subtype='DIR_PATH')

        def execute(self, context):
            for f in self.files:
                v,l,u = loadKImodel(self.directory+f.name)
                blendCreateObject(f.name.split('.')[0],v,l,u)
            return {'FINISHED'}
            

    def menu_func_import(self, context):
        self.layout.operator(ImportKImodel.bl_idname, text="KIengine (.kimodel)")

    def menu_func_export(self, context):
        print("WORK IN PROGRESS")
        pass
        self.layout.operator(ExportKImodel.bl_idname, text="KIengine (.kimodel)")


    def register():
        bpy.utils.register_class(ImportKImodel)
        bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


    def unregister():
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
        bpy.utils.unregister_class(ImportKImodel)

except ModuleNotFoundError as err:
    pass

#file=r"E:\AidemMedia\RiK TTW\data\models\grid.kimodel"
#file=r"E:\AidemMedia\RiK TTW\data\models\sel.kimodel"
#file=r"E:\AidemMedia\RiK TTW\data\models\players\blue\blue.kimodel"
file=r"E:\AidemMedia\RiK TTW\data\models\players\green\green.kimodel"
#file=r"E:\AidemMedia\RiK TTW\data\models\players\yellow\yellow.kimodel"
#file=r"E:\AidemMedia\RiK TTW\data\models\levels\planet_monolith.kimodel"
v,l,u,b = loadKImodel(file)
blendCreateObject("Fug",v,l,u,b)