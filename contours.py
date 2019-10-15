
# Extract contours and shapes(rectangles, hull) of objects 
# Steps
# 1. Read image
# 2. Convert to binary using thresholding
# 3. Extract contours
# 4. Fit rectangles using contours
# 5. Dispay the image with rectangles

#Ref:
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
#https://towardsdatascience.com/computer-vision-for-beginners-part-4-64a8d9856208
#https://stackoverflow.com/questions/40203932/drawing-a-rectangle-around-all-contours-in-opencv-python
#https://www.pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/


img = cv2.imread(#name of the image)
copy = img.copy()
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
image, contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

# straight rectangle
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    ROI = image[y:y+h, x:x+w]
	cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
    cv2.rectangle(copy,(x,y),(x+w,y+h), color=(255,0,0), thickness=2)
	ROI_number += 1
cv2.imshow('copy', copy)
cv2.waitKey()

# rotated rectangle
for c in contours:
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(copy, contours=[box], contourIdx=0, color=(255,0,0), thickness=2)
cv2.imshow('copy', copy)
cv2.waitKey()

# convex hull
for c in contours:
    hull = cv2.convexHull(c)
    cv2.drawContours(copy, contours=[hull], contourIdx=0, color=(255,0,36), thickness=2)
cv2.imshow('copy', copy)
cv2.waitKey()

# rectangular bounding box around all contours
boxes = []
for c in contours:
    (x, y, w, h) = cv2.boundingRect(c)
    boxes.append([x,y, x+w,y+h])

boxes = np.asarray(boxes)
# need an extra "min/max" for contours outside the frame
left = np.min(boxes[:,0])
top = np.min(boxes[:,1])
right = np.max(boxes[:,2])
bottom = np.max(boxes[:,3])

cv2.rectangle(copy, (left,top), (right,bottom), color=(255,0,0), thickness=2)
cv2.imshow('copy', copy)
cv2.waitKey()


# Finding extreme points in contours
# find contours in thresholded image, then grab the largest one
c = max(contours, key=cv2.contourArea)

# determine the most extreme points along the contour
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

# draw the outline of the object, then draw each of the
# extreme points, where the left-most is red, right-most
# is green, top-most is blue, and bottom-most is teal
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)
 
cv2.imshow("Image", image)
cv2.waitKey(0)






