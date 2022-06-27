import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')


def restart_server_and_container():
    # Restart Linode Server
    print("Rebooting the server...")
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 37036999)
    nginx_server.reboot()

    # Restart the application
    while True:
        nginx_server = client.load(linode_api4.Instance, 37036999)
        if nginx_server.status == 'running':
            time.sleep(5)
            restart_container()
            break


def send_notification(email_msg):
    print("Sending an email...")
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"""MIME-Version: 1.0
Content-type: text/html 
Subject: SITE DOWN

<b>{email_msg}</b>
"""
        recipient = "amadinathaniel@gmail.com"
        smtp.sendmail(EMAIL_ADDRESS, recipient, message)


def restart_container():
    print("Restarting the application")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname='176.58.108.55', username='root',
                key_filename=r"\\wsl.localhost\Ubuntu\home\nathaniel\.ssh\id_rsa")
    stdin, stdout, stderr = ssh.exec_command('docker start 7637a2f97dcf')
    print(stdout.readlines())
    ssh.close()
    print("Application successfully restarted")


def monitor_application():
    try:
        response = requests.get('http://176-58-108-55.ip.linodeusercontent.com:8080/')
        if response.status_code == 200:
            print("Application is running successfully")
        else:
            print("Application is down. Fix it!")
            msg = f"Application returned {response.status_code}. Fix the issue!"
            send_notification(msg)
            restart_container()

    except Exception as ex:
        print(f"Connection error occurred: {ex}")
        msg = "Application is not accessible at all."
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()
