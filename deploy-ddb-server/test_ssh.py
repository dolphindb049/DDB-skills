import paramiko
import sys

hostname = "192.168.100.45"
username = "jrzhang"
passwords = ["123456", "DolphinDB123"]

def try_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for pwd in passwords:
        try:
            print(f"Trying password: {pwd}")
            client.connect(hostname, username=username, password=pwd, timeout=5)
            print("Successfully connected!")
            stdin, stdout, stderr = client.exec_command("ls -la")
            print(stdout.read().decode())
            client.close()
            return True
        except Exception as e:
            print(f"Failed with {pwd}: {e}")
    
    return False

if __name__ == "__main__":
    if not try_connect():
        sys.exit(1)
