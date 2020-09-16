import sys
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import threading
# import time

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
image_path = '../img'
file_path = '../file'
count = 0
black_count = 0


def detect_color(array):
    if array[0] < 200 and array[1] < 200 and array[2] < 200:
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
    # print('-----------image_process-----------')
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
    f = open(file_path+"/count.txt", 'w')
    f.write(str(black_count0)+' '+str(count))
    f.close()
    print(black_count0, count0)


def led_red():
    os.system(
        'rostopic pub -1 /mobile_base/rgb_leds std_msgs/UInt8MultiArray "{data: [100,0,0, 100,0,0, 100,0,0, 100,0,0]}"')


def led_blue():
    os.system(
        'rostopic pub -1 /mobile_base/rgb_leds std_msgs/UInt8MultiArray "{data: [0,0,100, 0,0,100, 0,0,100, 0,0,100]}"')


if __name__ == '__main__':
    while True:
        str_count = str(count).zfill(6)
        try:
            flag = image_process(image_path + '/image' + str_count + '.jpg')
        except IOError:
            continue
        if flag == 1:
            black_count = black_count + 1
        count = count + 1
        save(black_count, count)

        if flag == 1:
            threading.Thread(target=led_red).start()
        else:
            threading.Thread(target=led_blue).start()

        # plot(image_path+'/image'+str_count+'.jpg')
