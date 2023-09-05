import bpy
import math
import numpy as np
import os

rep=os.getcwd()
reparr=os.path.abspath(os.path.join(rep,os.pardir))
reparr=os.path.abspath(os.path.join(reparr,os.pardir))




CUBE=bpy.data.objects[0]
bpy.data.objects.remove(CUBE,do_unlink=True)
all_objects=bpy.data.objects

for obj in all_objects:
    if obj.type!='CAMERA' and obj.type !='LIGHT':
        bpy.data.objects.remove(obj,do_unlink=True)
        

def mat(filepath):
    material = bpy.data.materials.new(name="mat1")
    # Activer le mode d'édition du matériau
    material.use_nodes = True

    # Récupérer le nœud principal du matériau
    nodes = material.node_tree.nodes
    principled_node = nodes.get("BSDF guidée")

    # Ajouter un nœud Image Texture
    image_texture_node = nodes.new("ShaderNodeTexImage")
    # Charger l'image à utiliser comme texture
    image_texture_node.image = bpy.data.images.load(filepath=filepath)
    # Positionner le nœud Image Texture
    image_texture_node.location = (-200, 200)

    # Connecter le nœud Image Texture au nœud Principled BSDF
    material.node_tree.links.new(image_texture_node.outputs["Color"], principled_node.inputs["Base Color"])
    return material

path_acier=os.path.join(reparr,"api","acier.jpg")
path_bois=os.path.join(reparr,"api","bois.jpg")
acier=mat(r"C:\Users\adikp\OneDrive\Desktop\site pergola\api\acier.jpg")
bois=mat(r"C:\Users\adikp\OneDrive\Desktop\site pergola\api\bois.jpg")

def add_roof(x,y,z,col):
    tissu = mat(col)

    # Créer le toit de la pergola
    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
    bpy.ops.transform.resize(value=(2.2, 3.2, 0))
    obj = bpy.context.object
    obj.data.materials.append(tissu)
    
    bpy.ops.mesh.primitive_cube_add(location=(x+2.3,y+3.2,z))
    bpy.ops.transform.resize(value=(0.1, 0.6, 0))
    bpy.ops.transform.rotate(value=math.radians(45), 
            orient_axis='Z', orient_type='GLOBAL')
    obj = bpy.context.object
    obj.data.materials.append(tissu)
    bpy.ops.mesh.primitive_cube_add(location=(x-2.3,y+3.2,z))
    bpy.ops.transform.resize(value=(0.1, 0.6, 0))
    bpy.ops.transform.rotate(value=math.radians(-45), 
            orient_axis='Z', orient_type='GLOBAL')
    obj = bpy.context.object
    obj.data.materials.append(tissu)
    bpy.ops.mesh.primitive_cube_add(location=(x+2.3,y-3.2,z))
    bpy.ops.transform.resize(value=(0.1, 0.6, 0))
    bpy.ops.transform.rotate(value=math.radians(-45), 
            orient_axis='Z', orient_type='GLOBAL')
    obj = bpy.context.object
    obj.data.materials.append(tissu)
    bpy.ops.mesh.primitive_cube_add(location=(x-2.3,y-3.2,z))
    bpy.ops.transform.resize(value=(0.1, 0.6, 0))
    bpy.ops.transform.rotate(value=math.radians(45), 
            orient_axis='Z', orient_type='GLOBAL')
    obj = bpy.context.object
    obj.data.materials.append(tissu)


def add_roof_ouv(x,y,z):
   
    for i in range(3):     
           bpy.ops.mesh.primitive_cube_add(location=(x-1.5+i*1.5,y,z))
           bpy.ops.transform.resize(value=(0.2,7.8/2,0.2))
           obj=bpy.context.object
           obj.data.materials.append(bois)
        
           
    # for i in range(3):    
    #         bpy.ops.mesh.primitive_cube_add(location=(x,y-1.8+i*1.8,z))
    #         bpy.ops.transform.resize(value=(3,0.2,0.2))
           
           obj=bpy.context.object
           obj.data.materials.append(bois)  
    
def pergola(pos,t,type,color):
    a=t-4
    row = pos[0]
    col = pos[1]
    support_name = []
    
    for i in range(2):
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,row*7.8,0))
        bpy.ops.transform.resize(value=(0.2,0.2,t))
        obj=bpy.context.object
        obj.data.materials.append(bois)
        
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,row*7.8,-3.8-a))
        bpy.ops.transform.resize(value=(0.22,0.22,0.4))
        obj=bpy.context.object
        obj.data.materials.append(acier)
        
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,row*7.8,3.8+a))
        bpy.ops.transform.resize(value=(0.22,0.22,0.4))
        obj=bpy.context.object
        obj.data.materials.append(acier)
   
        
    for i in range(2):
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,(row+1)*7.8,0))
        bpy.ops.transform.resize(value=(0.2,0.2,t))
        obj=bpy.context.object
        obj.data.materials.append(bois)
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,(row+1)*7.8,-3.8-a))
        bpy.ops.transform.resize(value=(0.22,0.22,0.4))
        obj=bpy.context.object
        obj.data.materials.append(acier)
        
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,(row+1)*7.8,3.8+a))
        bpy.ops.transform.resize(value=(0.22,0.22,0.4))
        obj=bpy.context.object
        obj.data.materials.append(acier)
  
        
    ## Créer les poutres pour la pergola
    for i in range(2):
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,7.8/2+row*7.8,t))
        bpy.ops.transform.resize(value=(0.2,7.8/2,0.2))
        obj=bpy.context.object
        obj.data.materials.append(bois)
    
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,0.2+row*7.8,t))
        bpy.ops.transform.resize(value=(0.22,0.4,0.22))
        obj=bpy.context.object
        obj.data.materials.append(acier)
        
        bpy.ops.mesh.primitive_cube_add(location=((i+col)*6,7.6+row*7.8,t))        
        bpy.ops.transform.resize(value=(0.22,0.4,0.22))
        obj=bpy.context.object
        obj.data.materials.append(acier)
#     

    # Créer les poutres transversales pour la pergola
    for i in range(2):
        bpy.ops.mesh.primitive_cube_add(location=(col*6+3,(row+i)*7.8,t))
        bpy.ops.transform.resize(value=(3,0.2,0.2))
        obj=bpy.context.object
        obj.data.materials.append(bois)
      
        bpy.ops.mesh.primitive_cube_add(location=(5.8+col*6,(row+i)*7.8,t))
        bpy.ops.transform.resize(value=(0.4,0.22,0.22)) 
        obj=bpy.context.object
        obj.data.materials.append(acier)       
   
        bpy.ops.mesh.primitive_cube_add(location=(0.2+col*6,(row+i)*7.8,t))        
        bpy.ops.transform.resize(value=(0.4,0.22,0.22))  
        obj=bpy.context.object
        obj.data.materials.append(acier)      
       
        if type=="fermee":
         add_roof(col*6+3,row*7.8+7.8/2,z=t,col=color)
        if type=="ouvert":
          add_roof_ouv(col*6+3,row*7.8+7.8/2,z=t)
           
           

def construire(perg,type,color,t,filename):       

        for i in range(3):
                for j in range(4):
                        if perg[i][j]==1:
                           pergola((i,j),t,type,color=color)

        cubes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.name.startswith("Cube")]

        #     Joindre tous les cubes en un seul objet
        bpy.ops.object.select_all(action='DESELECT')
        for cube in cubes:
                cube.select_set(True)
        bpy.context.view_layer.objects.active = cubes[0]
        bpy.ops.object.join()   
        # Configurez les paramètres d'export FBX
        # fbx_export_settings = {
        # 'filepath': filename,
        # 'path_mode': 'COPY',
        # 'embed_textures': True,
        # 'axis_forward': 'Y',
        # 'axis_up' :'Z'
        # }
        # bpy.ops.export_scene.fbx(**fbx_export_settings)
     

        # Paramètres de l'exportateur
        export_settings = {
    'filepath': filename,
    'filter_glob': '*.glb',
    # 'export_format': 'GLTF_SEPARATE',
      # Attention : chaîne de caractères !
    
    
}
        bpy.ops.export_scene.gltf(**export_settings)




import sys
import ast
# Parse command line arguments
if len(sys.argv) > 4 and sys.argv[4] == "--":
    function_name = sys.argv[5]
    param1 = sys.argv[6]
    matrice = ast.literal_eval(param1)
    path = sys.argv[7]
    type = sys.argv[8]
    color = sys.argv[9]
    height = sys.argv[10]
    height = ast.literal_eval(height)
    
    # print(color)
    # print(type)
    # print(height)
    # print(matrice)
    # Call function with parameters
    construire(matrice,type,color,height,path)