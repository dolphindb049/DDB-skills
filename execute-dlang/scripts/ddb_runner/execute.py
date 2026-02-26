# execute.py
import sys
import os
import argparse
import socket

# Check for required packages
try:
    import dolphindb as ddb
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Error: Missing required package '{e.name}'.", file=sys.stderr)
    print("Please install dependencies: pip install dolphindb python-dotenv", file=sys.stderr)
    sys.exit(1)

def load_config():
    """Load configuration from .env files or environment variables."""
    # 1. Try loading from current directory .env
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_dir, ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    # 2. Try loading from parent directory (legacy support potentially)
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir))) 
    parent_dotenv_path = os.path.join(parent_dir, ".env")
    if os.path.exists(parent_dotenv_path):
        load_dotenv(parent_dotenv_path)

    # 3. Read from environment
    host = os.getenv("DDB_HOST")
    port = os.getenv("DDB_PORT")
    user = os.getenv("DDB_USER", "admin")
    password = os.getenv("DDB_PASSWORD") or os.getenv("DDB_PASS", "123456")
    
    if not host or not port:
        print("❌ Error: DDB_HOST and DDB_PORT must be set in .env file or environment variables.")
        sys.exit(1)
        
    return host, int(port), user, password

def connect_ddb():
    """Connect to DolphinDB and return the session object."""
    try:
        host, port, user, password = load_config()
    except SystemExit:
        return None
        
    # print(f"🔌 Connecting to {host}:{port}...")
    print(f"🔌 Connecting to {host}:{port}...")
    try:
        s = ddb.session()
        s.connect(host, port, user, password)
        # print(f"✅ Connected to {host}:{port}")
        print(f"✅ Connected to {host}:{port}")
        return s
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return None

def run_via_server(code_str):
    """Attempt to run code via the persistent server."""
    HOST = '127.0.0.1'
    PORT = 65432
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2) # Short timeout to detect if server is down quickly
            s.connect((HOST, PORT))
            s.sendall(code_str.encode('utf-8'))
            
            # Receive response
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            
            print("✅ Execution Successful (via Server)")
            print("--- Result ---")
            print(data.decode('utf-8'))
            print("--------------")
            return True
    except (ConnectionRefusedError, socket.timeout):
        return False
    except Exception as e:
        print(f"⚠️ Server connection error: {e}")
        return False

def run_code(session, code_str, print_output=True):
    """Execute a raw code string."""
    # Try server first if session is None (meaning we didn't connect locally yet)
    if session is None:
        if run_via_server(code_str):
            return "Executed via server"
            
        # Fallback to local connection if server failed
        print("⚠️ Persistent server not found. Falling back to new session.")
        session = connect_ddb()
        if not session:
            return None

    try:
        if print_output:
            print(f"Executing code snippet...")
        result = session.run(code_str)
        if print_output:
            print("✅ Execution Successful")
            print("--- Result ---")
            print(result)
            print("--------------")
        return result
    except Exception as e:
        print(f"❌ Code Execution Failed: {e}")
        return None

def run_dos_file(session, file_path):
    """Read and execute a .dos file."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            script_content = f.read()
            
        print(f"Executing file: {file_path}")
        return run_code(session, script_content)
    except Exception as e:
        print(f"❌ File Execution Failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="DolphinDB Script Executor")
    parser.add_argument("file", nargs="?", help="Path to .dos or .txt script file")
    parser.add_argument("-c", "--code", help="Direct code string to execute")
    parser.add_argument("--new-session", action="store_true", help="Force new session (bypass server)")
    
    args = parser.parse_args()
    
    if not args.file and not args.code:
        print("Please provide a file path or use -c to specify code.")
        parser.print_help()
        sys.exit(1)

    session = None
    if args.new_session:
        session = connect_ddb()
        if not session:
            sys.exit(1)
    if args.file:
        run_dos_file(session, args.file)

if __name__ == "__main__":
    main()
