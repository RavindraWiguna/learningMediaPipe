import cv2
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