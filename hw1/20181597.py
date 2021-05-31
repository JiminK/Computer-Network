from socket import *
from urllib.parse import urlparse

print('Student ID : 20181597')
print('Name : Jimin Kim')

def parseHeader(data):
    try:
        index = data.index(b'\r\n\r\n')
    except:
        return data, bytes()
    else:
        index += len(b'\r\n\r\n')
        return data[:index], data[index:]

while True:
    print('> ', end='')
    cmd = input()

    if (cmd == 'quit'):
        break

    elif (cmd.startswith('get')):
        url = cmd.replace('get ', '', 1)
        o = urlparse(url)
        host = url.split("//")[-1].split("/")[0].split(':')[0]
        #host = o.netloc
        img = o.path
        # img = url.split('/')[-1]
        # print("o : " + str(o))
        # print("host : " + host)
        # print("img : " + img)

        # ERROR : if the protocol of url is not http
        if (o.scheme != 'http'):
            print('Only support http, not ' + o.scheme)
        else:
            if (o.port is None):
                if o.scheme == 'http':
                    port = 80
                # set to https port number
                else:
                    port = 443
            else:
                port = o.port
            # print("port : " + str(port))

            # create socket
            serverSocket = socket(AF_INET, SOCK_STREAM)
            addr = (host, int(port))
            BUFSIZE = 1024

            # ERROR : When you cannot connect to the server
            try:
                serverSocket.connect(addr)
            except Exception as e:
                print(host + ": unknown host")
                print("cannot connect to server " + host + " " + str(port))
                continue

            try:
                # print("try")
                # serverSocket.connect(addr)

                msg = "GET {} HTTP/1.0\r\nHost: {}\r\nUser-agent: HW1/1.0\r\nConnection: Close\r\n\r\n".format(img, host)
                # print(msg)
                byte_message = msg.encode() # string to binary
                serverSocket.send(byte_message)
                # print("send msg")

                serverSocket.send(msg.encode())
                receiveData = serverSocket.recv(BUFSIZE)
                header, data = parseHeader(receiveData)
                header = header.decode()
                for line in header.split('\r\n'):
                    if 'HTTP' in line:
                        statusCode = int(line.split()[1])
                # print("statusCode : " + str(statusCode))


                if (statusCode == 200):
                    print(msg)
                    for line in header.split('\r\n'):
                        if 'Content-Length' in line:
                            contentLength = int(line[len('Content-Length') + 1:])
                    print("Total Size {} bytes".format(contentLength))
                    # Download data
                    dataTransferred = 0
                    if not data:
                        print("File [{}] doesn't exist or network error".format(img))
                        exit(0)
                    f = open(url.split('/')[-1], 'wb')
                    # print("109")
                    try:
                        cnt = 1
                        while data:
                            f.write(data)
                            dataTransferred += len(data)
                            data = serverSocket.recv(BUFSIZE)
                            # Display a message every time it exceeds 10%
                            if int(dataTransferred / contentLength * 100) >= cnt * 10:
                                print('Current Downloading {}/{} (bytes) {} %'.format(dataTransferred, contentLength, int(dataTransferred / contentLength * 100)))
                                cnt += 1
                    except Exception as e:
                        # print("error 162")
                        print(e)

                    f.close()
                    print("Download Complete: {}, {}/{}".format(url.split('/')[-1], dataTransferred, contentLength))
                    serverSocket.close()

                # ERROR : When the status code of HTTP Response message is not 200
                else:
                    print(str(statusCode) + ' Not Found')
                    continue

            except Exception as e:
                print(e)
                continue

    else:
        print(cmd + ' is WRONG command')