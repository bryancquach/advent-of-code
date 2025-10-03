from enum import Enum
import re

class MullerState(Enum):
    """States for a Muller state machine."""
    START = 0
    M = 1
    MU = 2
    MUL = 3
    OPEN = 4
    FIRST_NUM = 5
    COMMA = 6
    SECOND_NUM = 7
    CLOSE = 8
    PROCESSING = 9

class Muller:
    """A state machine class for string parsing and arithmetic on data streams."""
    # Could set this dynamically based on system limits using sys.maxsize
    MAX_SIGNAL_LENGTH = 20 #including mul(,)

    def __init__(self) -> None:
        self.mul: int = 0
        self.signal: list[str] = []
        self.state: MullerState = MullerState.START

    def update_mul(self, number: int) -> None:
        """Add a number to the current value of 'mul'.
        
        Args:
            number (int): The number to add.
        """
        self.mul += number

    def get_mul(self) -> int:
        """Get the current value of 'mul'."""
        return self.mul
    
    def get_signal(self) -> str:
        """Get the current signal as a concatenated string."""
        return "".join(self.signal)

    def get_stage(self) -> MullerState:
        """Get the current state."""
        return self.state

    def process_event(self, event: str) -> None:
        """Process an event from incoming data stream"""
        match self.state:
            case MullerState.START:
                if event == "m":
                    self._accept(event)
                else:
                    self._reject()
            case MullerState.M:
                if event == "u":
                    self._accept(event)
                else:
                    self._reject()
            case MullerState.MU:
                if event == "l":
                    self._accept(event)
                else:
                    self._reject()
            case MullerState.MUL:
                if event == "(":
                    self._accept(event)
                else:
                    self._reject()
            case MullerState.OPEN:
                if re.match(r"\d", event):
                    self._accept(event)
            case MullerState.FIRST_NUM:
                if re.match(r"\d", event):
                    self._accept(event, update_state=False)
                elif event == ",":
                    self._accept(event)
                else:
                    self._reject()
            case MullerState.COMMA:
                if re.match(r"\d", event):
                    self._accept(event)
            case MullerState.SECOND_NUM:
                if re.match(r"\d", event):
                    self._accept(event, update_state=False)
                elif event == ")":
                    self._accept(event)
                    self._process_signal()
                else:
                    self._reject()
            case _:
                self._reject()
        if len(self.signal) > Muller.MAX_SIGNAL_LENGTH:
            raise ValueError("Signal length exceeded maximum limit.")

    def _process_signal(self) -> None:
        """Internal method to parse string signal."""
        self.state = MullerState.PROCESSING
        signal_str = self.signal.join("")
        match = re.match(r"mul\((\d+),(\d+)\)", signal_str)
        if match:
            first_num = int(match.group(1))
            second_num = int(match.group(2))
            self.update_mul(first_num * second_num)
        else:
            raise ValueError(f"Invalid signal format: {signal_str}")
        self.signal = []

    def _accept(self, ch: str, update_state: bool = True) -> None:
        """Accept a character and append it to the signal."""
        self.signal.append(ch)
        if update_state:
            self.state = MullerState(self.state.value + 1)

    def _reject(self) -> None:
        """Reject the current signal and reset."""
        self.signal = []
        self.state = MullerState.START