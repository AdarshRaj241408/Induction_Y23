import socket

SERVER = socket.gethostbyname(socket.gethostname())  # Change this to the IP address of your server
PORT = 5050
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# def send_command(command):
#     client.sendall(command.encode())
#     response = client.recv(1024).decode()
#     # Close the connection after receiving the response
#     return response

def store(filename):
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
    except FileNotFoundError:
        print("File not found.")
        return
    print(f"file_data at client(1): {file_data}")
    command = f"STOR {filename}"
    print(command)
    client.sendall(command.encode())
    print('commend sent')
    response = client.recv(1024).decode()
    print('response came')
    print(f"file_data at client: {file_data}")
    if response == "Recieved the file":
        print(file_data)
        client.sendall(file_data)
        print(client.recv(1024).decode())
    return

def retrieve(filename):
    command = f"RETR {filename}"
    client.sendall(command.encode())
    response = client.recv(1024).decode()
    
    if response.startswith("ERROR"):
        print(response)
    else:
        with open(filename, 'wb') as file:
            file.write(response.encode())
        print("File retrieved successfully")

def list_files():
    command = "LIST hi"
    print("listing....")
    print(command)
    client.sendall(command.encode())
    print('hi')
    response = client.recv(1024).decode()
    print(response)

def quit():
    command = "QUIT yo"
    client.sendall(command.encode())
    response = client.recv(1024).decode()
    print(response)

def main():
    while True:
        print("1. Store file (STOR)")
        print("2. Retrieve file (RETR)")
        print("3. List files (LIST)")
        print("4. Quit (QUIT)")

        choice = input("Enter your choice: ")

        if choice == "1":
            filename = input("Enter filename to store: ")
            store(filename)
        elif choice == "2":
            filename = input("Enter filename to retrieve: ")
            retrieve(filename)
        elif choice == "3":
            list_files()
        elif choice == "4":
            quit()
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()

