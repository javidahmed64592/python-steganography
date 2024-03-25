import argparse
from pathlib import Path

from helpers import system_msg
from steganographer import Steganographer


def main(args: argparse.Namespace) -> None:
    """
    Run steganography application with args.

    Parameters:
        args (Namespace): Console arguments, see below
    """
    steg = Steganographer()
    if args.encode:
        steg.encode_img(Path(args.input_img[0]), args.msg_file[0], args.output_img[0])
    elif args.decode:
        msg = steg.decode_img(Path(args.input_img[0]))
        system_msg(f"Extracted message: {msg}")
    else:
        system_msg("Error! Need to specify -encode or -decode!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steganography application.")
    parser.add_argument("-encode", action="store_true", help="Insert a message into an image")
    parser.add_argument("-decode", action="store_true", help="Extract a message from an image")
    parser.add_argument("--input_img", type=str, nargs="+", help="Path to image file to encode/decode")
    parser.add_argument("--msg_file", type=str, nargs="+", help="Path to message file to insert into image if encoding")
    parser.add_argument("--output_img", type=str, nargs="+", help="Name for encoded image if encoding")
    args = parser.parse_args()
    main(args)
