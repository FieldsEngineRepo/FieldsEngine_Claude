import win32com.client

emailTo = ["jason.skophammer@gmail.com"]
# ccTo = ["email@address1.com", "email@address2.com"]
ccTo = []
emailSubject = "Subject of email"
emailBody = """

Body of email

"""
# emailAttachments = ["C:\attachment1.txt", "C:\attachment2.txt"]
emailAttachments = []


def email_out(email_to, email_subject, email_body, CC_to, email_attachments):
    outlookApp = win32com.client.Dispatch("Outlook.Application")
    msg = outlookApp.CreateItem(0)
    if email_to:
        msg.To = ';'.join(email_to)
    if CC_to:
        msg.CC = ';'.join(CC_to)
    msg.Subject = email_subject
    msg.Body = email_body
    if email_attachments:
        for attachment in email_attachments:
            msg.Attachments.Add(attachment)
    msg.Send()

email_out(emailTo, emailSubject, emailBody, ccTo, emailAttachments)