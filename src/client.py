#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
import sys

sysEncode = sys.getfilesystemencoding()

ip = '127.0.0.1'
ip_port = (ip, 6666)
filename = './img/image.jpg'
file0 = 'image.jpg'

address = ('127.0.0.1', 6666)


def send(photo):
    print('sending {}'.format(photo))
    data = file_deal(photo)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.send('{}|{}'.format(len(data), file0).encode())  # 默认编码 utf-8,发送文件长度和文件名
    reply = sock.recv(1024)
    if 'ok' == reply.decode():  # 确认一下服务器get到文件长度和文件名数据
        go = 0
        total = len(data)
        while go < total:  # 发送文件
            data_to_send = data[go:go + 1024]
            sock.send(data_to_send)
            go += len(data_to_send)
        reply = sock.recv(1024)
        if 'copy' == reply.decode():
            print('{} send successfully'.format(photo))
    sock.close()


def file_deal(file_path):  # 读取文件的方法
    mes = b''
    try:
        f = open(file_path, 'rb')
        mes = f.read()
    except:
        print('error{}'.format(file_path))
    else:
        f.close()
        return mes


if __name__ == '__main__':
    send(filename)
