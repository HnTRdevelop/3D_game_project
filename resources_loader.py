def load_resources(mesh):
    mesh.set_vbo("cat", "models/cat.obj")
    mesh.set_vbo("cube", "models/cube.obj")
    mesh.set_vbo("rainbow_dash", "models/rainbow.obj")
    mesh.set_vbo("twilight", "models/twilight.obj")

    mesh.set_vao("cube", "default", "cube")
    mesh.set_vao("cat", "default", "cat")
    mesh.set_vao("rainbow_dash", "default", "rainbow_dash")
    mesh.set_vao("twilight", "default", "twilight")

    mesh.set_texture("wooden_box", "textures/wooden_box0.jpg")
    mesh.set_texture("cat", "textures/cat.jpg")
    mesh.set_texture("grass0", "textures/grass0.jpg")
    mesh.set_texture("grass1", "textures/grass1.jpg")
    mesh.set_texture("dirt0", "textures/dirt0.jpg")