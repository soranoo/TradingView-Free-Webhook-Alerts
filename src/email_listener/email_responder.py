"""email_responder: Log into an email and send emails.

Example:

    # Initialize the email responder
    responder = EmailResponder(example@email.com, badpassword)
    # Login
    responder.login()
    # The recipient for the email
    recipient = "other@email.com"
    # The subject of the emails
    subject = "This is the subject"
    # Plain text version of the email
    text = "This is the body of the email."
    # HTML version of the email
    html = '''\
    <html>
      <body>
        <img src="cid:image0"/>
        <br>
        <p>This is the body of the email.</p>
        <br>
        <img src="cid:image1"/>
      </body>
    </html>'''
    # List of images
    images = ["./images/example1.png", "./images/example2.png"]
    # List of attachments
    attachments = ["./some_file.txt", "./folder/another_file.pdf"]

    # Sends a plain text email
    responder.send_singlepart_msg(recipient, subject, text)
    # Sends a multipart (MIME) email with only plain text
    responder.send_multipart_msg(recipient, subject, text)
    # Sends a multipart (MIME) email with all options
    responder.send_multipart_msg(recipient, subject, text, html, images, attachments)

"""

# Imports from other packages
import os
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl


class EmailResponder:
    """EmailResponder object for sending emails.

    Attributes:
        email (str): The email to send emails from.
        app_password (str): The password for the email.
        server (SMTP_SSL): The SMTP server to use. Defaults to None.

    """

    def __init__(self, email, app_password):
        """Initialize an EmailResponder instance.

        Args:
            email (str): The email to send emails from.
            app_password (str): The password for the email.

        """

        self.email = email
        self.app_password = app_password
        self.server = None


    def login(self, host="smtp.gmail.com", port=465):
        """Logs in the EmailResponder to the SMTP server.

        Args:
            host (str): The smtp host to log into. Default host is Gmail.
            port (int): The port number to connect through. Default port is
                465, which is needed for a secure SSL connection.

        Returns:
            None

        """

        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(host, port, context=context)
        self.server.login(self.email, self.app_password)


    def logout(self):
        """Logs out the EmailResponder from the SMTP server.

        Args:
            None

        Returns:
            None

        """

        self.server.quit()
        self.server = None


    def send_singlepart_msg(self, recipient, subject, text):
        """Sends a plain text email to the recipient.

        Args:
            recipient (str): The email address to send the email to.
            subject (str): The subject of the email.
            text (str): The message of the email.

        Returns:
            None

        """

        msg = "Subject: {}\n\n{}".format(subject, text)
        self.server.sendmail(self.email, recipient, msg)
        return


    def send_multipart_msg(self, recipient, subject, text, **kwargs):
        """Sends a multipart (MIME) email to the recipient.

        Args:
            recipient (str): The email address to send the email to.
            subject (str): The subject of the email.
            text (str): The plain text version of the message.
            **kwargs (dict): Additional message parts. Options include:
                    html (str): The HTML version of the message. Optional
                        argument that defaults to None.
                    images (list): A list of imbedded image file paths for the
                        HTML messages. Optional argument that defaults to None.
                    attachments (list): A list of file paths for files to attach
                        to the email. Optional argument that defaults to None.

        Returns:
            None

        """

        # Process kwargs
        html = kwargs.get('html')
        images = kwargs.get('images')
        attachments = kwargs.get('attachments')

        # Overall message object
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = recipient

        # Create the body
        msg_body = MIMEMultipart("alternative")
        msg_body.attach(MIMEText(text, "plain"))

        # If there is an html part, attach it
        if html is not None:
            # Create a new multipart section
            msg_html = MIMEMultipart("related")
            # Attach the html text
            msg_html.attach(MIMEText(html, "html"))

            # If there are images, include them
            for i in range(len(images or [])):
                # Open the image, read it, and name it so that it can be
                # referenced by name in the html as:
                # <img src="cid:image[i]">
                # where [i] is the index of the image in images
                fp = open(images[i], 'rb')
                img_type = images[i].split('.')[-1]
                img = MIMEImage(fp.read(), _subtype=img_type)
                img.add_header('Content-ID', "<image{}>".format(i))
                fp.close()
                # Attach the image to the html part
                msg_html.attach(img)

            # Attach the html section to the alternative section
            msg_body.attach(msg_html)

        # Attach the alternative section to the message
        msg.attach(msg_body)

        # Attach each attachment
        for file in attachments or []:
            # Open the file
            f = open(file, "rb")
            # Read in the file, and give set the header
            part = MIMEApplication(f.read())
            part.add_header('Content-Disposition',
                    "attachment; filename={}".format(os.path.basename(file)))
            # Attach the attachment to the message
            f.close()
            msg.attach(part)

        # Send the email
        self.server.sendmail(self.email, recipient, msg.as_string())
        return

