import pytest
from stegops import read_image_binary, BMP_EXTENSION, is_valid_bmp_file


@pytest.mark.parametrize("file_name", ["", None, "/owl.bmp", "owl.jpg"])
def test_image_bytes_read(file_name):
    if not file_name:
        with pytest.raises(ValueError):
            _ = read_image_binary(file_name)
    elif file_name.split(".")[-1] != BMP_EXTENSION:
        with pytest.raises(ValueError):
            _ = read_image_binary(file_name)

    else:
        res = read_image_binary(file_name)
        assert isinstance(res, bytes)


def test_bmp_header_validation():
    header_bytes = b"BMPADPA"
    result = is_valid_bmp_file(header_bytes)

    assert result
