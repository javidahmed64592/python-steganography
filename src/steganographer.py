from pathlib import Path
from typing import List, Tuple, cast

import numpy as np
import skimage as ski
from numpy.typing import NDArray

from helpers import system_msg


class Steganographer:
    def __init__(self):
        self._img: NDArray
        self._img_shape: Tuple[int, ...]
        self._img_dir: Path
        self._img_array: NDArray
        self._msg: str

    @staticmethod
    def _even_img(img: NDArray) -> NDArray:
        img_array: NDArray = img - (img % 2)
        return img_array

    @staticmethod
    def _char_to_bytes_list(char: str) -> List[int]:
        _char_bin = bin(ord(char))
        _char_bytes = _char_bin[2:]
        _padding = [0] * (7 - len(_char_bytes))
        bytes_list = _padding + [int(b) for b in _char_bytes]
        return bytes_list

    @staticmethod
    def _msg_to_bytes_list(msg: str) -> List[int]:
        bytes_list = []
        for _char in msg:
            bytes_list += Steganographer._char_to_bytes_list(_char)
        return bytes_list

    @staticmethod
    def _bytes_list_to_char(bytes_list: List[int]) -> str:
        _b = np.array([2 ** (6 - i) for i in range(7)])
        _char_ord = np.sum(_b * bytes_list)
        char = chr(_char_ord)
        return char

    @staticmethod
    def _bytes_list_to_msg(bytes_list: List[int]) -> str:
        _char_list = []
        i = 0
        while True:
            _char_bytes = bytes_list[i : i + 7]
            _char = Steganographer._bytes_list_to_char(_char_bytes)
            if ord(_char) == 0:
                break

            _char_list.append(_char)
            i += 7

        msg = "".join(_char_list)
        return msg

    def _load_img(self, filepath: Path) -> None:
        system_msg(f"Loading image '{filepath}'...")
        self._img = ski.io.imread(filepath)
        self._img_shape = self._img.shape
        self._img_dir = filepath.parent

    def _save_img(self, filename: str) -> None:
        system_msg(f"Saving image '{filename}.png'...")
        ski.io.imsave(self._img_dir / f"{filename}.png", self._img)

    def _make_img_array(self) -> None:
        system_msg("Making image array...")
        self._img_array = self._img.flatten()

    def _recreate_img(self) -> None:
        system_msg("Recreating image...")
        self._img = np.reshape(self._img_array, self._img_shape)

    def _insert_msg(self, msg: str) -> None:
        system_msg(f"Inserting message '{msg}' into image...")
        self._img_array = Steganographer._even_img(self._img_array)
        _msg_bytes = np.array(Steganographer._msg_to_bytes_list(msg), dtype="uint8")
        self._img_array[: len(_msg_bytes)] += _msg_bytes
        self._recreate_img()

    def _extract_msg(self) -> None:
        system_msg("Extracting message...")
        _msg_bytes = cast(List[int], self._img_array % 2)
        _char_list = Steganographer._bytes_list_to_msg(_msg_bytes)
        self._msg = "".join(_char_list)

    def encode_img(self, filepath: Path, msg: str, output_name: str) -> None:
        self._load_img(filepath)
        self._make_img_array()
        self._insert_msg(msg)
        self._save_img(output_name)

    def decode_img(self, filepath: Path) -> str:
        self._load_img(filepath)
        self._make_img_array()
        self._extract_msg()
        return self._msg
