import csv
import cx_Oracle
import smtplib
from socket import gaierror
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import functools 

con = cx_Oracle.connect('userid/pwd@dbname')
cursor = con.cursor()
csv_file = open("\\\\ne1pastore01\\oma_users2$\\przse2\\ErrorReport.csv", "w")
writer = csv.DictWriter(csv_file, fieldnames = ["DSF_LOAD_ERR_SEQ", "INF_GROUP_ID", "POLICY_NUMBER", "CLAIM_NUMBER", "PAY_AMOUNT", "ERROR_MSG"])
writer.writeheader()
writer = csv.writer(csv_file, delimiter=',', lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC)
cursor.execute("SELECT count(*) FROM gman.dsf_clm_chrgs_load_errors where trunc(batch_date) = trunc(sysdate)")
data = cursor.fetchone()
res = functools.reduce(lambda sub, ele: sub * 10 + ele, data) 
# printing result 
print("Error Records : " + str(res)) 
if res > 0:
    cursor.execute("SELECT DSF_LOAD_ERR_SEQ, INF_GROUP_ID, POLICY_NUMBER, CLAIM_NUMBER, PAY_AMOUNT, ERROR_MSG  FROM gman.dsf_clm_chrgs_load_errors where trunc(batch_date) = trunc(sysdate)")
    for row in cursor:
        writer.writerow(row)
cursor.close()
con.close()
csv_file.close()   
if res > 0:
    subject = "DSF Claims Load Errors from GRINS to ARDIS"
    body = "Attached is a Report of DSF Claims Load Errors from GRINS to ARDIS.\n Prod Support please take action in Fixing the Errors and Reporcessing the Records to Load in the Ardis"
    sender_email = "DoNotReply@lfg.com"
    receiver_email = "pradeep.settipalli@lfg.com"
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    message['X-Priority'] = '2'
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    filename = "ErrorReport.csv"  # In same directory as script
    Path     = "\\\\ne1pastore01\\oma_users2$\\przse2\\"
    # Open PDF file in binary mode
    with open(Path + filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    # Log in to server using secure context and send email
    try:
        # Send your message with credentials specified above
        with smtplib.SMTP("gsosmtp.lfg.com", 25) as server:
          server.sendmail(sender_email, receiver_email, text)
    except (gaierror, ConnectionRefusedError):
    # tell the script to report if your message was sent or which errors need to be fixed
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))
    else:
        print('Sent')
else:
    print('No Records to Email')
os.remove("\\\\ne1pastore01\\oma_users2$\\przse2\\ErrorReport.csv")           
  