import smtplib
import globaldata as gd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_update_email(send_to=[], subject='Engine Update {}', message='', attach_files=[]):
    run_id = gd.get_run_id()
    msg = MIMEMultipart()
    msg['Subject'] = subject.format(run_id)
    msg['From'] = 'titaniiglobaldata@gmail.com'
    msg['To'] = ', '.join(send_to)
    msg.preamble = '{}'.format(gd.get_datetime())

    for filename in attach_files:
        with open(filename) as txt_file:
            txt = MIMEText(txt_file.read())
            txt.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(txt)

    body = 'Engine Update for "{}":\n'.format(run_id)
    body += (message + '\n')
    body_text = MIMEText(body, 'plain')
    msg.attach(body_text)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('titaniiglobaldata@gmail.com', 'Welcome2018')
    server.sendmail('titaniiglobaldata@gmail.com', send_to, msg.as_string())
    server.close()

if __name__=='__main__':
    file_1 = 'D:\\python_code\\attach_this.txt'
    send_update_email(send_to=['jason.skophammer@gmail.com'], message='This is a test', attach_files=[file_1])