import glm
from physics import counting_speed
from math import *


class BaseComponent:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner


class Transform(BaseComponent):
    def __init__(self, owner):
        super().__init__("Transform", owner)
        self.position = glm.vec3(0)
        self.rotation = glm.vec3(0)
        self.scale = glm.vec3(1)

    def translate(self, translation: glm.vec3):
        self.position += translation

    def rotate(self, rotation: glm.vec3):
        self.rotation += glm.radians(rotation)


class Model(BaseComponent):
    def __init__(self, app, owner, vao_name: str, texture_name: str = None):
        super().__init__("Model", owner)
        self.texture = None
        self.app = app
        self.texture_name = texture_name
        self.vao = self.app.mesh.vao_controller.vao_array[vao_name]
        self.shader_program = self.vao.program
        self.camera = self.app.camera
        self.on_init()

    def get_model_matrix(self):
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, self.owner.transform.position)

        model_matrix = glm.rotate(model_matrix, self.owner.transform.rotation.x, glm.vec3(1, 0, 0))
        model_matrix = glm.rotate(model_matrix, self.owner.transform.rotation.y, glm.vec3(0, 1, 0))
        model_matrix = glm.rotate(model_matrix, self.owner.transform.rotation.z, glm.vec3(0, 0, 1))

        model_matrix = glm.scale(model_matrix, self.owner.transform.scale)

        return model_matrix

    def on_init(self):
        self.texture = self.app.mesh.texture_controller.texture_array[self.texture_name]
        self.shader_program["u_texture"] = 0
        self.texture.use()

        self.shader_program["projection_matrix"].write(self.camera.projection_matrix)
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(self.get_model_matrix())

    def update(self):
        model_matrix = self.get_model_matrix()
        self.texture.use()
        self.shader_program["view_matrix"].write(self.camera.get_view_matrix())
        self.shader_program["model_matrix"].write(model_matrix)

    def render(self):
        self.update()
        self.vao.render()


class RigidBody(BaseComponent):
    def __init__(self, owner, mass: float = 1):
        super().__init__("RigidBody", owner)
        self.velocity = glm.vec3(0)
        self.angular_velocity = glm.vec3(0)
        self.mass = mass
        collider_component: Collider = self.owner.get_component("Collider")
        if collider_component in None:
            raise Exception("'RigidBody' component can't be created without 'Collider' component")
        self.collider = collider_component

    def move(self, delta_time: float):
        self.owner.transform.position += self.velocity * delta_time
        self.owner.transform.rotation += self.angular_velocity * delta_time

    def bump(self, other):
        if not other.static:
            if self.mass >= other.mass:
                if self.velocity.x >= 0 and other.velocity.x >= 0 or self.velocity.x <= 0 and other.velocity.x <= 0:
                    if self.mass * self.velocity.x > other.mass * other.velocity.x:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.velocity.x,
                                                                           other.mass, other.velocity.x,
                                                                           chase=True, opposite=False)
                    else:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.velocity.x,
                                                                           other.mass, other.velocity.x,
                                                                           chase=True, opposite=True)
                else:
                    if self.mass * self.velocity.x > other.mass * other.velocity.x:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.x, other.mass,
                                                                           other.velocity.x,
                                                                           chase=False, opposite=False)
                    else:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.x, other.mass,
                                                                           other.velocity.x,
                                                                           chase=False, opposite=True)
                if self.velocity.z >= 0 and other.velocity.z >= 0 or self.velocity.z <= 0 and other.velocity.z <= 0:
                    if self.mass * self.velocity.z > other.mass * other.velocity.z:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=True, opposite=False)
                    else:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=True, opposite=True)
                else:
                    if self.mass * self.velocity.z > other.mass * other.velocity.z:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=False, opposite=False)
                    else:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=False, opposite=True)
                if self.velocity.y >= 0 and other.velocity.y >= 0 or self.velocity.y <= 0 and other.velocity.y <= 0:
                    if self.mass * self.velocity.y > other.mass * other.velocity.y:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=True, opposite=False)
                    else:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=True, opposite=True)
                else:
                    if self.mass * self.velocity.y > other.mass * other.velocity.y:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=False, opposite=False)
                    else:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=False, opposite=True)
            else:
                if self.velocity.x >= 0 and other.velocity.x >= 0 or self.velocity.x <= 0 and other.velocity.x <= 0:
                    if self.mass * self.velocity.x > other.mass * other.velocity.x:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.velocity.x,
                                                                           other.mass, other.velocity.x,
                                                                           chase=True, opposite=True)
                    else:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.velocity.x,
                                                                           other.mass, other.velocity.x,
                                                                           chase=True, opposite=False)
                else:
                    if self.mass * self.velocity.x > other.mass * other.velocity.x:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.x,
                                                                           other.mass, other.velocity.x,
                                                                           chase=False, opposite=True)
                    else:
                        self.velocity.x, other.velocity.x = counting_speed(self.mass, self.x,
                                                                           other.mass, other.velocity.x,
                                                                           chase=False, opposite=False)
                if self.velocity.z >= 0 and other.velocity.z >= 0 or self.velocity.z <= 0 and other.velocity.z <= 0:
                    if self.mass * self.velocity.z > other.mass * other.velocity.z:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=True, opposite=True)
                    else:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=True, opposite=False)
                else:
                    if self.mass * self.velocity.z > other.mass * other.velocity.z:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=False, opposite=True)
                    else:
                        self.velocity.z, other.velocity.z = counting_speed(self.mass, self.velocity.z,
                                                                           other.mass, other.velocity.z,
                                                                           chase=False, opposite=False)
                if self.velocity.y >= 0 and other.velocity.y >= 0 or self.velocity.y <= 0 and other.velocity.y <= 0:
                    if self.mass * self.velocity.y > other.mass * other.velocity.y:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=True, opposite=True)
                    else:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=True, opposite=False)
                else:
                    if self.mass * self.velocity.y > other.mass * other.velocity.y:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=False, opposite=True)
                    else:
                        self.velocity.y, other.velocity.y = counting_speed(self.mass, self.velocity.y,
                                                                           other.mass, other.velocity.y,
                                                                           chase=False, opposite=False)
        else:
            velocity_angle = glm.normalize(glm.acos(self.velocity))
            new_velocity = glm.vec3(cos(-velocity_angle.x) * sin(-velocity_angle.z),
                                    sin(-velocity_angle.y),
                                    cos(-velocity_angle.z) * sin(-velocity_angle.x))


class Collider(BaseComponent):
    def __init__(self, owner, scale: glm.vec3 = glm.vec3(1), static: bool = False):
        super().__init__("Collider", owner)
        self.scale = scale
        self.static = static

    def get_meet_point(self, other):
        if self.check_meeting(other):
            self_space = self.get_hired_space()
            other_space = other.get_hired_space()
            point = glm.vec3(0)
            if self.owner.transform.position.x > other.owner.transform.position.x:  # Какое тело находится дольше на оси
                point.x = self.owner.transform.position.x - len(range(max(other_space[0]), min(self_space[0])))
                # Место Встречи с некоторой погрешностью, что, полагаю, не очень критично
            else:
                point.x = other.owner.transform.position.x - len(range(max(self_space[0]), min(other_space[0])))
            if self.owner.transform.position.y > other.owner.transform.position.y:
                point.y = self.owner.transform.position.y - len(range(max(other_space[1]), min(self_space[1])))
            else:
                point.y = other.owner.transform.position.y - len(range(max(self_space[1]), min(other_space[1])))
            if self.owner.transform.position.z > other.owner.transform.position.z:
                point.z = self.owner.transform.position.z - len(range(max(other_space[2]), min(self_space[2])))
            else:
                point.z = other.owner.transform.position.z - len(range(max(self_space[2]), min(other_space[2])))
            return point
        else:
            return None

    def get_hired_space(self):  # Занятое телом место
        x_space = self.owner.transform.position.x, self.owner.transform.position.x + self.scale.x
        y_space = self.owner.transform.position.y, self.owner.transform.position.y + self.scale.y
        z_space = self.owner.transform.position.z, self.owner.transform.position.z + self.scale.z
        return x_space, y_space, z_space

    def check_meeting(self, other):
        self_space = self.get_hired_space()
        other_space = other.get_hired_space()
        if min(self_space[0]) <= max(other_space[0]) and min(other_space[0]) <= max(self_space[0]):
            if min(self_space[1]) <= max(other_space[1]) and min(other_space[1]) <= max(self_space[1]):
                if min(self_space[2]) <= max(other_space[2]) and min(other_space[2]) <= max(self_space[2]):
                    return True
        else:
            return False
