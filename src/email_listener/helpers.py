"""Helper functions for email_listener.

Examples:

    # Calculate the timeout in 5 minutes
    timeout = calc_timeout(5)

    # Calculate the timeout to be at 1:30pm
    timeout = calc_timeout([13, 30])

    # Get the current time for timeout comparison
    time = get_time()

"""

import datetime


def calc_timeout(timeout):
    """Calculate the time when a timeout should occur in seconds since epoch.

    Args:
        timeout (int or list): Either an integer representing the number of
            minutes to timeout in, or a list, formatted as [hour, minute] of
            the local time to timeout at.

    Returns:
        The timeout time in number of sections since epoch.

    """

    # Get datetime object for the current time
    t = datetime.datetime.now()

    # Calculate time offset based on whether timeout is a
    # list or an int of minutes
    if type(timeout) is list:
        hr = (timeout[0] - t.hour) % 24
        mi = (timeout[1] - t.minute) % 60
        sec = 0 - t.second

        if (timeout[1] - t.minute) < 0:
            hr -= 1
            hr = hr % 24
    elif type(timeout) is int:
        # Convert input minutes to hours and minutes
        hr = timeout // 60
        mi = timeout % 60
        sec = 0
    else:
        # Input isn't an int or list, so it is invalid
        err = ( "timeout must be either a list in the format [hours, minutes] "
                "or an integer representing minutes"
        )
        raise ValueError(err)

    # Calculate the change in time between now and the timeout
    t_delta = datetime.timedelta(seconds=sec, minutes=mi, hours=hr)
    # Calculate the timeout in seconds since epoch
    t_out = (t + t_delta).timestamp()

    # Return the timeout
    return t_out


def get_time():
    """Get the current time in seconds since epoch.

    Args:
        None

    Returns:
        The current time in seconds since epoch.

    """

    return datetime.datetime.now().timestamp()

