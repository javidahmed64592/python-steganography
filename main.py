import argparse
from pathlib import Path

from src.steganographer import Steganographer


def main(args: argparse.Namespace) -> None:
    """
    Run steganography application with args.

    Parameters:
        args (Namespace): Console arguments, execute `python main.py -h` to see possible arguments
    """
    steg = Steganographer()
    if args.encode:
        steg.encode_img(Path(args.input_img[0]), Path(args.msg_file[0]), Path(args.output_img[0]))
    elif args.decode:
        steg.decode_img(Path(args.input_img[0]), Path(args.output_file[0]))
    else:
        steg.print_error_message()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Steganography application. Run with either `-encode` or `-decode`.")
    parser.add_argument("-encode", action="store_true", help="Insert a message into an image")
    parser.add_argument("-decode", action="store_true", help="Extract a message from an image")
    parser.add_argument("--input_img", type=str, nargs="+", help="Path to image file to encode/decode")
    parser.add_argument("--msg_file", type=str, nargs="+", help="Path to message file to insert into image if encoding")
    parser.add_argument("--output_img", type=str, nargs="+", help="Path for encoded image if encoding")
    parser.add_argument("--output_file", type=str, nargs="+", help="Path to decoded message text file if decoding")
    args = parser.parse_args()
    main(args)
