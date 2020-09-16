import sys
import os
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import socket
import logging

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
image_path = '../img'
count = 0
black_count = 0

COMMAND_PACKET_SIZE = 21
HEADER_PACKET_SIZE = 1
MAX_NUM_CONN_TRIALS = 5
TCP_PORT = 1000  # This is fixed.
NUM_ROBOTS = 1  # Set this value to the number of robots to which connect
addr = "192.168.43.32"
robot_id = "4695"
sock = [None] * NUM_ROBOTS
header = bytearray([0] * 1)
proximity = [[0 for x in range(16)] for y in
             range(NUM_ROBOTS)]  # Matrix containing the proximity values for all robots.
command = [bytearray([0] * COMMAND_PACKET_SIZE) for y in
           range(NUM_ROBOTS)]  # Matrix containing the commands sent by all the robots.
refresh = [0 for x in range(NUM_ROBOTS)]


def send(s, msg, msg_len):
    totalsent = 0
    while totalsent < msg_len:
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("Send error")
        totalsent = totalsent + sent


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
    led = 0
    trials = 0
    client_index = 0
    client_addr = addr

    # Init the array containing the commands to be sent to the robot.
    command[client_index][0] = 0x80  # Packet id for settings actuators
    command[client_index][1] = 0x02  # Request: only sensors enabled
    command[client_index][2] = 0  # Settings: set motors speed
    command[client_index][3] = 0x80  # left motor LSB
    command[client_index][4] = 0  # left motor MSB
    command[client_index][5] = 0x80  # right motor LSB
    command[client_index][6] = 0  # right motor MSB
    command[client_index][7] = 0  # lEDs
    command[client_index][8] = 0x44  # LED2 red
    command[client_index][9] = 0  # LED2 green
    command[client_index][10] = 0  # LED2 blue
    command[client_index][11] = 0x44  # LED4 red
    command[client_index][12] = 0  # LED4 green
    command[client_index][13] = 0  # LED4 blue
    command[client_index][14] = 0x44  # LED6 red
    command[client_index][15] = 0  # LED6 green
    command[client_index][16] = 0  # LED6 blue
    command[client_index][17] = 0x44  # LED8 red
    command[client_index][18] = 0  # LED8 green
    command[client_index][19] = 0  # LED8 blue
    command[client_index][20] = 0  # speaker

    # Init the connection. In case of errors, try again for a while and eventually give up in case the connection
    # cannot be accomplished.
    print("Try to connect to " + client_addr + ":" + str(TCP_PORT) + " (TCP)")
    while trials < MAX_NUM_CONN_TRIALS:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_sock.settimeout(10)  # non-blocking socket
        try:
            client_sock.connect((client_addr, TCP_PORT))
        except socket.timeout as err:
            client_sock.close()
            logging.error("Error from " + client_addr + ":")
            logging.error(err)
            trials += 1
            continue
        except socket.error as err:
            client_sock.close()
            logging.error("Error from " + client_addr + ":")
            logging.error(err)
            trials += 1
            continue
        except Exception as err:
            client_sock.close()
            logging.error("Error from " + client_addr + ":")
            logging.error(err)
            trials += 1
            continue
        break

    if trials == MAX_NUM_CONN_TRIALS:
        print("Can't connect to " + client_addr)
        print('trials\n')

    print("Connected to " + client_addr)
    print("\r\n")

    while True:
        str_count = str(count).zfill(6)
        flag = image_process(image_path + '/image' + str_count + '.jpg')
        if flag == 1:
            black_count = black_count + 1
        count = count + 1
        save(black_count, count)

        if flag == 1:
            command[client_index][8] = 0x44  # LED2 red
            command[client_index][9] = 0  # LED2 green
            command[client_index][10] = 0  # LED2 blue
            command[client_index][11] = 0x44  # LED4 red
            command[client_index][12] = 0  # LED4 green
            command[client_index][13] = 0  # LED4 blue
            command[client_index][14] = 0x44  # LED6 red
            command[client_index][15] = 0  # LED6 green
            command[client_index][16] = 0  # LED6 blue
            command[client_index][17] = 0x44  # LED8 red
            command[client_index][18] = 0  # LED8 green
            command[client_index][19] = 0  # LED8 blue
        else:
            command[client_index][8] = 0  # LED2 red
            command[client_index][9] = 0  # LED2 green
            command[client_index][10] = 0x44  # LED2 blue
            command[client_index][11] = 0  # LED4 red
            command[client_index][12] = 0  # LED4 green
            command[client_index][13] = 0x44  # LED4 blue
            command[client_index][14] = 0  # LED6 red
            command[client_index][15] = 0  # LED6 green
            command[client_index][16] = 0x44  # LED6 blue
            command[client_index][17] = 0  # LED8 red
            command[client_index][18] = 0  # LED8 green
            command[client_index][19] = 0x44  # LED8 blue

        # Send a command to the robot.
        try:
            send(client_sock, command[client_index], COMMAND_PACKET_SIZE)
        except socket.timeout as err:
            logging.error("Error from " + client_addr + ":")
            logging.error(err)
        except socket.error as err:
            logging.error("Error from " + client_addr + ":")
            logging.error(err)
        except Exception as err:
            logging.error("Error from " + client_addr + ":")
            logging.error(err)
        time.sleep(1)
        # plot(image_path+'/image'+str_count+'.jpg')
