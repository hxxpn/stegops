import os
from struct import unpack
from typing import Any

BMP_EXTENSION = "bmp"
HEADER_BMP_SIGNATURE = b"BM"


def read_image_binary(file_name: str) -> bytes:
    if not file_name:  # falsy validation
        raise ValueError(f"File path is not a valid value: {file_name}")

    if file_name.split(".")[-1] != BMP_EXTENSION:  # extension validation
        raise ValueError(
            f"File extension is not correct: {file_name.split('.')[-1]} instead of {BMP_EXTENSION}"
        )

    if file_name[0] != "/":
        file_name = "/" + file_name

    with open(os.getcwd() + file_name, mode="rb+") as fp:
        return fp.read()


# validates image signature
def is_valid_bmp_file(header_bytes: bytes) -> bool:
    signature_match = b"".join(unpack("<cc", header_bytes[0:2])) == HEADER_BMP_SIGNATURE

    return all([signature_match])


def get_image_info(image_bytes: bytes) -> dict[str, Any]:
    return {
        "file_size": unpack("<I", image_bytes[2:6])[0],
        "image_size": unpack("<I", image_bytes[14:18])[0],
        "width": unpack("<I", image_bytes[18:22])[0],
        "height": unpack("<I", image_bytes[22:26])[0],
    }


# Method that opens the BMP image given the filename
def open_bmp_image(file_name: str) -> list[list[int]]:
    image_bytes: bytes = read_image_binary(file_name)
    is_valid_bmp_file(image_bytes[0:14])
    image_info = get_image_info(image_bytes)
    return []
