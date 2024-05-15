import socket
import random
import os

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)


users = {}
files = []

def user_exists(username):
    return username in users


def client_stor(filename, client):
    try:
        i = random.randint(1, 100)
        if filename in files:
            print('File already present!')
        else:
            while True:
                new_filename = f"{filename}_{i}"  
                if new_filename not in files:
                    break
                i += 1
            with open(new_filename, 'wb') as file: 
                while True:
                    client.send("Recieved the file".encode())
                    data = client.recv(1024)
                    print(f"yoyo at server: {data}")
                    if not data:
                        break
                    file.write(data)
                    files.append(new_filename)
                    #print (f"recieved {filename}")
        return "Recieved the file"
    except:
        return "Error recieving the file"

def client_retr(filename):
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
        return (file_data, "File retrieved")
    except FileNotFoundError:
        return ("File not found.",)
    except:
        return ("6969 ERROR")

def listing(client):
    try:
        files_list = os.listdir('.')
        files_str = '\n'.join(files_list)
        client.sendall(files_str.encode())
        return "List sent"
    except:
        return "Error sending the list"
    

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)

    print("FTP Server listening on....")

    while True:
        client,address = server.accept()
        print(f'Connected at{address}')

        while True:
            data = client.recv(1024).decode()
            #data = "STOR file.txt"
            if not data:
                break

            command = data.split(' ')[0]
            args = data.split(' ')[1]
            print(command)

            #USER commands 
            
            if command == 'LIST':
                response = listing(client)
            elif command == 'RETR':
                filename = args
                response = client_retr(filename, client)
            elif command == 'STOR':
                # print('YO')
                filename = args
                response = client_stor(filename, client)
            elif command == 'QUIT':
                print('Exiting....')
                client.close()
                return 'Exited from the server'
            #ADMIN commands
            else:
                response = "Error, command unrecognized"
            
            client.sendall(response.encode())
        #server.close()

if __name__ == "__main__":
    main()