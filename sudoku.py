# sudo -_-

import cv2
import operator
import math
import numpy as np
from matplotlib import pyplot as plt
from keras.models import load_model
from cv2 import cv2


def show_image(img):

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def plot_many_images(images, titles, rows=1, columns=2):

    for i, image in enumerate(images):
        plt.subplot(rows, columns, i+1)
        plt.imshow(image, 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])  # Hide tick marks

    plt.show()


def display_points(in_img, points, radius=10, colour=(0, 255, 0)):

    img = in_img.copy()
    if len(colour) == 3:
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for point in points:
        img = cv2.circle(img, tuple(int(x) for x in point), radius, colour, -1)

    show_image(img)

    return img


def display_rects(in_img, rects, colour=255):

    img = in_img.copy()
    for rect in rects:
        img = cv2.rectangle(img, tuple(int(x)
                                       for x in rect[0]), tuple(int(x) for x in rect[1]), colour)
    show_image(img)
    # return img

# Blur image to reduce noise obtained in thresholding algorithm
# Binary Thresholding - makes split of either 0/1 on basis of threshold measured from entire image
# Adaptive Thresholding - calculates threshold for each pixel based on mean value of surrounding pixels
# Dilate image to increase thickness of lines


def preprocess_img(img, skip_dilate=False):
    # Gaussian blur with a kernel size (height, width)
    blur = cv2.GaussianBlur(img.copy(), (9, 9), 0)

    # cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, constant(c))
    # the threshold value T(x, y) is a weighted sum (cross-correlation with a Gaussian window) of {blockSize} x {blockSize} neighborhood of (x, y) minus C
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # to make gridlines have non-zero pixel values, we will invert the colors
    preprocess = cv2.bitwise_not(thresh, thresh)

    if not skip_dilate:
        kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]])
        preprocess = cv2.dilate(preprocess, np.uint8(kernel))

    # plot_many_images([blur, thresh, bitwise, preprocess], [
    #                  "blur", "thresh", "bitwise", "dilate"], rows=2)

    return preprocess


def plot_external_contours(processed_image):
    # findContours: boundaries of shapes having same intensity
    # CHAIN_APPROX_SIMPLE - stores only minimal information of points to describe contour
    # RETR_EXTERNAL gives "outer" contours, so if you have (say) one contour enclosing another (like concentric circles), only the outermost is given.

    contours, _ = cv2.findContours(
        processed_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)

    contours = cv2.drawContours(
        processed_image.copy(), contours, -1, (0, 255, 0), 2)

    show_image(contours)


def get_corners_of_largest_poly(img):
    # cv2.ContourArea(): Finds area of outermost polygon(largest feature) in img.
    # Ramer Doughlas Peucker algorithm: Approximate no of sides of shape(filter rectangle objects only).

    contours, h = cv2.findContours(
        img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,
                      reverse=True)  # Sort by area, descending

    polygon = contours[0]  # get largest contour

    # operator.itemgetter - get index of point
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1]
                                     for pt in polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1]
                                 for pt in polygon]), key=operator.itemgetter(1))
    bottom_left, _ = max(enumerate([pt[0][0] - pt[0][1]
                                    for pt in polygon]), key=operator.itemgetter(1))
    top_right, _ = min(enumerate([pt[0][0] - pt[0][1]
                                  for pt in polygon]), key=operator.itemgetter(1))

    return [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]


def infer_sudoku_puzzle(image, crop_rectangle):
    # wrapPerspective: implementation of perspective transform equation.
    # https://docs.opencv.org/3.1.0/da/d6e/tutorial_py_geometric_transformations.html

    # Map four coords from og img to new locations in new img
    # https://wp.optics.arizona.edu/visualopticslab/wp-content/uploads/sites/52/2016/08/Lectures6_7.pdf

    img = image
    crop_rect = crop_rectangle

    def distance_between(a, b):  # scalar distance between a and b
        return np.sqrt(((b[0] - a[0]) ** 2) + ((b[1] - a[1]) ** 2))

    def crop_img():  # crops rectangular portion from image and wraps it into a square of similar size
        top_left, top_right, bottom_right, bottom_left = crop_rect[
            0], crop_rect[1], crop_rect[2], crop_rect[3]

        # float for perspective transformation
        source_rect = np.array(
            np.array([top_left, bottom_left, bottom_right, top_right], dtype='float32'))

        side = max([
            distance_between(bottom_right, top_right),
            distance_between(top_left, bottom_left),
            distance_between(bottom_right, bottom_left),
            distance_between(top_left, top_right)
        ])

        dest_square = np.array(
            [[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')

        # Skew the image by comparing 4 before and after points -- return matrix
        m = cv2.getPerspectiveTransform(source_rect, dest_square)

        # Perspective Transformation on original image
        return cv2.warpPerspective(img, m, (int(side), int(side)))

    return crop_img()


def infer_grid(img):  # infer 81 cells from image
    squares = []
    side = img.shape[:1]

    side = side[0] / 9

    for i in range(9):  # get each box and append it to squares -- 9 rows, 9 cols
        for j in range(9):
            p1 = (i*side, j*side)  # top left corner of box
            p2 = ((i+1)*side, (j+1)*side)  # bottom right corner of box
            squares.append((p1, p2))
    return squares


def extract_number(sudoku, loaded_model):
    sudoku = cv2.resize(sudoku, (450, 450))
    show_image(sudoku)

    # split sudoku
    grid = np.zeros([9, 9])
    for i in range(9):
        for j in range(9):
            #            image = sudoku[i*50+3:(i+1)*50-3,j*50+3:(j+1)*50-3]
            image = sudoku[i*50:(i+1)*50, j*50:(j+1)*50]
            image=preprocess_img(image, True)
#            filename = "images/sudoku/file_%d_%d.jpg"%(i, j)
#            cv2.imwrite(filename, image)
            # show_image(image)
            if image.sum() > 25000:
                grid[i][j] = identify_number(image, loaded_model)
            else:
                grid[i][j] = 0
    return grid.astype(int)

# evaluate loaded model on test data


# def n10():
# 	img = np.zeros((50, 50, 3), np.uint8)
# 	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 	roi = img[:,:]
# 	return roi

# def getRoi(box):
# 	padding = 5
# 	contours, _ = cv2.findContours(box, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 	for cnt in contours:
# 		[x,y,w,h] = cv2.boundingRect(cnt)
# 		if(h > 15 and w > 5 and x > padding/2 and y > padding/2):
# 			roi = box[y:y+h,x:x+w]
# 			roi = cv2.resize(roi,(28,28))
# 			return roi
# 	return n10()


def identify_number(image, loaded_model):
    image = cv2.resize(image, (28, 28))
    # show_image(image)
    # For input to model.predict_classes
    image_resize_2 = image.reshape((1, 28, 28, 1))
    loaded_model_pred = loaded_model.predict_classes(image_resize_2)
    # print('Prediction of loaded_model: {}'.format(loaded_model_pred[0]))
    return loaded_model_pred[0]


def main():
    img = cv2.imread('images/sudoku1.jpg', cv2.IMREAD_GRAYSCALE)
    loaded_model = load_model("models/model")
    print("Loaded saved model from disk.")

    processed_sudoku = preprocess_img(img)

    plot_external_contours(processed_sudoku)
    corners_of_sudoku = get_corners_of_largest_poly(processed_sudoku)
    display_points(processed_sudoku, corners_of_sudoku)
    cropped_sudoku = infer_sudoku_puzzle(img, corners_of_sudoku)
    # show_image(cropped_sudoku)
    squares_on_sudoku = infer_grid(cropped_sudoku)
    display_rects(cropped_sudoku, squares_on_sudoku)
    # loadModel()
    grid = extract_number(cropped_sudoku, loaded_model)
    print(grid)


if __name__ == '__main__':
    main()
