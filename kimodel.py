import struct as st


# #### Main section ####

def read(off,type,data):
    var=st.unpack_from(type, data, offset=off)[0]
    off+=4
    return var, off

def loadKImodel(file):
    data=[]
    #file=r"E:\AidemMedia\RiK TTW\data\models\grid.kimodel"
    #file=r"E:\AidemMedia\RiK TTW\data\models\sel.kimodel"
    #file=r"E:\AidemMedia\RiK TTW\data\models\players\blue\blue.kimodel"
    #file=r"E:\AidemMedia\RiK TTW\data\models\players\green\1green.kimodel"
    #file=r"E:\AidemMedia\RiK TTW\data\models\players\yellow\yellow.kimodel"
    #file=r"E:\AidemMedia\RiK TTW\data\models\levels\planet_monolith.kimodel"

    with open(file,"rb") as f:
        data=f.read()
        
        
    vertOff=st.unpack_from("<I", data, offset=28)[0]
    loopOff=st.unpack_from("<I", data, offset=16)[0]
    vertNum=st.unpack_from("<I", data, offset=36)[0]
    loopNum=st.unpack_from("<I", data, offset=24)[0]


    vertices = []
    loops = [] 
    uvs = []

    for i in range(0,vertNum):
        if(vertOff+16>len(data)):
            break
        [x,vertOff]=read(vertOff,"<f",data)
        vertices.append(x)
        [y,vertOff]=read(vertOff,"<f",data)
        [z,vertOff]=read(vertOff,"<f",data)
        vertices.append(z)
        vertices.append(y)
        vertOff+=4*4
        [x,vertOff]=read(vertOff,"<f",data)
        [y,vertOff]=read(vertOff,"<f",data)
        uvs.append((x,1-y))
        vertOff+=4*8

    for i in range(0,loopNum):
        [l,loopOff]=(read(loopOff,"<I",data))
        loops.append(l)

    return vertices, loops, uvs

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
    


    def blendCreateObject(name, vertices, loops, uvs):
        vertNum=int(len(vertices)/3)
        loopNum=len(loops)
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
                print(f.name)
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

    if __name__ == "__main__":
        register()
except ModuleNotFoundError as err:
    pass