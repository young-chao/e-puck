#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
image_path = '../img/img_raspberry'
count = 3


def detect_color(array):
    if array[0] > 100 and array[1] < array[0] - 40 and array[1] < 90 and array[2] < 90 and array[2] < array[0] - 20 and \
            array[1] - 10 < array[2] < array[1] + 10:
        return 'red'
    elif array[0] < 80 and array[1] > 100 and array[2] < array[1] - 20:
        return 'green'
    elif array[0] < 80 and array[2] > 100 and array[1] < array[2] - 20:
        return 'blue'
    else:
        return 'others'


def plot(path, count0):
    str_count = str(count0).zfill(6)
    name = path + '/image' + str_count + '.jpg'
    img = Image.open(name)
    img0 = np.array(img)
    plt.figure("beauty")
    plt.imshow(img0)
    plt.axis('off')
    plt.show()


def detect_object(path, count0):
    str_count = str(count0).zfill(6)
    name = path + '/image' + str_count + '.jpg'
    r_num = 0
    g_num = 0
    b_num = 0
    img = Image.open(name)
    img_array = img.load()
    print('1:', img.size[0], ' 2:', img.size[1])

    # 输出像素值
    for i in range(img.size[0] - 20):
        for j in range(img.size[1] - 20):
            if detect_color(img_array[i, j]) == 'red':
                print('red one:', i, j)
                for x in range(20):
                    for y in range(20):
                        if detect_color(img_array[i + x, j + x]) == 'red':
                            r_num = r_num + 1
                        else:
                            r_num = r_num - 1
                if r_num > 300:
                    print('red:', i, j, img_array[i, j])
                    return 'red one'
                else:
                    r_num = 0
            elif detect_color(img_array[i, j]) == 'green':
                print('green one:', i, j)
                for x in range(20):
                    for y in range(20):
                        if detect_color(img_array[i + x, j + x]) == 'green':
                            g_num = g_num + 1
                if g_num > 300:
                    print('green:', i, j, img_array[i, j])
                    return 'green one'
                else:
                    g_num = 0
            elif detect_color(img_array[i, j]) == 'blue':
                print('blue one:', i, j)
                for x in range(20):
                    for y in range(20):
                        if detect_color(img_array[i + x, j + x]) == 'blue':
                            b_num = b_num + 1
                if b_num > 300:
                    print('blue:', i, j, img_array[i, j])
                    return 'blue one'
                else:
                    b_num = 0


if __name__ == '__main__':
    obj = detect_object(image_path, count)
    print('The e-puck is the', obj)
    plot(image_path, count)
