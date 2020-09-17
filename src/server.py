#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
import sys
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
save_path = '../img/img_raspberry'
file_path = '../file'
LOCAL_IP = '127.0.0.1'
PORT = 6666
count = 0


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


def save(count0, obj):
    print('-----------save_obj-----------')
    f = open(file_path + "/obj.txt", 'w')
    f.write(str(count0) + ' ' + obj)
    f.close()


def server(count0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((LOCAL_IP, PORT))
    sock.listen(3)
    while True:
        sc, sc_name = sock.accept()  # 当有请求到指定端口是 accpte()会返回一个新的socket和对方主机的（ip,port）
        print('收到{}请求'.format(sc_name))
        info = sc.recv(1024)  # 首先接收一段数据，这段数据包含文件的长度和文件的名字，使用|分隔，具体规则可以在客户端自己指定
        length, file_name = info.decode().split('|')
        if length and file_name:
            str_count = str(count0).zfill(6)
            new_file = open(save_path + '/image' + str_count + '.jpg', 'wb')  # 这里可以使用从客户端解析出来的文件名
            count0 = count0 + 1
            print('length {},filename {}'.format(length, file_name))
            sc.send(b'ok')  # 表示收到文件长度和文件名
            file = b''
            total = int(length)
            get = 0
            while get < total:  # 接收文件
                data = sc.recv(1024)
                file += data
                get = get + len(data)
            print('应该接收{},实际接收{}'.format(length, len(file)))
            if file:
                print('actually length:{}'.format(len(file)))
                new_file.write(file[:])
                new_file.close()
                sc.send(b'copy')  # 告诉完整的收到文件
        sc.close()
        obj = detect_object(save_path, count0)
        print('The e-puck is the', obj)
        save(count0, obj)


if __name__ == '__main__':
    server(count)
