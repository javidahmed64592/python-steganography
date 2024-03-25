from src.steganographer import Steganographer

steg = Steganographer()


def test_given_character_when_creating_byte_list_then_check_correct_list_generated():
    test_chars = ["a", "!", " ", "4", "Z"]
    expected_lists = [
        [1, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 0],
    ]

    for index, char in enumerate(test_chars):
        actual = steg._char_to_byte_list(char)
        assert actual == expected_lists[index]


def test_given_msg_when_creating_bytes_list_then_check_correct_list_generated():
    test_msg = "Hello!"
    expected_bytes = [
        [1, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 1],
    ]
    expected = [bit for byte in expected_bytes for bit in byte]
    actual = steg._msg_to_bytes_list(test_msg)
    assert actual == expected


def test_given_byte_list_when_converting_to_char_then_check_correct_char_returned():
    test_lists = [
        [1, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 0],
    ]
    expected_chars = ["a", "!", " ", "4", "Z"]

    for index, byte in enumerate(test_lists):
        actual = steg._byte_list_to_char(byte)
        assert actual == expected_chars[index]


def test_given_bytes_list_when_converting_to_msg_then_check_correct_msg_returned():
    test_bytes = [
        [1, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 1],
    ]
    test_bytes_list = [bit for byte in test_bytes for bit in byte]
    expected = "Hello!"
    actual = steg._bytes_list_to_msg(test_bytes_list)
    assert actual == expected
