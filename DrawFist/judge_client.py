import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.101', 55555))
counter = 1

while True:
    with open('/home/esdc/桌面/QT_gui_test_bin/Flags/FastStart.txt', 'r') as fsr:
        fst = fsr.readline().strip()
    if fst == '1':
        s.send(b'nocheat')
        print('send success')
        with open('/home/esdc/桌面/QT_gui_test_bin/Flags/FastStart.txt', 'w+') as fsw:
            fsw.write('')
        break
    elif fst == '0':
        s.send(b'quick')
        print('send success')
        with open('/home/esdc/桌面/QT_gui_test_bin/Flags/FastStart.txt', 'w+') as fsw:
            fsw.write('')
        break

while True:
    data = s.recv(1024)
    if data:
        print('receive data ')
        print(counter)
        counter = counter + 1
        # print(str(data))
        with open('/home/esdc/桌面/QT_gui_test_bin/Flags/RobotGesture.txt', 'w') as rg:
            rg.write(str(data)[2])
        with open('/home/esdc/桌面/QT_gui_test_bin/Flags/RobotVoice.txt', 'w') as rv:
            rv.write(str(data)[3])
    while True:
        with open('/home/esdc/桌面/QT_gui_test_bin/Flags/HumanGesture_send.txt', 'rb') as hg:
            hgdata = hg.readline().strip()
        with open('/home/esdc/桌面/QT_gui_test_bin/Flags/HumanVoice_send.txt', 'rb') as hv:
            hvdata = hv.readline().strip()

        if hvdata and hgdata:
            s.send(hvdata + hgdata)
            print('send success')
            with open('/home/esdc/桌面/QT_gui_test_bin/Flags/HumanGesture_send.txt', 'w+') as hgw:
                hgw.write('')
            with open('/home/esdc/桌面/QT_gui_test_bin/Flags/HumanVoice_send.txt', 'w+') as hvw:
                hvw.write('')
            break
s.close()
