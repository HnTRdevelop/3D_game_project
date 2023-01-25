import math
import glm


class Collider:
    def __init__(self, x, y, z, vx, vy, vz, mass, width, height, length, static=False):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass
        self.width = width
        self.height = height
        self.length = length
        self.position = glm.vec3(self.x, self.y, self.z)

        self.static = static

    def get_meet_point(self, another):
        if self.check_meeting(another):
            space1 = self.get_hired_space(self.x, self.width, self.y, self.height, self.z, self.length)
            space2 = another.get_hired_space(another.x, another.width, another.y, another.height, another.z,
                                             another.length)
            point = glm.vec3()
            if self.position[0] > another.position[0]:  # Какое тело находится дольше на оси
                point[0] = self.position[0] - len(range(max(space2[0]), min(space1[0])))
                # Место Встречи с некоторой погрешностью, что, полагаю, не очень критично
            else:
                point[0] = another.position[0] - len(range(max(space1[0]), min(space2[0])))
            if self.position[1] > another.position[1]:
                point[1] = self.position[1] - len(range(max(space2[1]), min(space1[1])))
            else:
                point[1] = another.position[1] - len(range(max(space1[1]), min(space2[1])))
            if self.position[2] > another.position[2]:
                point[2] = self.position[2] - len(range(max(space2[2]), min(space1[2])))
            else:
                point[2] = another.position[2] - len(range(max(space1[2]), min(space2[2])))
            return point
        else:
            return None

    def get_hired_space(self, x, width, y, height, z,  length):  # Занятое телом место
        x_space = x, x + width
        y_space = y, y + height
        z_space = z, z + length
        return x_space, y_space, z_space

    def check_meeting(self, another):
        space1 = self.get_hired_space(self.x, self.width, self.y, self.height, self.z, self.length)
        space2 = another.get_hired_space(another.x, another.width, another.y, another.height, another.z, another.length)
        if min(space1[0]) <= max(space2[0]) and min(space2[0]) <= max(space1[0]):
            if min(space1[1]) <= max(space2[1]) and min(space2[1]) <= max(space1[1]):
                if min(space1[2]) <= max(space2[2]) and min(space2[2]) <= max(space1[2]):
                    return True
        else:
            return False

    def movement(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        # if self.vx >= 1:
        #     self.vx -= 1
        # if self.vz >= 1:
        #     self.vz -= 1
        # if self.vy <= 0:
        #     self.vy += 1

    def bump(self, another):
        if not another.static:
            if self.mass >= another.mass:
                if self.vx >= 0 and another.vx >= 0 or self.vx <= 0 and another.vx <= 0:
                    if self.mass * self.vx > another.mass * another.vx:
                        self.vx, another.vx = counting_speed(self.mass, self.vx, another.mass, another.vx,
                                                             chase=True, opposite=False)
                    else:
                        self.vx, another.vx = counting_speed(self.mass, self.vx, another.mass, another.vx,
                                                             chase=True, opposite=True)
                else:
                    if self.mass * self.vx > another.mass * another.vx:
                        self.vx, another.vx = counting_speed(self.mass, self.x, another.mass, another.vx,
                                                             chase=False, opposite=False)
                    else:
                        self.vx, another.vx = counting_speed(self.mass, self.x, another.mass, another.vx,
                                                             chase=False, opposite=True)
                if self.vz >= 0 and another.vz >= 0 or self.vz <= 0 and another.vz <= 0:
                    if self.mass * self.vz > another.mass * another.vz:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=True, opposite=False)
                    else:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=True, opposite=True)
                else:
                    if self.mass * self.vz > another.mass * another.vz:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=False, opposite=False)
                    else:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=False, opposite=True)
                if self.vy >= 0 and another.vy >= 0 or self.vy <= 0 and another.vy <= 0:
                    if self.mass * self.vy > another.mass * another.vy:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=True, opposite=False)
                    else:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=True, opposite=True)
                else:
                    if self.mass * self.vy > another.mass * another.vy:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=False, opposite=False)
                    else:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=False, opposite=True)
            else:
                if self.vx >= 0 and another.vx >= 0 or self.vx <= 0 and another.vx <= 0:
                    if self.mass * self.vx > another.mass * another.vx:
                        self.vx, another.vx = counting_speed(self.mass, self.vx, another.mass, another.vx,
                                                             chase=True, opposite=True)
                    else:
                        self.vx, another.vx = counting_speed(self.mass, self.vx, another.mass, another.vx,
                                                             chase=True, opposite=False)
                else:
                    if self.mass * self.vx > another.mass * another.vx:
                        self.vx, another.vx = counting_speed(self.mass, self.x, another.mass, another.vx,
                                                             chase=False, opposite=True)
                    else:
                        self.vx, another.vx = counting_speed(self.mass, self.x, another.mass, another.vx,
                                                             chase=False, opposite=False)
                if self.vz >= 0 and another.vz >= 0 or self.vz <= 0 and another.vz <= 0:
                    if self.mass * self.vz > another.mass * another.vz:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=True, opposite=True)
                    else:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=True, opposite=False)
                else:
                    if self.mass * self.vz > another.mass * another.vz:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=False, opposite=True)
                    else:
                        self.vz, another.vz = counting_speed(self.mass, self.vz, another.mass, another.vz,
                                                             chase=False, opposite=False)
                if self.vy >= 0 and another.vy >= 0 or self.vy <= 0 and another.vy <= 0:
                    if self.mass * self.vy > another.mass * another.vy:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=True, opposite=True)
                    else:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=True, opposite=False)
                else:
                    if self.mass * self.vy > another.mass * another.vy:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=False, opposite=True)
                    else:
                        self.vy, another.vy = counting_speed(self.mass, self.vy, another.mass, another.vy,
                                                             chase=False, opposite=False)
        else:
            now_range = range(another.x, another.x - another.vx + 2) if another.x < another.x - another.vx else\
                range(another.x - another.vx, another.x + 2)
            if self.x - self.vx not in now_range:
                self.x *= -1
                return None
            now_range = range(another.y, another.y - another.vy + 2) if another.y < another.y - another.vy else \
                range(another.y - another.vy, another.y + 2)
            if self.y - self.vy not in now_range:
                self.y *= -1
                return None
            now_range = range(another.z, another.z - another.vz + 2) if another.z < another.z - another.vz else \
                range(another.xz - another.vz, another.z + 2)
            if self.z - self.vz not in now_range:
                self.z *= -1
                return None


def counting_speed(m1, v1, m2, v2, chase=False, opposite=False):
    # Формулы найдены из ЗСИ и ЗСЭ
    # Абсолютно упругий удар, неупругий учитывать не обязательно, он энивэй выглядит некруто :)
    if chase:  # Движение вдогонку
        impulse = m1 * v1 + m2 * v2
        if not opposite:
            need_v2_1 = (3 * m1 * v1 + 2 * m2 * v2 - m1 * v2) / (2 * (m2 + m1))
            need_v2_2 = (2 * m2 * v2 + m1 * (v1 + v2)) / (2 * (m1 + m2))
            if not (need_v2_1 <= math.sqrt((m1 * v1 ** 2 + m2 * v2 ** 2) / m2) and need_v2_1 <= impulse / m2):
                need_v2 = need_v2_2
            else:
                need_v2 = need_v2_1
            need_v1 = (impulse - m2 * need_v2) / m1
            return need_v1, need_v2
        else:
            need_v2_1 = -(2 * m2 * v2 + m1 * v1 + m1 * v2) / (2 * (m2 + m1))
            need_v2_2 = (m1 * v2 - 3 * m1 * v1 - 2 * m2 * v2) / (2 * (m1 + m2))
            if not ((need_v2_1 <= math.sqrt((m1 * v1 ** 2 + m2 * v2 ** 2) / m2)) and (need_v2_1 >= impulse / m2)):
                need_v2 = need_v2_2
            else:
                need_v2 = need_v2_1
            need_v1 = (impulse - m2 * need_v2) / m1
            return need_v1, need_v2
    else:  # Встречное движение
        impulse = abs(m1 * v1 - m2 * v2)
        if not opposite:
            need_v2_1 = (3 * m1 * v1 - 2 * m2 * v2 - m1 * v2) / (2 * (m1 + m2))
            need_v2_2 = (m1 * v1 - 2 * m2 * v2 - m1 * v2) / (2 * (m1 + m2))
            if not (need_v2_1 <= math.sqrt((m1 * v1 ** 2 + m2 * v2 ** 2) / m2) and need_v2_1 <= impulse / m2):
                need_v2 = need_v2_2
            else:
                need_v2 = need_v2_1
            need_v1 = (impulse - m2 * need_v2) / m1
            return need_v1, need_v2
        else:
            need_v2_1 = (2 * (m2 ** 2 * v2 - m1 * m2 * v1) +
                         math.sqrt(m2 ** 2 * v2 * (m2 - 1) * (m2 + m1) + (m1 * m2 * v1 + m1 * m2 * v2) ** 2)) / (
                                2 * m2 * (m2 + m1))
            need_v2_2 = (2 * (m2 ** 2 * v2 - m1 * m2 * v1) -
                         math.sqrt(m2 ** 2 * v2 * (m2 - 1) * (m2 + m1) + (m1 * m2 * v1 + m1 * m2 * v2) ** 2)) / (
                                2 * m2 * (m2 + m1))
            if not ((need_v2_1 <= math.sqrt((m1 * v1 ** 2 + m2 * v2 ** 2) / m2)) and (need_v2_1 >= impulse / m2)):
                need_v2 = need_v2_2
            else:
                need_v2 = need_v2_1
            need_v1 = (impulse - m2 * need_v2) / m1
            return need_v1, need_v2
