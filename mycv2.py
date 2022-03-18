import cv2
from math import sqrt
import numpy as np

def createBoxWithText(text, fontScale, thickness, fontFace, RectangleColor, textColor):
    len_text = len(text)
    textWidth, textHeight = cv2.getTextSize(text, fontFace, fontScale, thickness)[0]
    avgPix = int(textWidth/len_text)
    # create np array with shape of rectangle filled with color
    filled_rect = np.full((textHeight+avgPix, textWidth+avgPix*2, 3), RectangleColor, np.uint8)
    # add the text
    cv2.putText(filled_rect, text, (avgPix, textHeight+avgPix//2), fontFace, fontScale, textColor, thickness, cv2.LINE_AA)
    return filled_rect

# Example USAGE:
# createBoxWithText("LEFT HAND", fontScale, 2, cv2.FONT_HERSHEY_SIMPLEX, RECT_COLOR, (255, 255, 255))
#============================================================================================================================
# calc distance between 2 points
def calcDistance(x1, y1, x2, y2):
    dx = x1-x2
    dy = y1-y2
    return sqrt(dx*dx + dy*dy)

# calculate middle point of lanmark, return x, y, isClose or no
def findMiddlePoint(point1, point2, width, height):
    x1,y1 = point1.x * width, point1.y * height
    x2, y2 = point2.x * width, point2.y * height

    midPoint = (int(( x1 + x2 ) / 2 ), int(( y1 + y2 ) / 2 ))

    return (midPoint, calcDistance(x1, y1, x2, y2) < 72.0)