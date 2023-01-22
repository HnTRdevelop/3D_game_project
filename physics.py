import math


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
        self.static = static

    def movement(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        if self.vx >= 1:
            self.vx -= 1
        if self.vz >= 1:
            self.vz -= 1
        if self.vy <= 0:
            self.vy += 1

    def bump(self, another):
        if not another.static:
            if self.mass >= another.mass:
                if self.vz == 0:
                    if another.vz == 0:
                        if self.vx > 0 and another.vx >= 0 or self.vx < 0 and another.vx <= 0:
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


def counting_speed(m1, v1, m2, v2, chase=False, opposite=False):
    if chase:
        impulse = m1 * v1 + m2 * v2
        if not opposite:
            need_v2_1 = (3 * m1 * v1 + 2 * m2 * v2 - m1 * v2) / (2 * (m2 + m1))
            need_v2_2 = (2 * m2 * v2 + m1 * (v1 + v2)) / (2 * (m1 + m2))
            if not (need_v2_1 < math.sqrt((m1 * v1 ** 2 + m2 * v2 ** 2) / m2) and need_v2_1 < impulse / m2):
                need_v2 = need_v2_2
            else:
                need_v2 = need_v2_1
            need_v1 = (impulse - m2 * need_v2) / m1
            return need_v1, need_v2
        else:
            need_v2_1 = -(2 * m2 * v2 + m1 * v1 + m1 * v2) / (2 * (m2 + m1))
            need_v2_2 = (m1 * v2 - 3 * m1 * v1 - 2 * m2 * v2) / (2 * (m1 + m2))
            if not ((need_v2_1 < math.sqrt((m1 * v1 ** 2 + m2 * v2 ** 2) / m2)) and (need_v2_1 > impulse / m2)):
                need_v2 = need_v2_2
            else:
                need_v2 = need_v2_1
            need_v1 = (impulse - m2 * need_v2) / m1
            return need_v1, need_v2
    else:
        impulse = abs(m1 * v1 - m2 * v2)
        if not opposite:
            need_v2_1 = (3 * m1 * v1 - 2 * m2 * v2 - m1 * v2) / (2 * (m1 + m2))
            need_v2_2 = (m1 * v1 - 2 * m2 * v2 - m1 * v2) / (2 * (m1 + m2))
            if not (need_v2_1 < math.sqrt((m1 * v1 ** 2 + m2 * v2 ** 2) / m2) and need_v2_1 < impulse / m2):
                need_v2 = need_v2_2
            else:
                need_v2 = need_v2_1
            need_v1 = (impulse - m2 * need_v2) / m1
            return need_v1, need_v2
        else:
            pass
