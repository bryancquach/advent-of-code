from advent_of_code.day_03.utils import MulStateMachine, MulState, NumState, DoState, DontState
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
def part1_state_machine():
    return MulStateMachine(disable_dont=True)


@pytest.fixture
def part2_state_machine():
    return MulStateMachine(disable_dont=False)


def test_state_machine_init(part1_state_machine, part2_state_machine):
    assert isinstance(part1_state_machine._state, DoState)
    assert part1_state_machine.mul == 0
    assert part1_state_machine.signal == ""
    assert part1_state_machine.disable_dont is True

    assert isinstance(part2_state_machine._state, DoState)
    assert part2_state_machine.mul == 0
    assert part2_state_machine.signal == ""
    assert part2_state_machine.disable_dont is False


def test_mul_property(part1_state_machine, part2_state_machine):
    part1_state_machine.mul = 5
    assert part1_state_machine.mul == 5
    part1_state_machine.mul = 2
    assert part1_state_machine.mul == 2

    part2_state_machine.mul = 10
    assert part2_state_machine.mul == 10
    part2_state_machine.mul = 34
    assert part2_state_machine.mul == 34


def test_set_state(part1_state_machine, part2_state_machine):
    part1_state_machine.set_state(DoState())
    assert isinstance(part1_state_machine._state, DoState)
    part1_state_machine.set_state(MulState())
    assert isinstance(part1_state_machine._state, MulState)
    part1_state_machine.set_state(NumState())
    assert isinstance(part1_state_machine._state, NumState)

    part2_state_machine.set_state(DontState())
    assert isinstance(part2_state_machine._state, DontState)
    part2_state_machine.set_state(DoState())
    assert isinstance(part2_state_machine._state, DoState)
    part2_state_machine.set_state(MulState())
    assert isinstance(part2_state_machine._state, MulState)
    part2_state_machine.set_state(NumState())
    assert isinstance(part2_state_machine._state, NumState)


def test_process_event(part1_state_machine, part2_state_machine):
    # Test processing a valid 'mul(3,4)' sequence
    sequence = "mul(3,4)"
    for char in sequence:
        part1_state_machine.process_event(char)
    assert part1_state_machine.mul == 12  # 3 * 4 = 12

    for char in sequence:
        part2_state_machine.process_event(char)
    assert part2_state_machine.mul == 12  # 3 * 4 = 12

    # Test processing an invalid sequence that exceeds MAX_SIGNAL_LENGTH
    long_sequence = "mul(12345678901234567890,1)"
    with pytest.raises(ValueError):
        for char in long_sequence:
            part1_state_machine.process_event(char)
    with pytest.raises(ValueError):
        for char in long_sequence:
            part2_state_machine.process_event(char)
