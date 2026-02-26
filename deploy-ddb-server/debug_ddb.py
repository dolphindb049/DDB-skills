import paramiko
import sys

HOSTNAME = "192.168.100.45"
USERNAME = "jrzhang"
PASSWORD = "123456"
TARGET_DIR = "/hdd/hdd9/jrzhang/deploy_test"
LOG_FILE = f"{TARGET_DIR}/server/server/dolphindb.log"

def get_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
    return client

def read_log():
    client = get_client()
    try:
        print("Checking netstat...")
        stdin, stdout, stderr = client.exec_command(f"netstat -tulnp | grep {8900}")
        print(stdout.read().decode())
        
        print(f"Reading {LOG_FILE}...")
        stdin, stdout, stderr = client.exec_command(f"cat {LOG_FILE}")

        out = stdout.read().decode()
        err = stderr.read().decode()
        if out:
            print("--- LOG START ---")
            print(out)
            print("--- LOG END ---")
        else:
            print("Log is empty or file not found.")
            print(f"STDERR: {err}")
    finally:
        client.close()

if __name__ == "__main__":
    read_log()
