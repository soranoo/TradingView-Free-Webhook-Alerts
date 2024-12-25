# -----------------* Modified *-----------------
# original: https://github.com/njdreikosen/email_listener/blob/master/email_listener/__init__.py
# ----------------------------------------------

"""email_listener: Listen in an email folder and process incoming emails.

Example:

    # Create the listener
    listener = EmailListener("example@email.com", "badpassword", "Inbox", "./files/")
    # Log the listener into the IMAP server
    listener.login()
    # Scrape emails from the folder without moving them
    listener.scrape()
    # Scrape emails from the folder, and move them to the "email_listener" folder
    listener.scrape("email_listener")
    # Listen in the folder for 5 minutes, without moving the emails, and not
    # calling any process function on the emails.
    listener.listen(5)
    # Listen in the folder until 1:30pm, moving each new email to the "email_listener"
    # folder, and calling the processing function 'send_reply()'
    listener.listen([13, 30], "email_listener", send_reply)
    # Log the listener out of the IMAP server
    listener.logout()

"""

# Imports from other packages
import email
import html2text
from imapclient import IMAPClient, SEEN
import os

from datetime import datetime

# Imports from this package
from .helpers import (
    calc_timeout,
    get_time,
)
from .email_processing import write_txt_file


class EmailListener:
    """EmailListener object for listening to an email folder and processing emails.

    Attributes:
        email (str): The email to listen to.
        app_password (str): The password for the email.
        folder (str): The email folder to listen in.
        attachment_dir (str): The file path to the folder to save scraped
            emails and attachments to.
        server (IMAPClient): The IMAP server to log into. Defaults to None.

    """

    def __init__(self, email, app_password, folder="Inbox", attachment_dir=f"{os.getcwd()}/data/email attachments", logger=print, imap_address="imap.gmail.com", imap_port=993):
        """Initialize an EmailListener instance.

        Args:
            email (str): The email to listen to.
            app_password (str): The password for the email.
            folder (str): The email folder to listen in.
            attachment_dir (str): The file path to folder to save scraped
                emails and attachments to.
            logger (function): The function for messages printed to the console.
            imap_address (str): The IMAP server to log into. Defaults to Gmail (imap.gmail.com).
            imap_port (int): The port to log into the IMAP server on. Defaults to 993.
        Returns:
            None

        """

        # create attachment directory if it's not exist.
        if not os.path.exists(attachment_dir):
            os.makedirs(attachment_dir)

        self.email = email
        self.app_password = app_password
        self.folder = folder
        self.attachment_dir = attachment_dir
        self.server = None
        self.logger = logger
        self.imap_address = imap_address
        self.imap_port = imap_port


    def login(self):
        """Logs in the EmailListener to the IMAP server.

        Args:
            None

        Returns:
            None

        """

        self.server = IMAPClient(self.imap_address, self.imap_port)
        self.server.login(self.email, self.app_password)
        self.server.select_folder(self.folder, readonly=False)


    def logout(self):
        """Logs out the EmailListener from the IMAP server.

        Args:
            None

        Returns:
            None

        """

        self.server.logout()
        self.server = None

    def scrape(self, move=None, unread=False, delete=False, search_filter="UNSEEN", latest_only=False, no_log = False):
        """Scrape unread emails from the current folder.

        Args:
            move (str): The folder to move the emails to. If None, the emails
                are not moved. Defaults to None.
            unread (bool): Whether the emails should be marked as unread.
                Defaults to False.
            delete (bool): Whether the emails should be deleted. Defaults to
                False.
            search_filter (str): The search filter to use. Defaults to "UNSEEN".
            latest_only (bool): Get the latest email only(the last email that the user received).
                Defaults to False.
            no_log (bool): Whether to hide the notice. Defaults to False.
        Returns:
            A list of the file paths to each scraped email.

        """

        # Ensure server is connected
        if type(self.server) is not IMAPClient:
            raise ValueError("server attribute must be type IMAPClient")

        # List containing the file paths of each file created for an email message
        msg_dict = {}

        # Search for unseen messages
        messages = self.server.search(search_filter)
        if (latest_only):
            messages = messages[-1]
        # For each unseen message
        for uid, message_data in self.server.fetch(messages, 'RFC822').items():
            # Get the message
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            # Get who the message is from
            from_email = self.__get_from(email_message)

            # Generate the dict key for this email
            key = f"{uid}_{from_email}"
            # Generate the value dictionary to be filled later
            val_dict = {}

            # Display notice
            if (not no_log):
                self.logger(f"PROCESSING: Email UID<{uid}> from {from_email}")

            # Add the email address
            val_dict["From_Address"] = from_email

            # Add the email uid
            val_dict["Email_UID"] = uid

            # Add the date, ref: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            # eg. Wed, 2 Feb 2022 04:16:44 +0000
            val_dict["Date"] = datetime.strptime(self.__get_date(email_message), "%a, %d %b %Y %H:%M:%S %z")

            # Add the subject
            val_dict["Subject"] = self.__get_subject(email_message).strip()

            # If the email has multiple parts
            if email_message.is_multipart():
                val_dict = self.__parse_multipart_message(email_message, val_dict)

            # If the message isn't multipart
            else:
                val_dict = self.__parse_singlepart_message(email_message, val_dict)

            msg_dict[key] = val_dict

            # If required, move the email, mark it as unread, or delete it
            self.__execute_options(uid, move, unread, delete)

        # Return the dictionary of messages and their contents
        return msg_dict


    def __get_from(self, email_message):
        """Helper function for getting who an email message is from.

        Args:
            email_message (email.message): The email message to get sender of.

        Returns:
            A string containing the from email address.

        """

        from_raw = email_message.get_all('From', [])
        from_list = email.utils.getaddresses(from_raw)
        if len(from_list[0]) == 1:
            from_email = from_list[0][0]
        elif len(from_list[0]) == 2:
            from_email = from_list[0][1]
        else:
            from_email = "UnknownEmail"

        return from_email


    def __get_subject(self, email_message):
        """

        """

        # Get the subject
        subject = email_message.get("Subject")
        # If there isn't a subject
        if subject is None:
            return "No Subject"
        return subject

    def __get_date(self, email_message):
        """

        """

        # Get the date
        date = email_message.get("Date")
        # If there isn't a date
        if date is None:
            return False
        return date


    def __parse_multipart_message(self, email_message, val_dict):
        """Helper function for parsing multipart email messages.

        Args:
            email_message (email.message): The email message to parse.
            val_dict (dict): A dictionary containing the message data from each
                part of the message. Will be returned after it is updated.

        Returns:
            The dictionary containing the message data for each part of the
            message.

        """

        # For each part
        for part in email_message.walk():
            # If the part is an attachment
            file_name = part.get_filename()
            if bool(file_name):
                # Generate file path
                file_path = os.path.join(self.attachment_dir, file_name)
                with open(file_path, "wb") as file:
                    file.write(part.get_payload(decode=True))
                # Get the list of attachments, or initialize it if there isn't one
                attachment_list = val_dict.get("attachments", [])
                attachment_list.append(f"{file_path}")
                val_dict["attachments"] = attachment_list

            elif part.get_content_type() == "text/html":
                # Convert the body from html to plain text
                val_dict["Plain_HTML"] = html2text.html2text(
                        part.get_payload())
                val_dict["HTML"] = part.get_payload()

            elif part.get_content_type() == "text/plain":
                # Get the body
                val_dict["Plain_Text"] = part.get_payload()

        return val_dict


    def __parse_singlepart_message(self, email_message, val_dict):
        """Helper function for parsing singlepart email messages.

        Args:
            email_message (email.message): The email message to parse.
            val_dict (dict): A dictionary containing the message data from each
                part of the message. Will be returned after it is updated.

        Returns:
            The dictionary containing the message data for each part of the
            message.

        """

        # Get the message body, which is plain text
        val_dict["Plain_Text"] = email_message.get_payload()
        return val_dict


    def __execute_options(self, uid, move, unread, delete):
        """Loop through optional arguments and execute any required processing.

        Args:
            uid (int): The email ID to process.
            move (str): The folder to move the emails to. If None, the emails
                are not moved. Defaults to None.
            unread (bool): Whether the emails should be marked as unread.
                Defaults to False.
            delete (bool): Whether the emails should be deleted. Defaults to
                False.

        Returns:
            None

        """

        # If the message should be marked as unread
        if bool(unread):
            self.server.remove_flags(uid, [SEEN])

        # If a move folder is specified
        if move is not None:
            try:
                # Move the message to another folder
                self.server.move(uid, move)
            except:
                # Create the folder and move the message to the folder
                self.server.create_folder(move)
                self.server.move(uid, move)
        # If the message should be deleted
        elif bool(delete):
            # Move the email to the trash
            self.server.set_gmail_labels(uid, "\\Trash")
        return


    def listen(self, timeout, update_frequency=30, process_func=write_txt_file, **kwargs):
        """Listen in an email folder for incoming emails, and process them.

        Args:
            timeout (int or list): Either an integer representing the number
                of minutes to timeout in, or a list, formatted as [hour, minute]
                of the local time to timeout at.
            update_frequency (int): Check for new email every certain time.
            process_func (function): A function called to further process the
                emails. The function must take only the list of file paths
                returned by the scrape function as an argument. Defaults to the
                example function write_txt_file in the email_processing module.
            **kwargs (dict): Additional arguments for processing the email.
                Optional arguments include:
                    move (str): The folder to move emails to. If not set, the
                        emails will not be moved.
                    unread (bool): Whether the emails should be marked as unread.
                        If not set, emails are kept as read.
                    delete (bool): Whether the emails should be deleted. If not
                        set, emails are not deleted.
                    latest_only {on development} (bool): Get the latest email only(the last email that the user received).

        Returns:
            None

        """

        # Ensure server is connected
        if type(self.server) is not IMAPClient:
            raise ValueError("server attribute must be type IMAPClient")

        # Get the timeout value
        outer_timeout = calc_timeout(timeout)

        # Run until the timeout is reached
        if timeout == -1:
            while True:
                self.__idle(timeout=update_frequency, process_func=process_func, **kwargs)
        else:
            while (get_time() < outer_timeout):
                self.__idle(timeout=update_frequency, process_func=process_func, **kwargs)
        self.logger("Email listener has stopped, reson: timeout")
        return


    def __idle(self, timeout=30, process_func=write_txt_file, **kwargs):
        """Helper function, idles in an email folder processing incoming emails.

        Args:
            process_func (function): A function called to further process the
                emails. The function must take only the list of file paths
                returned by the scrape function as an argument. Defaults to the
                example function write_txt_file in the email_processing module.
            timeout (int): Idle timeout.
            **kwargs (dict): Additional arguments for processing the email.
                Optional arguments include:
                    move (str): The folder to move emails to. If not set, the
                        emails will not be moved.
                    unread (bool): Whether the emails should be marked as unread.
                        If not set, emails are kept as read.
                    delete (bool): Whether the emails should be deleted. If not
                        set, emails are not deleted.
                    latest_only (bool): Get the latest email only(the last email that the user received).

        Returns:
            None

        """

        # Set the relevant kwarg variables
        move = kwargs.get("move")
        unread = bool(kwargs.get("unread"))
        delete = bool(kwargs.get("delete"))
        latest_only = bool(kwargs.get("latest_only"))

        # Start idling
        self.server.idle()
        # Set idle timeout to 5 minutes
        inner_timeout = get_time() + 60*5
        # Until idle times out
        while (get_time() < inner_timeout):
            # Check for a new response every x seconds
            responses = self.server.idle_check(timeout=timeout)
            # If there is a response
            if (responses):
                # Suspend the idling
                self.server.idle_done()
                # Process the new emails
                msgs = self.scrape(move=move, unread=unread, delete=delete, latest_only=latest_only)
                # Run the process function
                process_func(self, msgs)
                # Restart idling
                self.server.idle()
        # Stop idling
        self.server.idle_done()
        return

