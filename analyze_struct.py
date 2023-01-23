import os

import cv2, numpy, sys

def read_image(image_path):
    img = cv2.imread(image_path)
    return img


def increase_contrast(image):
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(image_lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)
    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def slice_image(image, path_to_dir, start_coordinates, number_slices):
    current_coordinates = start_coordinates[:]
    finish_coordinates = [image.shape[0], image.shape[1]]
    delta_coordinate = [abs((finish_coordinates[0] - current_coordinates[0]) // number_slices),
                        (abs(finish_coordinates[1] - current_coordinates[1]))
                        ]

    for i in range(number_slices):
        crop_img = image[current_coordinates[0]:current_coordinates[0] + delta_coordinate[0],
                   current_coordinates[1]:current_coordinates[1] + delta_coordinate[1]]

        current_coordinates[0] += delta_coordinate[0]

        result_image = find_ferrite(crop_img)

        print("%i: %4.2f%%" % (i + 1, get_percentage_ferrite(result_image)))

        cv2.imwrite(path_to_dir + f"/{i + 1}.jpg", result_image)


def find_ferrite(image, theshold_pixel= 180, threshold_contour=5000):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, theshold_pixel, 255, cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(binary,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # cv2.imwrite(f"./res.png", binary)
    i = 0
    for contour in contours:
        # x,y,w,h = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < threshold_contour:
            convexHull = cv2.convexHull(contour)
            cv2.fillPoly(binary, [convexHull], (0, 0, 0))

    binary = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    return binary

def get_percentage_ferrite(image):
    return numpy.sum(image == 255) / image.size * 100

def openImage(path):
    return read_image(path)

def runProcessing(image, name, threshold_pixel, threshold_contour):
    try:
        image = increase_contrast(image)
    except cv2.error as e:
        print(f'image {name} isn\'t processed')

    result_image = find_ferrite(image, theshold_pixel=threshold_pixel, threshold_contour=threshold_contour)
    # cv2.imwrite(f"./res_{name}", result_image)

    # print(type(result_image))
    return result_image

def saveImage(path, image):
    cv2.imwrite(path, image)

def main():
    if len(sys.argv) != 3:
        print(sys.argv)
        print("Wrong parameters! Example: python analyze_struct.py path_to_dir number_of_slices(>=0)")
        exit(1)
    elif not os.path.exists(sys.argv[1]):
        print("Directory doesn't exist")
        exit(1)

    images = os.listdir(sys.argv[1])

    try:
        number_slices = 0 if int(sys.argv[2]) < 0 else int(sys.argv[2])
    except ValueError:
        print("Wrong number! Example: python analyze_struct.py path_to_dir number_of_slices(>=0)")
        exit(1)

    start_coordinates = [1565, 1585]

    result_perc_ferrite = {}
    for name_image in images:
        print(name_image)
        print(sys.argv[1]  + "\\" + name_image)
        image = read_image(sys.argv[1] + "\\" + name_image)

        try:
            image = increase_contrast(image)
        except cv2.error as e:
            print(f'{name_image} is not processed')
            continue

        if number_slices > 0:
            path_dir = f"./{name_image}"
            os.mkdir(path_dir)
            slice_image(image, path_dir, start_coordinates, number_slices)

        # cv2.imshow('image', image)
        # cv2.waitKey(0)
        # image = image[start_coordinates[0]:image.shape[0], start_coordinates[1]:image.shape[1]]
        result_image = find_ferrite(image)
        result_perc_ferrite[name_image] = get_percentage_ferrite(result_image)
        cv2.imwrite(f"./res_{name_image}", result_image)

    with open("./result.txt", "w") as result_txt:
        for name in result_perc_ferrite:
            print(f"%s: %4.2f%%" % (name, result_perc_ferrite[name]), file=result_txt)


if __name__ == '__main__':
    main()
