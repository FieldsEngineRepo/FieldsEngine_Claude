__author__ = 'tim'

from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
from apiclient.discovery import build
#depends on pycrypto module and PyOpenSSL
# CreateMethodWithAttachment is untested

"""Send an email message from the user's account.
"""
import unittest
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from HTMLParser import HTMLParser

from apiclient import errors



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class Google_apps_mail(object):
    """
    This class is for service accounts defined in the Google developer console. It assumes you have
    admin rights at Google Apps to give permission to this Service account
    """
    def __init__(self,client_email,use_as_email,privatekey_path):
        """

        :param client_email: The registered client address from the service account, Google Developers Consolde
        :param use_as_email: The email of the account to use
        :param privatekey_path:
        :return:
        """
        self.client_email = client_email
        with open(privatekey_path,'rb') as f:  #'rb' is needed on Windows or else 'not enough data'
            self.private_key = f.read()
        # The oauth2client.client.SignedJwtAssertionCredentials class is only used with OAuth 2.0 Service Accounts.
        # No end-user is involved for these server-to-server API calls,
        # so you can create this object directly without using a Flow object.
        self.credentials = SignedJwtAssertionCredentials(self.client_email, self.private_key,
        'https://www.googleapis.com/auth/gmail.modify',  #scope
        sub=use_as_email)

        http = httplib2.Http()
        http = self.credentials.authorize(http)
        self.service = build('gmail', 'v1', http=http)

    def SendMessage(self, user_id, message):
      """Send an email message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

      Returns:
        Sent Message.
      """
      try:
        message = (self.service.users().messages().send(userId=user_id, body=message).execute())
        print 'Message Id: %s' % message['id']
        return message
      except errors.HttpError, error:
        print 'An error occurred: %s' % error


    def CreateMessage(self,sender, to, subject, message_text=None,message_html=None):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message. No markup allowed. If empty will strip tags from message_html
        message_html: html tags allowed. If message_html is provided, both text and html are sent.

        Returns:
        An object containing a base64 encoded email object.
        """
        if not message_text and not message_html:
            raise ValueError("Both plain text and HTML message arguments are empty!")

        if not message_html: #plain text only
            message = MIMEText(message_text)
        else:
            message = MIMEMultipart('alternative')
            if not message_text:
                message_text = strip_tags(message_html)
            part1_plain = MIMEText(message_text,'plain')
            part2_html = MIMEText(message_html,'html')
            message.attach(part1_plain)
            message.attach(part2_html)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        return {'raw': base64.urlsafe_b64encode(message.as_string())}


    def CreateMessageWithAttachment(self,sender, to, subject, message_text=None, message_html=None,file_dir=None,
                                    filename=None):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        message_html: HTML body of email. Optional.
        file_dir: The directory containing the file to be attached.
        filename: The name of the file to be attached.

        Returns:
        An object containing a base64 encoded email object.
        TODO this should accept a list of attachments, not just one
        """
        if not message_text and not message_html:
            raise ValueError("Plain text and HTML message arguments are both empty")
        if not filename:
            raise ValueError("Please provide a filename for the attachment")
        if not file_dir:
            raise ValueError("Please provide a file system directory for the attachment")
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        if not message_text and message_html:
            message_text = strip_tags(message_html)
        else:
            raise ValueError("Plain text and HTML message arguments are both empty")

        msg_plain = MIMEText(message_text,'plain')
        msg_html = MIMEText(message_html,'html')

        message.attach(msg_plain)
        message.attach(msg_html)

        path = os.path.join(file_dir, filename)
        content_type, encoding = mimetypes.guess_type(path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(path, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def CreateDraft(self,sender,message):
        """

        """
        try:
            message_envelope = {'message': message}
            draft = (self.service.users().drafts().create(userId=sender, body=message_envelope).execute())
            print 'Draft Id: %s' % draft['id']
            return draft
        except errors.HttpError, error:
            print 'An error occurred: %s' % error


class TestGoogle_meta_class(unittest.TestCase):
    def setUp(self):
        self.client_email = '...@developer.gserviceaccount.com'
        self.key_path = "e:/web2py/web2py_iis/web2py/applications/key.p12"
        self.test_user = 'tim@abc.net.au'
        self.test_recipient = 'tim@xyz.net.au'
        self.message_html = """\
<html>
  <head></head>
  <body>
    <h1>Hi!</h1><br>
       How <b>are</b> you?<br>
       Here is the <a href="http://www.python.org:80">link</a> <em>you</em> wanted.
    </p>
  </body>
</html>
        """
        self.message_plain = "This is plain text"

class TestGoogle_create_message(TestGoogle_meta_class):
    def test_create_object(self):
        gmail = Google_apps_mail(self.client_email,self.test_user,self.key_path)
        self.assertTrue(gmail)

    def test_create_message_html_only(self):
        gmail = Google_apps_mail(self.client_email,self.test_user,self.key_path)
        message = gmail.CreateMessage(self.test_user, self.test_recipient,'subject is test v2, send HTML only',message_html=self.message_html)
        self.assertTrue(message)

    def test_create_message_plaintext_only(self):
        gmail = Google_apps_mail(self.client_email,self.test_user,self.key_path)
        message = gmail.CreateMessage(self.test_user,self.test_recipient,'subject is test v2, send plain text only',message_text=self.message_plain)
        self.assertTrue(message)

    def test_create_message_bothtypes_only(self):
        gmail = Google_apps_mail(self.client_email,self.test_user,self.key_path)
        message = gmail.CreateMessage(self.test_user,self.test_recipient,'subject is test v2, send both plain and html',message_text=self.message_plain,message_html=self.message_html)
        self.assertTrue(message)

class TestGoogle_send_message(TestGoogle_meta_class):
    def test_send_plain_text(self):
        gmail = Google_apps_mail(self.client_email,self.test_user,self.key_path)
        message = gmail.CreateMessage(self.test_user,self.test_recipient,'subject is test v2, send plain text only',message_text=self.message_plain)
        message_id=gmail.SendMessage(self.test_user,message)
        self.assertTrue(message_id)

    def test_send_html_only(self):
        gmail = Google_apps_mail(self.client_email,self.test_user,self.key_path)
        message = gmail.CreateMessage(self.test_user,self.test_recipient,'subject is test v2, send HTML only',message_html=self.message_html)
        message_id = gmail.SendMessage(self.test_user,message)
        self.assertTrue(message_id)

    def test_send_both_types(self):
        gmail = Google_apps_mail(self.client_email,self.test_user,self.key_path)
        message = gmail.CreateMessage(self.test_user,self.test_recipient,'subject is test v2, send both plain and html',message_text=self.message_plain,message_html=self.message_html)
        message = gmail.SendMessage(self.test_user,message)
        self.assertTrue(message)

class TestGoogle_drafts(TestGoogle_meta_class):
    def test_create_draft_text(self):
        gmail = Google_apps_mail(self.client_email, self.test_user, self.key_path)
        message = gmail.CreateMessage(self.test_user, self.test_recipient, 'draft test , send plain text only',
                                      message_text=self.message_plain)
        draft = gmail.CreateDraft(self.test_user,message)
        self.assertTrue(draft)

    def test_create_draft_html_only(self):
        gmail = Google_apps_mail(self.client_email, self.test_user, self.key_path)
        message = gmail.CreateMessage(self.test_user, self.test_recipient, 'subject is test v2, send HTML only',
                                  message_html=self.message_html)
        draft = gmail.CreateDraft(self.test_user,message)
        self.assertTrue(draft)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGoogle_create_message)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGoogle_send_message)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGoogle_drafts)
    unittest.TextTestRunner(verbosity=2).run(suite)



