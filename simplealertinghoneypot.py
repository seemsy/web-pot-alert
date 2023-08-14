import socket
import threading
import requests

# Set your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID_HERE'

# Set the HTML to be served
HTML = "<h1>Database connection failed..</h1>"

# Set the Server HTTP header
SERVER = "Apache httpd 2.4.46"

def send_telegram_notification(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(telegram_url, params=params)

def handle_tcp_connection(client_socket, addr):
    try:
        data = request = client_socket.recv(1024)
        send_telegram_notification(f"HONEYPOT ALERT: Connection from: {addr}")
        http_response = f"HTTP/1.1 200\r\nServer: {SERVER}\r\nContent-Length: {len(HTML)}\r\n\r\n{HTML}"
        client_socket.sendall(http_response.encode())
        client_socket.close()
    except ConnectionResetError:
        send_telegram_notification(f"HONEYPOT ALERT[ConnReset]: Connection from: {addr}")

def main():
    # Set the host and port to listen on
    HOST = '0.0.0.0'
    PORT = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_tcp_connection, args=(client_socket,addr))
        client_thread.start()

if __name__ == "__main__":
    main()
