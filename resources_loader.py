class ResourceLoader:
    load_model = None
    load_texture = None

    loaded_models = {}
    loaded_textures = {}

    def init(mesh):
        ResourceLoader.load_model = mesh.set_3d_model
        ResourceLoader.load_texture = mesh.set_texture
