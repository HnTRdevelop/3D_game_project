class Collider:
    def __init__(self, x, y, z, vx, vy, vz, mass, static=False):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.mass = mass
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
                            self.vx /= coefficient(self.mass, another.mass)
                            another.vx *= coefficient(self.mass, another.mass)
                        else:
                            if self.vx * self.mass == another.vx * another.mass:
                                self.vx = -self.vx
                                another.vx = -another.vx
                            elif self.vx * self.mass > another.vx * another.mass:
                                self.vx /= coefficient(self.mass, another.mass)
                                another.vx *= -coefficient(self.mass, another.mass)
                            else:
                                self.vx /= -coefficient(self.mass, another.mass)
                                another.vx *= coefficient(self.mass, another.mass)
                    else:
                        if self.vx > 0 and another.vx > 0 or self.vx > 0 and another.vx > 0:
                            self.vx /= coefficient(self.mass, another.mass)
                            self.vy += coefficient(self.mass, another.mass)
                            another.vx *= coefficient(self.mass, another.mass)
                            another.vy -= coefficient(self.mass, another.mass)
                        else:
                            if self.vx * self.mass == another.vx * another.mass:
                                self.vx = -self.vx
                                another.vx = -another.vx
                                self.vy += coefficient(self.mass, another.mass)
                                another.vy -= coefficient(self.mass, another.mass)
                            elif self.vx * self.mass > another.vx * another.mass:
                                self.vx /= coefficient(self.mass, another.mass)
                                another.vx *= -coefficient(self.mass, another.mass)
                                self.vy += coefficient(self.mass, another.mass)
                                another.vy -= coefficient(self.mass, another.mass)
                            else:
                                self.vx /= -coefficient(self.mass, another.mass)
                                another.vx *= coefficient(self.mass, another.mass)
                                self.vy += coefficient(self.mass, another.mass)
                                another.vy -= coefficient(self.mass, another.mass)
                else:
                    if another.vz == 0:
                        if self.vx > 0 and another.vx > 0 or self.vx > 0 and another.vx > 0:
                            self.vx /= coefficient(self.mass, another.mass)
                            self.vy -= coefficient(self.mass, another.mass)
                            another.vx *= coefficient(self.mass, another.mass)
                            another.vy += coefficient(self.mass, another.mass)
                        else:
                            if self.vx * self.mass == another.vx * another.mass:
                                self.vx = -self.vx
                                another.vx = -another.vx
                                self.vy -= coefficient(self.mass, another.mass)
                                another.vy += coefficient(self.mass, another.mass)
                            elif self.vx * self.mass > another.vx * another.mass:
                                self.vx /= coefficient(self.mass, another.mass)
                                another.vx *= -coefficient(self.mass, another.mass)
                                self.vy -= coefficient(self.mass, another.mass)
                                another.vy += coefficient(self.mass, another.mass)
                            else:
                                self.vx /= -coefficient(self.mass, another.mass)
                                another.vx *= coefficient(self.mass, another.mass)
                                self.vy -= coefficient(self.mass, another.mass)
                                another.vy += coefficient(self.mass, another.mass)
                    else:
                        if self.vx > 0 and another.vx > 0 or self.vx > 0 and another.vx > 0:
                            self.vx /= coefficient(self.mass, another.mass)
                            self.vy /= coefficient(self.mass, another.mass)
                            another.vx *= coefficient(self.mass, another.mass)
                            another.vy *= coefficient(self.mass, another.mass)
                        else:
                            if self.vx * self.mass == another.vx * another.mass:
                                self.vx = -self.vx
                                another.vx = -another.vx
                                if self.vx * self.mass == another.vy * another.mass:
                                    self.vy = -self.vy
                                    another.vy = -another.vy
                                else:
                                    self.vy += coefficient(self.mass, another.mass)
                                    another.vy -= coefficient(self.mass, another.mass)
                            elif self.vx * self.mass > another.vx * another.mass:
                                self.vx /= coefficient(self.mass, another.mass)
                                another.vx *= -coefficient(self.mass, another.mass)
                                self.vy += coefficient(self.mass, another.mass)
                                another.vy -= coefficient(self.mass, another.mass)
                            else:
                                self.vx /= -coefficient(self.mass, another.mass)
                                another.vx *= coefficient(self.mass, another.mass)
                                self.vy += coefficient(self.mass, another.mass)
                                another.vy -= coefficient(self.mass, another.mass)


def coefficient(m1, m2):
    return (m1 / m2) if (m1 / m2) > 1 else (m2 / m1)