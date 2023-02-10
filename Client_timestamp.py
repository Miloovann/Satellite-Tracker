import socket
import sys, os


def HCI_tracking(T_sta,T_end,T_dur):

    try:    os.remove("projected.txt")
    except:	pass

    Time = 1672848330


    for Time in range(T_sta,T_end,T_dur):
    #for Time in range(Time,Time+120,2):

        hTime = hex(Time)[2:]
        header = b'\xae\xa3\xc0\x00\x00\x02\x09'
        packet = header + bytes.fromhex(hTime)

        processedhTime = bytes.fromhex(hTime)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        IP = "172.27.119.252"#may need to change
        PORT = 1028
        server_address = (IP, PORT)
        sock.connect(server_address)
        print('connecting to %s port %s' % server_address)

        try:
            sock.sendall(packet)

        finally:
            print('closing socket')
            sock.close()

HCI_tracking(1672849000,1672849160,2)
