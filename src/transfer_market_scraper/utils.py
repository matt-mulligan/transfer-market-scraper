"""
transfer_market_scraper.utils

module for generic utils that don't fit anywhere else
"""

import base64


def encode(msg: str) -> str:
    """
    generic base64 encode method

    :param msg: normal string to encode
    :return: encoded base64 string
    """

    msg_bytes = msg.encode("ascii")
    b64_bytes = base64.b64encode(msg_bytes)
    return b64_bytes.decode("ascii")


def decode(b64_msg: str) -> str:
    """
    generic base64 decoder method

    :param b64_msg: base64 ascii string to decode
    :return: decoded ascii string
    """

    b64_bytes = b64_msg.encode("ascii")
    b64_bytes = base64.b64decode(b64_bytes)
    return b64_bytes.decode("ascii")


