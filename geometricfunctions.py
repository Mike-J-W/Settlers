import math
import sys


def pp_distance(pointA, pointB):
    xA = pointA[0]
    yA = pointA[1]
    xB = pointB[0]
    yB = pointB[1]
    return int(round(math.sqrt(math.pow(yB - yA, 2) + math.pow(xB - xA, 2))))


def get_closest_point(listOfPoints, point):
    if len(listOfPoints) == 0:
        return None
    closestPoint = (0, 0)
    minDistance = sys.maxsize
    for p in listOfPoints:
        newDistance = pp_distance(p, point)
        if newDistance < minDistance:
            minDistance = newDistance
            closestPoint = p
        if minDistance < 10:
            break
    return (closestPoint, minDistance)


def is_within_hex(hexObject, point):
    disFromCenter = pp_distance(hexObject.coordinates, point)
    if disFromCenter < hexObject.radius:
        return True
    return False


def is_within_rect(rectObject, point):
    if rectObject.left < point[0] < rectObject.right:
        if rectObject.top < point[1] < rectObject.bottom:
            return True
    return False
