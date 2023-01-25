import math
import glm


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
