from mcp.server.fastmcp import FastMCP
import json
import random
import string
import hashlib

mcp = FastMCP("Random string")

@mcp.tool()
def random_string(length: int, lower: bool, upper: bool, numeric: bool, special: bool) -> str:
    """
    Generate a random string of given length with specified character types.
    :param length: Length of the random string
    :param lower: Include lowercase letters
    :param upper: Include uppercase letters
    :param numeric: Include numeric characters
    :param special: Include special characters
    :return: Random string
    """
    char_pool = ""
    if lower:
        char_pool += string.ascii_lowercase
    if upper:
        char_pool += string.ascii_uppercase
    if numeric:
        char_pool += string.digits
    if special:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("At least one character type must be selected.")

    result = ''.join(random.choices(char_pool, k=length))
    return result

@mcp.tool()
def unique_string(seed_text: str, length: int, lower: bool, upper: bool, numeric: bool, special: bool) -> str:
    """
    Generate a unique-like predictable string based on seed_text.
    Using the same seed_text consistently produces the same output.
    """
    # Create a stable seed using sha256.
    seed_value = int(hashlib.sha256(seed_text.encode('utf-8')).hexdigest(), 16) % (2**32)
    rand = random.Random(seed_value)
    char_pool = ""
    if lower:
        char_pool += string.ascii_lowercase
    if upper:
        char_pool += string.ascii_uppercase
    if numeric:
        char_pool += string.digits
    if special:
        char_pool += string.punctuation
    if not char_pool:
        raise ValueError("At least one character type must be selected.")
    return ''.join(rand.choices(char_pool, k=length))

mcp.run(transport="sse")