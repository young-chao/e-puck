import sys
import os
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
image_path = '../img/img_e-puck'
count = 0
black_count = 0


def detect_color(array):
    if array[0] < 100 and array[1] < 100 and array[2] < 100:
        return 1
    else:
        return 0


def plot(name):
    img = Image.open(name)
    img0 = np.array(img)
    plt.figure("beauty")
    plt.imshow(img0)
    plt.axis('off')
    plt.show()


def image_process(img_path):
    print('-----------image_process-----------')
    black_num = 0
    img = Image.open(img_path)
    img_array = img.load()
    print('1:', img.size[0], '2:', img.size[1])
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if detect_color(img_array[i, j]) == 1:
                black_num = black_num + 1
    print(img_path)
    if black_num > img.size[0] * img.size[1] / 2:
        return 1
    else:
        return 0


def save(black_count0, count0):
    print('-----------save_count-----------')
    print(black_count0, count0)


if __name__ == '__main__':
    plot(image_path + '/image000033.jpg')
    for i in range(100):
        count = count + 1
        str_count = str(count).zfill(6)
        plot(image_path+'/image'+str_count+'.jpg')

    while True:
        str_count = str(count).zfill(6)
        flag = image_process(image_path + '/image' + str_count + '.jpg')
        if flag == 1:
            black_count = black_count + 1
        count = count + 1
        save(black_count, count)

        time.sleep(1)
        # plot(image_path+'/image'+str_count+'.jpg')
