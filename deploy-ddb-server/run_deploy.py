import paramiko
import sys
import os

HOSTNAME = "192.168.100.45"
USERNAME = "jrzhang"
PASSWORD = "123456"

def deploy():
    # Read the bash script
    script_path = os.path.join(os.path.dirname(__file__), "deploy.sh")
    with open(script_path, "r", encoding="utf-8") as f:
        bash_script = f.read()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Connecting to {HOSTNAME}...")
        client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
        
        print("Sending deployment script...")
        stdin, stdout, stderr = client.exec_command("bash -s")
        stdin.write(bash_script)
        stdin.flush()
        stdin.channel.shutdown_write()

        while True:
            line = stdout.readline()
            if not line:
                break
            print(line, end="")
            
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("\nDeployment Successful")
        else:
            print(f"\nDeployment Failed (Code: {exit_status})")
            print("STDERR:", stderr.read().decode())

    finally:
        client.close()

if __name__ == "__main__":
    deploy()
