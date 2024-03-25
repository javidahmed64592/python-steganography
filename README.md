# python-steganography
A Python steganography application which can be used to insert ASCII strings into images, or extract these strings from modified images.

## Table of Contents

- [python-steganography](#python-steganography)
  - [Table of Contents](#table-of-contents)
  - [Installing Dependencies](#installing-dependencies)
  - [Running the Application](#running-the-application)
  - [Testing](#testing)
  - [Formatting, Type Checking and Linting](#formatting-type-checking-and-linting)

## Installing Dependencies

Install the required dependencies using [pipenv](https://github.com/pypa/pipenv):

    pipenv install
    pipenv install --dev

## Running the Application

Enter the virtual environment with

    pipenv shell

The main application is located in `main.py`.
Execute the following to see what command line arguments need to be included:

    python main.py -h

The application has two modes: encoding and decoding.

Encoding an image allows you to insert a message into a `.png` image file, and outputs a modified `.png` file.
The message must be stored in a `.txt` file which will be read and inserted into the image.

    pipenv run encode --input_img 'my_image.png' --msg_file 'my_message.txt' --output_img 'modified_img.png'

Decoding a modified image extracts a message which has been stored in the image, and outputs a `.txt` file.

    pipenv run decode --input_img 'modified_img.png' --output_file 'decoded_msg.txt'

## Testing

This application uses Pytest for the unit tests.
These tests are located in the `tests` directory.
To run the tests:

    pipenv run test

## Formatting, Type Checking and Linting

This application uses a number of tools for code formatting and linting. These tools are configured in `pyproject.toml`, `setup.cfg` and `mypy.ini`.

Black is used as a code formatter:

    black .

isort is used for tidying up imports:

    isort .

Mypy is used as a type checker:

    mypy .

Flake8 is used for linting:

    flake8
