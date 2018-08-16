import logging
import datetime
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import smtplib, socket
from subprocess import Popen, PIPE
import subprocess

import requests

from utils.utils import read_config, logger

# Config file
config = read_config('config.yaml')

# set variable from config file
SMTP_SERVER = config['SMTP_SERVER']
PORT = config['PORT']
FROM = config['FROM']
TO = config['TO']
PASSWORD = config['PASSWORD']
HEALTHCHECK_URL = config['HEALTHCHECK_URL']
LOG_FILENAME_SERVER = config['LOG_FILENAME_SERVER']
LOG_FILENAME_EMAIL = config['LOG_FILENAME_EMAIL']

# initialise logger
log = logger(LOG_FILENAME_EMAIL)


def send_email(error_msd, filename):
    """
    send email with error message from log file

    Args:
        error_msg:``list``
            Error message, each sentence as list
        filename:``str``
            filename of log file
            
    Return:
        True if success else log error message
        
    Raise:
        ``socket.error`` if error while sending message.
    """
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    password = PASSWORD
    msg['Subject'] = "Server is down {}".format(sys.argv[1])
    body = "Error found in log: \n" + '\n'.join(error_msd) + "\n Check logfile: " + filename
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(SMTP_SERVER, PORT)
    server.starttls()
    server.login(msg['From'], password)
    try:
        server.sendmail(msg['From'],msg['To'], msg.as_string())
        server.quit()
        return True
    except socket.error as e:
        log.debug('email failed: Exception {}'.format(e))
        raise

def tail(filename, n):
    """
    Get last n lines from file as string

    Args:
        filename:``str``
            filename of log file
        n:``int``
            number of lines
            
    Return:
        lines form file as string
    """
    p=subprocess.Popen(['tail','-n',str(n),filename], stdout=subprocess.PIPE)
    soutput, _=p.communicate()
    lines = soutput.decode('utf8').split('\r')
    return lines

def healthcheck(url):
    """
    check the health of server

    Args:
        url:``str``
            url of healthcheck endpoint
            
    Return:
        if live True else False
    """
    try:
        r = requests.get('http://localhost:5000/healthcheck')
        output = r.json()
        _ = output['Success']
        return True
    except:
        return False
        
def checkhealth_send_email(server_logfile=LOG_FILENAME_SERVER,
							email_logfile=LOG_FILENAME_EMAIL,
							healthcheck_url=HEALTHCHECK_URL):
    """
    Check the health and send the log file as error message if server is down

    Args:
        server_logfile:``str``
            path of file where log of server is stored
        email_logfile:``str``
            path of file where log of this email is stored
        healthcheck_url:``str``
            url for health checkhealth
            
    Return:
        send email if server is down and email is not already send

    """
    # get the lines from files
    email_loglines = tail(email_logfile, 100)
    server_loglines  = tail(server_logfile, 100)

    # check if email log file has 'down' words we dont want to send email every 10mins
    # if server is down, we just record it on email log files
    # if server is down first time we send email
    if 'down' in email_loglines[0]:
        if healthcheck(healthcheck_url):
            log.debug("{}  server is ok".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            log.debug("{}  server is down".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        if not healthcheck(healthcheck_url):
            send_email(server_loglines, server_logfile)
            log.debug("{}  server is down".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            log.debug("{}  server is ok".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


if __name__ == "__main__":
    checkhealth_send_email(server_logfile=LOG_FILENAME_SERVER,
							email_logfile=LOG_FILENAME_EMAIL,
							healthcheck_url=HEALTHCHECK_URL)
