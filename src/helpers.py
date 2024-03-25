from datetime import datetime
from pathlib import Path

import skimage as ski
from numpy.typing import NDArray


def system_msg(msg: str) -> None:
    """
    Print a message to the console with the current time.

    Parameters:
        msg (str): Message to print
    """
    print(f"[{datetime.now().isoformat()}] {msg}")


def load_img(filepath: Path) -> NDArray:
    """
    Load an image as an NDArray.

    Parameters:
        filepath (Path): Path to image file

    Returns:
        image_array (NDArray): Image as array of RGBA values
    """
    image_array: NDArray = ski.io.imread(filepath)
    return image_array


def save_img(filepath: Path, img: NDArray) -> None:
    """
    Save image to filepath.

    Parameters:
        filepath (Path): Path to save image
        img (NDArray): Image array to save
    """
    ski.io.imsave(filepath, img)


def read_txt_file(filepath: Path) -> str:
    """
    Read a text file and return its contents.

    Parameters:
        filepath (Path): Path to text file

    Returns:
        contents (str): Contents of text file
    """
    with open(filepath, "r") as file:
        contents = file.read()
        return contents


def write_to_txt_file(filepath: Path, contents: str) -> None:
    """
    Write a string to a text file.

    Parameters:
        filepath (Path): Path to text file
        contents (str): Contents to write to text file
    """
    with open(filepath, "w") as file:
        contents = file.write(contents)
