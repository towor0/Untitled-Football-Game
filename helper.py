import math


def posToAngle(pos1, pos2):
    return math.atan2(pos1[1] - pos2[1], pos2[0] - pos1[0]) * 180 / math.pi + 180


def angleSpeed(speed, pos1, pos2):
    rad = math.radians(360) - math.radians(posToAngle(pos1, pos2))
    return [math.cos(rad) * speed, math.sin(rad) * speed]


def root(r, num):
    return math.pow(num, 1 / r)
