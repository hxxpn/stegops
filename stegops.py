import os
import struct
from enum import Enum
from struct import unpack
from typing import Any

BMP_EXTENSION = "bmp"
HEADER_BMP_SIGNATURE = b"BM"


class Compression(Enum):
    BI_RGB = 0
    BI_RLE8 = 1
    BI_RLE4 = 2


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
        "info_header_size": unpack("<I", image_bytes[14:18])[0],
        "width": unpack("<I", image_bytes[18:22])[0],
        "height": unpack("<I", image_bytes[22:26])[0],
        "planes": int.from_bytes(
            unpack("<cc", image_bytes[26:28])[0], byteorder="little"
        ),
        "bits_per_pixel": int.from_bytes(
            unpack("<cc", image_bytes[28:30])[0], byteorder="little"
        ),
        "compression": unpack("<I", image_bytes[30:34])[0],
        "image_size": unpack("<I", image_bytes[34:38])[0],
    }


def read_image_data(
    image_bytes: bytes, image_info: dict[str, int]
) -> list[list[list[bytes]]]:
    image_data_offset = 14 + image_info["info_header_size"]
    number_of_pixels = image_info["width"] * image_info["height"] * 3
    raw_pixels = list(
        struct.unpack(f"<{number_of_pixels}c", image_bytes[image_data_offset:])
    )
    image_pixels = []
    width, height = image_info["width"], image_info["height"]
    row_padding_bytes = (4 - (width * 3) % 4) % 4
    row_length = width * 3 + row_padding_bytes
    for i in range(height):
        new_row = []
        row = raw_pixels[i * row_length : (i + 1) * row_length]
        for j in range(width):
            bgr = row[j * 3 : (j + 1) * 3]
            new_row.append(bgr[::-1])

        image_pixels.append(new_row)

    return image_pixels


# Method that opens the BMP image given the filename
def open_bmp_image(file_name: str) -> list[list[int]]:
    image_bytes: bytes = read_image_binary(file_name)
    is_valid_bmp_file(image_bytes[0:14])
    image_info = get_image_info(image_bytes)
    print(image_info)
    pixel_data = read_image_data(image_bytes, image_info)
    print(pixel_data)
    return []


def create_a_copy_image(file_name: str) -> None:
    image_bytes = read_image_binary(file_name)
    return
