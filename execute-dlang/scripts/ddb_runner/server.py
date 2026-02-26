import dolphindb as ddb
import socket
import sys
import os
from dotenv import load_dotenv

# Load config
current_dir = os.path.dirname(os.path.abspath(__file__))
# Check for .env in parent directories
dotenv_path = os.path.join(os.path.dirname(current_dir), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

HOST = '127.0.0.1'
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def load_ddb_config():
    ddb_host = os.getenv("DDB_HOST", "192.168.100.43")
    ddb_port = int(os.getenv("DDB_PORT", 7739))
    ddb_user = os.getenv("DDB_USER", "admin")
    ddb_pass = os.getenv("DDB_PASSWORD") or os.getenv("DDB_PASS", "123456")
    return ddb_host, ddb_port, ddb_user, ddb_pass

def start_server():
    ddb_host, ddb_port, ddb_user, ddb_pass = load_ddb_config()
    print(f"Connecting to DolphinDB {ddb_host}:{ddb_port}...")
    
    try:
        session = ddb.session()
        session.connect(ddb_host, ddb_port, ddb_user, ddb_pass)
        print("Connected to DolphinDB!")
    except Exception as e:
        print(f"Failed to connect to DolphinDB: {e}")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server listening on {HOST}:{PORT}")
            
            while True:
                conn, addr = s.accept()
                with conn:
                    # extensive buffer for large scripts
                    data = b""
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                        if len(chunk) < 4096:
                            break
                    
                    if not data:
                        continue
                        
                    script = data.decode('utf-8')
                    print(f"Executing script length: {len(script)}")
                    
                    try:
                        result = session.run(script)
                        output = str(result)
                        conn.sendall(output.encode('utf-8'))
                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        conn.sendall(error_msg.encode('utf-8'))
        except OSError as e:
            if e.errno == 10048: # Address already in use
                print(f"Port {PORT} is already in use. Server might be running.")
            else:
                print(f"Socket error: {e}")

if __name__ == "__main__":
    start_server()
