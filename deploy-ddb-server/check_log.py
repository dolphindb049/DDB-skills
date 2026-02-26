import paramiko

HOSTNAME = "192.168.100.45"
USERNAME = "jrzhang"
PASSWORD = "123456"
LOG_FILE = "/hdd/hdd9/jrzhang/deploy_test/server/server/dolphindb.log"

def check_log():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOSTNAME, username=USERNAME, password=PASSWORD)
    stdin, stdout, stderr = client.exec_command(f"tail -n 50 {LOG_FILE}")
    print(stdout.read().decode())
    client.close()

if __name__ == "__main__":
    check_log()
