import cv2
import operator
import math
import numpy as np
from matplotlib import pyplot as plt
from keras.models import load_model
from cv2 import cv2

from solver import solve

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


def infer_grid(img):
	"""Infers 81 cell grid from a square image."""
	squares = []
	side = img.shape[:1]
	side = side[0] / 9
	for i in range(9):
		for j in range(9):
			p1 = (i * side, j * side)  # Top left corner of a bounding box
			p2 = ((i + 1) * side, (j + 1) * side)  # Bottom right corner of bounding box
			squares.append((p1, p2))
	return squares


def extract_number(digits, loaded_model):
    # sudoku = cv2.resize(sudoku, (450, 450))

    # split sudoku
	k = 0
	show_image(digits[k])
	grid = np.zeros([9, 9])
	for i in range(9):
		for j in range(9):
			if digits[k].sum() > 2500:
				grid[j][i] = identify_number(digits[k], loaded_model)
			else:
				grid[j][i] = 0
			k=k+1
	return grid.astype(int)


def identify_number(image, loaded_model):
    image = cv2.resize(image, (28, 28))
    # show_image(image)
    # For input to model.predict_classes
    image_resize_2 = image.reshape((1, 28, 28, 1))
    loaded_model_pred = loaded_model.predict_classes(image_resize_2)
    # print('Prediction of loaded_model: {}'.format(loaded_model_pred[0]))
    return loaded_model_pred[0]


def cut_from_rect(img, rect):
	"""Cuts a rectangle from an image using the top left and bottom right points."""
	return img[int(rect[0][1]):int(rect[1][1]), int(rect[0][0]):int(rect[1][0])]


def scale_and_centre(img, size, margin=0, background=0):
	"""Scales and centres an image onto a new background square."""
	h, w = img.shape[:2]

	def centre_pad(length):
		"""Handles centering for a given length that may be odd or even."""
		if length % 2 == 0:
			side1 = int((size - length) / 2)
			side2 = side1
		else:
			side1 = int((size - length) / 2)
			side2 = side1 + 1
		return side1, side2

	def scale(r, x):
		return int(r * x)

	if h > w:
		t_pad = int(margin / 2)
		b_pad = t_pad
		ratio = (size - margin) / h
		w, h = scale(ratio, w), scale(ratio, h)
		l_pad, r_pad = centre_pad(w)
	else:
		l_pad = int(margin / 2)
		r_pad = l_pad
		ratio = (size - margin) / w
		w, h = scale(ratio, w), scale(ratio, h)
		t_pad, b_pad = centre_pad(h)

	img = cv2.resize(img, (w, h))
	img = cv2.copyMakeBorder(img, t_pad, b_pad, l_pad, r_pad, cv2.BORDER_CONSTANT, None, background)
	return cv2.resize(img, (size, size))


def find_largest_feature(inp_img, scan_tl=None, scan_br=None):
	"""
	Uses the fact the `floodFill` function returns a bounding box of the area it filled to find the biggest
	connected pixel structure in the image. Fills this structure in white, reducing the rest to black.
	"""
	img = inp_img.copy()  # Copy the image, leaving the original untouched
	height, width = img.shape[:2]

	max_area = 0
	seed_point = (None, None)

	if scan_tl is None:
		scan_tl = [0, 0]

	if scan_br is None:
		scan_br = [width, height]

	# Loop through the image
	for x in range(scan_tl[0], scan_br[0]):
		for y in range(scan_tl[1], scan_br[1]):
			# Only operate on light or white squares
			if img.item(y, x) == 255 and x < width and y < height:  # Note that .item() appears to take input as y, x
				area = cv2.floodFill(img, None, (x, y), 64)
				if area[0] > max_area:  # Gets the maximum bound area which should be the grid
					max_area = area[0]
					seed_point = (x, y)

	# Colour everything grey (compensates for features outside of our middle scanning range
	for x in range(width):
		for y in range(height):
			if img.item(y, x) == 255 and x < width and y < height:
				cv2.floodFill(img, None, (x, y), 64)

	mask = np.zeros((height + 2, width + 2), np.uint8)  # Mask that is 2 pixels bigger than the image

	# Highlight the main feature
	if all([p is not None for p in seed_point]):
		cv2.floodFill(img, mask, seed_point, 255)

	top, bottom, left, right = height, 0, width, 0

	for x in range(width):
		for y in range(height):
			if img.item(y, x) == 64:  # Hide anything that isn't the main feature
				cv2.floodFill(img, mask, (x, y), 0)

			# Find the bounding parameters
			if img.item(y, x) == 255:
				top = y if y < top else top
				bottom = y if y > bottom else bottom
				left = x if x < left else left
				right = x if x > right else right

	bbox = [[left, top], [right, bottom]]
	return img, np.array(bbox, dtype='float32'), seed_point


def extract_digit(img, rect, size):
	"""Extracts a digit (if one exists) from a Sudoku square."""

	digit = cut_from_rect(img, rect)  # Get the digit box from the whole square
	# show_image(digit)

	# Use fill feature finding to get the largest feature in middle of the box
	# Margin used to define an area in the middle we would expect to find a pixel belonging to the digit
	h, w = digit.shape[:2]
	margin = int(np.mean([h, w]) / 2.5)
	_, bbox, seed = find_largest_feature(digit, [margin, margin], [w - margin, h - margin])
	digit = cut_from_rect(digit, bbox)

	# Scale and pad the digit so that it fits a square of the digit size we're using for machine learning
	w = bbox[1][0] - bbox[0][0]
	h = bbox[1][1] - bbox[0][1]

	# Ignore any small bounding boxes
	if w > 0 and h > 0 and (w * h) > 100 and len(digit) > 0:
		return scale_and_centre(digit, size, 4)
	else:
		return np.zeros((size, size), np.uint8)

def get_digits(img, squares, size):
	"""Extracts digits from their cells and builds an array"""
	digits = []
	img = preprocess_img(img.copy(), skip_dilate=True)
	for square in squares:
		# show_image(extract_digit(img, square, size))
		digits.append(extract_digit(img, square, size))
	return digits



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
	digits = get_digits(cropped_sudoku, squares_on_sudoku, 28)
	board = extract_number(digits, loaded_model)
	print(board)
	solved = solve(board)
	print(solved)



if __name__ == '__main__':
    main()
