import socket
import sys, os

def HCI_aoslos(Sat_no):

    try:    os.remove("AOSLOS.txt")
    except:	pass


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    IP = "172.27.98.68"#may need to change
    PORT = 1028
    server_address = (IP, PORT)
    sock.connect(server_address)
    print('connecting to %s port %s' % server_address)

    try:
        if Sat_no == 1:
            sock.sendall(b'\xae\xa3\xc0\x00\x00\x02\x08\x01')
        if Sat_no == 2:
            sock.sendall(b'\xae\xa3\xc0\x00\x00\x02\x08\x02')
        if Sat_no == 3:
            sock.sendall(b'\xae\xa3\xc0\x00\x00\x02\x08\x03')


    finally:
        print('closing socket')
        sock.close()

HCI_aoslos(3)#use this as a default for now
