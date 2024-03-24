import argparse
from datetime import datetime
from pathlib import Path

from steganographer import Steganographer


def system_msg(msg: str) -> None:
    print(f"[{datetime.now().isoformat()}] {msg}")


def main(args):
    steg = Steganographer()
    if args.encode:
        steg.encode_img(Path(args.input_img[0]), args.msg[0], args.output_img[0])
    elif args.decode:
        msg = steg.decode_img(Path(args.input_img[0]))
        system_msg(f"Extracted message: {msg}")
    else:
        system_msg("Error! Need to specify -encode or -decode!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("-encode", action="store_true", help="Insert a message into an image")
    parser.add_argument("-decode", action="store_true", help="Extract a message from an image")
    parser.add_argument("--input_img", type=str, nargs="+", help="Path to image file")
    parser.add_argument("--msg", type=str, nargs="+", help="Message to insert into image")
    parser.add_argument("--output_img", type=str, nargs="+", help="Name for encoded image")
    args = parser.parse_args()
    main(args)
