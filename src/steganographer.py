from pathlib import Path
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from src.helpers import load_img, read_txt_file, save_img, system_msg, write_to_txt_file


class Steganographer:
    _BIT_MAP = np.array([2 ** (6 - i) for i in range(7)])

    def __init__(self):
        """
        Initialise Steganographer object and define types.
        """
        self._img: NDArray
        self._img_shape: Tuple[int, ...]
        self._img_array: NDArray
        self._msg: str

    @staticmethod
    def _even_img(img: NDArray) -> NDArray:
        """
        Round down all values in image array to be even numbers.

        Parameters:
            img (NDArray): Array of RGBA values

        Returns:
            img_even (NDArray): Array of even RGBA values with same shape as `img`
        """
        img_even: NDArray = img - (img % 2)
        return img_even

    @staticmethod
    def _char_to_byte_list(char: str) -> List[int]:
        """
        Convert an ASCII character to a list of bits of length 7.

        ```
        Steganographer._char_to_byte_list("a") # [1, 1, 0, 0, 0, 0, 1]
        ```

        Parameters:
            char (str): Single ASCII character

        Returns:
            byte_list (List[int]): Character represented as a list of bits
        """
        _char_bin = bin(ord(char))
        _char_bytes = _char_bin[2:]
        _padding = [0] * (7 - len(_char_bytes))
        byte_list = _padding + [int(b) for b in _char_bytes]
        return byte_list

    @staticmethod
    def _msg_to_bytes_list(msg: str) -> List[int]:
        """
        Convert an ASCII message to a list of bytes of length (7 * length of message).

        Parameters:
            msg (str): Sequence of ASCII characters

        Returns:
            byte_list (List[int]): Characters represented as a list of bytes
        """
        byte_list = []
        for _char in msg:
            byte_list += Steganographer._char_to_byte_list(_char)
        return byte_list

    @staticmethod
    def _byte_list_to_char(byte_list: List[int]) -> str:
        """
        Convert a list of bits to a character.

        ```
        Steganographer._byte_list_to_char([1, 1, 0, 0, 0, 0, 1]) # "a"
        ```

        Parameters:
            byte_list (List[int]): Character represented as a list of bits

        Returns:
            char (str): Single ASCII character
        """
        _char_ord = np.sum(Steganographer._BIT_MAP * byte_list)
        char = chr(_char_ord)
        return char

    @staticmethod
    def _bytes_list_to_msg(bytes_list: List[int]) -> str:
        """
        Convert a list of bytes to a message.

        Parameters:
            bytes_list (List[int]): Characters represented as a list of bits

        Returns:
            msg (str): Sequence of ASCII characters
        """
        _char_list = []
        i = 0
        while True:
            _char_byte = bytes_list[i : i + 7]
            if not _char_byte:
                break

            _char = Steganographer._byte_list_to_char(_char_byte)
            if ord(_char) == 0:
                break

            _char_list.append(_char)
            i += 7

        msg = "".join(_char_list)
        return msg

    def _load_img(self, filepath: Path) -> None:
        """
        Load an image from filepath.

        Parameters:
            filepath (Path): Path to image file
        """
        system_msg(f"Loading image '{filepath}'...")
        self._img = load_img(filepath)
        self._img_shape = self._img.shape

    def _save_img(self, filepath: Path) -> None:
        """
        Save image using filename in same directory as source image.

        Parameters:
            filepath (Path): Path for output image file
        """
        system_msg(f"Saving image '{filepath}'...")
        save_img(filepath, self._img)

    def _make_img_array(self) -> None:
        """
        Flatten image array.
        """
        system_msg("Making image array...")
        self._img_array = self._img.flatten()

    def _recreate_img(self) -> None:
        """
        Recreate image at original dimensions from image array.
        """
        system_msg("Recreating image...")
        self._img = np.reshape(self._img_array, self._img_shape)

    def _insert_msg(self, msg: str) -> None:
        """
        Insert a message into loaded image.

        Parameters:
            msg (str): Message to insert into image
        """
        system_msg(f"Inserting message of length {len(msg)} into image...")
        self._img_array = Steganographer._even_img(self._img_array)
        _msg_bytes = np.array(Steganographer._msg_to_bytes_list(msg), dtype="uint8")
        self._img_array[: len(_msg_bytes)] += _msg_bytes

    def _extract_msg(self) -> None:
        """
        Extract a message from an image.
        """
        system_msg("Extracting message...")
        _msg_bytes = (self._img_array % 2).tolist()
        _char_list = Steganographer._bytes_list_to_msg(_msg_bytes)
        self._msg = "".join(_char_list)
        system_msg(f"Decoded message length: {len(self._msg)}")

    def _save_msg_to_txt_file(self, filepath: Path) -> None:
        """
        Save decoded message to text file.

        Parameters:
            filepath (Path): Path to output text file
        """
        system_msg(f"Saving message to text file `{filepath}`...")
        write_to_txt_file(filepath, self._msg)

    def encode_img(self, filepath: Path, msg_file: Path, output_img: Path) -> None:
        """
        Insert a message into an image file and save the modified image.

        Parameters:
            filepath (Path): Path to image file
            msg_file (Path): Path to text file with message to insert into image
            output_img (Path): Path for modified image file
        """
        system_msg("=== Encoding image ===")
        system_msg(f"Input image: `{filepath}` | Output image: `{output_img}` | Message file: `{msg_file}`")
        self._load_img(filepath)
        self._make_img_array()
        msg = read_txt_file(msg_file)
        self._insert_msg(msg)
        self._recreate_img()
        self._save_img(output_img)
        system_msg("=== Encoding complete! ===")

    def decode_img(self, filepath: Path, output_file: Path) -> None:
        """
        Extract a message from a modified image.

        Parameters:
            filepath (Path): Path to image file
            output_file (Path): Path to text file with decoded message
        """
        system_msg("=== Decoding image ===")
        system_msg(f"Input image: `{filepath}` | Output file: `{output_file}`")
        self._load_img(filepath)
        self._make_img_array()
        self._extract_msg()
        self._save_msg_to_txt_file(output_file)
        system_msg("=== Decoding complete! ===")

    def print_error_message(self) -> None:
        """
        Print error message to console.
        """
        system_msg("Error! Need to specify -encode or -decode!")
