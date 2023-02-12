def load_resources(mesh):
    load_3d_model = mesh.set_3d_model
    load_texture = mesh.set_texture

    load_3d_model("cat_model", "models/cat.obj")

    load_texture("cat_texture", "textures/cat.jpg")
