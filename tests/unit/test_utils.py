from transfer_market_scraper.utils import encode, decode


def test_when_encode_then_base64_string_returned():
    actual = encode("test string.")
    assert actual == "dGVzdCBzdHJpbmcu"


def test_when_decode_then_decoded_string_returned():
    actual = decode("dGVzdCBzdHJpbmcu")
    assert actual == "test string."
