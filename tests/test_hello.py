from modules.hello import get_hello_str


def test_get_hello_str():
    assert get_hello_str() == 'Hello world!'
