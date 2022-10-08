
import cv2

def gray_scale_img(img_3_chanels, type):

    def formula(bgr):
        return 0.114*bgr[0] + 0.587*bgr[1] + 0.299*bgr[2]

    def _max(bgr):
        return max(bgr)

    def average(bgr):
        return (bgr[0] + bgr[1] + bgr[2]) / 3

    def ligthness(bgr):
        return (max(bgr) + min(bgr)) / 2

    h, w, c = img_3_chanels.shape
    gray_img = img_3_chanels.copy()

    if type == 'cv2':
        for y in range(h):
            for x in range(w):
                gray_img[y][x] = formula(img_3_chanels[y][x])
    if type == 'max':
        for y in range(h):
            for x in range(w):
                gray_img[y][x] = _max(img_3_chanels[y][x])   
    if type == 'average':
        for y in range(h):
            for x in range(w):
                gray_img[y][x] = average(img_3_chanels[y][x]) 
    if type == 'ligthness':
        for y in range(h):
            for x in range(w):
                gray_img[y][x] = ligthness(img_3_chanels[y][x])
    
    return gray_img

img = cv2.imread('./a.jpg')
scale_img = gray_scale_img(img, 'cv2')
scale_img1 = gray_scale_img(img, 'max')
scale_img2 = gray_scale_img(img, 'average')
scale_img3 = gray_scale_img(img, 'ligthness')
cv2.imshow('3c', img)

cv2.imshow('cv2', scale_img)
cv2.imshow('max', scale_img1)
cv2.imshow('average', scale_img2)
cv2.imshow('ligthness', scale_img3)
cv2.waitKey(0)
cv2.destroyAllWindows()


