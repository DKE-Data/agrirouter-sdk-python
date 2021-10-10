"""Test agrirouter/messaging/decode.py"""

from agrirouter.messaging.decode import read_properties_buffers_from_input_stream


def test_read_properties_buffers_from_input_stream():
    test_func = read_properties_buffers_from_input_stream((1, 2, 3))
    assert test_func == ((2,), ())
    test_func = read_properties_buffers_from_input_stream(())
    assert test_func == ()
    test_tuple = [i for i in range(1, 10)]
    test_func = read_properties_buffers_from_input_stream(test_tuple)
    assert test_func == ([2], [4, 5, 6], [8, 9])
