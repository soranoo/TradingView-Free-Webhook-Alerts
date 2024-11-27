"""email_processing: Optional processing methods to be used with EmailListener.listen().

Example:

    # Create the EmailListener
    email = "example@gmail.com"
    password = "badpassword"
    folder = "Inbox"
    attachment_dir = "/path/to/attachments"
    el = EmailListener(email, password, folder, attachment_dir)

    # Pass to the listen() function
    timeout = 5
    el.listen(timeout, process_func=write_txt_file)

"""

# Imports from other packages
import json
import os
# Imports from this package
from .email_responder import EmailResponder


def write_txt_file(email_listener, msg_dict):
    """Write the email message data returned from scrape to text files.

    Args:
        email_listener (EmailListener): The EmailListener object this function
            is used with.
        msg_dict (dict): The dictionary of email message data returned by the
            scraping function.

    Returns:
        A list of file paths of files that were created and written to.

    """

    # List of files to be returned
    file_list = []
    # For each key, create a file and ensure it doesn't exist
    for key in msg_dict.keys():
        file_path = os.path.join(email_listener.attachment_dir, f"{key}.txt")
        if os.path.exists(file_path):
            print("File has already been created.")
            continue

        with open(file_path, "w+") as file:
            # Conver the message data to a string, and write it to the file
            msg_string = __msg_to_str(msg_dict[key])
            file.write(msg_string)
        # Add the file name to the return list
        file_list.append(file_path)

    return file_list


def __msg_to_str(msg):
    """Convert a dictionary containing message data to a string.

    Args:
        msg (dict): The dictionary containing the message data.

    Returns:
        A string version of the message

    """

    # String to be returned
    msg_string = ""

    # Append the subject
    subject = msg.get('Subject')
    msg_string += f"Subject\n\n{subject}\n\n\n"

    # Append the plain text
    plain_text = msg.get('Plain_Text')
    if plain_text is not None:
        msg_string += f"Plain_Text\n\n{plain_text}\n\n\n"

    # Append the plain html and html
    plain_html = msg.get('Plain_HTML')
    html = msg.get('HTML')
    if plain_html is not None:
        msg_string += f"Plain_HTML\n\n{plain_html}\n\n\n"
        msg_string += f"HTML\n\n{html}\n\n\n"

    # Append the attachment list
    attachments = msg.get('attachments')
    if attachments is None:
        return msg_string

    msg_string += "attachments\n\n"
    for file in attachments:
        msg_string += f"{file}\n"

    return msg_string


def send_basic_reply(email_listener, msg_dict):
    """Write the messages to files, and then send a simple automated reply.

    Args:
        email_listener (EmailListener): The EmailListener object this function
            is used with.
        msg_dict (dict): The dictionary of email message data returned by the
            scraping function.

    Returns:
        A list of file paths of files that were created and written to.

    """

    # Write the email messages to files for use later
    file_list = write_txt_file(email_listener, msg_dict)

    er = EmailResponder(email_listener.email, email_listener.app_password)
    er.login()

    # Create the automated response
    subject = "Thank you!"
    message = "Thank you for your email, your request is being processed."

    # For each email
    for key in msg_dict.keys():
        # Split the key up to remove the email uid
        sender_email_parts = key.split('_')
        sender_email = "_".join(sender_email_parts[1:])
        # Send the email
        er.send_singlepart_msg(sender_email, subject, message)

    er.logout()

    return file_list


def write_json_file(email_listener, msg_dict):
    """Write the email message data returned from scrape to json files.

    Args:
        email_listener (EmailListener): The EmailListener object this function
            is used with.
        msg_dict (dict): The dictionary of email message data returned by the
            scraping function.

    Returns:
        A list of file paths of files that were created and written to.

    """

    # List of files to be returned
    file_list = []
    # For each key, create a file and ensure it doesn't exist
    for key in msg_dict.keys():
        file_path = os.path.join(email_listener.attachment_dir, f"{key}.json")
        if os.path.exists(file_path):
            print("File has already been created.")
            continue

        # Convert the returned dict to json
        json_obj = json.dumps(msg_dict[key], indent = 4)

        with open(file_path, "w+") as file:
            # Write the json object to the file
            file.write(json_obj)
        # Add the file name to the return list
        file_list.append(file_path)

    return file_list

