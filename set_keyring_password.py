"""
Will set password to your os keyring.
"""

import keyring
import argparse

if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument(
        "-u",
        "--username",
        type=str,
        required=True
    )
    arg_parse.add_argument(
        "-p",
        "--password",
        type=str,
        required=True
    )
    arg_parse.add_argument(
        "-s",
        "--system",
        type=str,
        required=True
    )
    args = arg_parse.parse_args()

    keyring.set_password(args.system, args.username, args.password)
