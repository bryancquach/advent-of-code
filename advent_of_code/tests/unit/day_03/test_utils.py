from advent_of_code.day_03.utils import (
    Muller,
    MullerState
)
import pathlib
import pytest

SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def file_paths():
    return [
        f"{SCRIPT_DIR}/data/example_data.tsv",  # Example data from challenge description
        f"{SCRIPT_DIR}/data/empty_file.tsv",
        f"{SCRIPT_DIR}/data/no_mul_data.tsv",  # File without a signal
        f"{SCRIPT_DIR}/data/oversized_mul_data",  # File with signal exceeding limit
        f"{SCRIPT_DIR}/data/non_existent_file.tsv",
    ]

@pytest.fixture
def muller_instance():
    return Muller()

def test_initial_state(muller_instance):
    assert muller_instance.get_state() == MullerState.START
    assert muller_instance.get_mul() == 0
    assert muller_instance.get_signal() == ""

def test_update_mul(muller_instance):
    muller_instance.update_mul(5)
    assert muller_instance.get_mul() == 5
    muller_instance.update_mul(10)
    assert muller_instance.get_mul() == 15

def test_reset_mul(muller_instance):
    muller_instance.update_mul(10)
    assert muller_instance.get_mul() == 10
    muller_instance.reset_mul()
    assert muller_instance.get_mul() == 0

def test_get_mul(muller_instance):
    assert muller_instance.get_mul() == 0
    muller_instance.update_mul(7)
    assert muller_instance.get_mul() == 7

def test_get_state(muller_instance):
    assert muller_instance.get_state() == MullerState.START
    muller_instance._accept('m')
    assert muller_instance.get_state() == MullerState.M
    muller_instance._accept('u')
    assert muller_instance.get_state() == MullerState.MU
    muller_instance._accept('l')
    assert muller_instance.get_state() == MullerState.MUL
    muller_instance._accept('(')
    assert muller_instance.get_state() == MullerState.OPEN
    muller_instance._accept('1')
    assert muller_instance.get_state() == MullerState.FIRST_NUM
    muller_instance._accept(',')
    assert muller_instance.get_state() == MullerState.COMMA
    muller_instance._accept('2')
    assert muller_instance.get_state() == MullerState.SECOND_NUM
    muller_instance._accept(')')
    assert muller_instance.get_state() == MullerState.CLOSE
    muller_instance._process_signal()
    assert muller_instance.get_state() == MullerState.START

def test_get_signal(muller_instance):
    assert muller_instance.get_signal() == ""
    muller_instance._accept('m')
    assert muller_instance.get_signal() == "m"
    muller_instance._accept('u')
    assert muller_instance.get_signal() == "mu"
    muller_instance._accept('l')
    assert muller_instance.get_signal() == "mul"
    muller_instance._accept('(')
    assert muller_instance.get_signal() == "mul("
    muller_instance._accept('1')
    assert muller_instance.get_signal() == "mul(1"
    muller_instance._accept(',')
    assert muller_instance.get_signal() == "mul(1,"
    muller_instance._accept('2')
    assert muller_instance.get_signal() == "mul(1,2"
    muller_instance._accept(')')
    assert muller_instance.get_signal() == "mul(1,2)"
    muller_instance._process_signal()
    assert muller_instance.get_signal() == ""

def test_accept(muller_instance):
    muller_instance._accept('m')
    assert muller_instance.get_state() == MullerState.M
    muller_instance._accept('u')
    assert muller_instance.get_state() == MullerState.MU
    muller_instance._accept('l')
    assert muller_instance.get_state() == MullerState.MUL
    muller_instance._accept('(')
    assert muller_instance.get_state() == MullerState.OPEN
    muller_instance._accept('1')
    assert muller_instance.get_state() == MullerState.FIRST_NUM
    muller_instance._accept(',')
    assert muller_instance.get_state() == MullerState.COMMA
    muller_instance._accept('2')
    assert muller_instance.get_state() == MullerState.SECOND_NUM
    muller_instance._accept(')')
    assert muller_instance.get_state() == MullerState.CLOSE
    muller_instance._process_signal()
    assert muller_instance.get_state() == MullerState.START

def test_reject(muller_instance):
    muller_instance._accept('m')
    assert muller_instance.get_state() == MullerState.M
    muller_instance._reject()
    assert muller_instance.get_state() == MullerState.START
    assert muller_instance.get_signal() == ""
    muller_instance._accept('m')
    muller_instance._accept('u')
    assert muller_instance.get_state() == MullerState.MU
    muller_instance._reject()
    assert muller_instance.get_state() == MullerState.START
    assert muller_instance.get_signal() == ""

def test_process_event_example(muller_instance):
    input_sequence = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    for char in input_sequence:
        muller_instance.process_event(char)
    assert muller_instance.get_mul() == 161
    assert muller_instance.get_state() == MullerState.START
    assert muller_instance.get_signal() == ""
