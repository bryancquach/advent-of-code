from __future__ import annotations
from abc import ABC, abstractmethod
import re


class MulStateMachine:
    """A finite state machine for string parsing and arithmetic on data streams.

    Attributes:
        _state (AbstractState): The current state of the state machine.
        _mul (int): An accumulated multiplication result from parsing 'mul([int],[int])' signals.
        signal (str): The current signal being processed.
        MAX_SIGNAL_LENGTH (int): Maximum allowed length for the signal to prevent overflow.

    """

    # Could set this dynamically based on system limits using sys.maxsize
    MAX_SIGNAL_LENGTH = 20  # including mul(,)

    def __init__(self, disable_dont: bool = False) -> None:
        self._mul: int = 0
        self.signal: str = ""
        self._state: AbstractState = DoState()
        self._state.context = self
        self.disable_dont: bool = disable_dont  # compatibility with part 1 when 'True'

    def set_state(self, state: AbstractState) -> None:
        self._state = state
        self._state.context = self

    @property
    def mul(self) -> int:
        return self._mul

    @mul.setter
    def mul(self, value: int) -> None:
        self._mul = value

    def process_event(self, event: str) -> None:
        if len(self.signal) > self.MAX_SIGNAL_LENGTH:
            raise ValueError(f"Signal length exceeded maximum limit of {self.MAX_SIGNAL_LENGTH}.")
        self._state.process_event(event)


class AbstractState(ABC):

    @property
    def context(self) -> MulStateMachine:
        return self._context

    @context.setter
    def context(self, context: MulStateMachine) -> None:
        self._context = context

    @abstractmethod
    def process_event(self, event: str) -> None:
        pass

    def _reject(self) -> None:
        self.context.signal = ""

    def _accept(self, ch: str) -> None:
        self.context.signal += ch


class MulState(AbstractState):
    """State class for handling 'mul(' prefix and ',' number delimiter."""

    def process_event(self, event: str) -> None:
        match event:
            case "u" if self.context.signal == "m":
                self._accept(event)
            case "l" if self.context.signal == "mu":
                self._accept(event)
            case "(" if self.context.signal == "mul":
                self._accept(event)
                self.context.set_state(NumState())
            case "d" if not self.context.disable_dont:
                self.context.signal = ""
                self._accept(event)
                self.context.set_state(DoState())
            # Switch back to NumState after comma
            case _ if re.match(r"\d", event):
                if re.match(r"mul\(\d+,$", self.context.signal):
                    self._accept(event)
                    self.context.set_state(NumState())
                else:
                    self._reject()
            case _:
                self._reject()

    def _reject(self) -> None:
        self.context.signal = ""
        self.context.set_state(DoState())


class NumState(AbstractState):

    def process_event(self, event: str) -> None:
        match event:
            case "," if re.match(r"mul\(\d+$", self.context.signal):
                self._accept(event)
                self.context.set_state(MulState())
            case ")" if re.match(r"mul\(\d+,\d+$", self.context.signal):
                self._accept(event)
                self._process_signal()
            case "d" if not self.context.disable_dont:
                self.context.signal = ""
                self._accept(event)
                self.context.set_state(DoState())
            case _ if re.match(r"\d", event):
                self._accept(event)
            case _:
                self._reject()

    def _reject(self) -> None:
        self.context.signal = ""
        self.context.set_state(DoState())

    def _process_signal(self) -> None:
        match = re.match(r"mul\((\d+),(\d+)\)", self.context.signal)
        if match:
            first_num = int(match.group(1))
            second_num = int(match.group(2))
            self.context.mul += first_num * second_num
        else:
            raise ValueError(f"Invalid signal format: {self.context.signal}")
        self.context.signal = ""
        self.context.set_state(DoState())


class DoState(AbstractState):

    def process_event(self, event: str) -> None:
        match event:
            case "m" if self.context.signal == "":
                self._accept(event)
                self.context.set_state(MulState())
            case "d" if self.context.signal == "" and not self.context.disable_dont:
                self._accept(event)
            # Can only enter remaining cases if 'disable_dont' is False
            case "o" if self.context.signal == "d":
                self._accept(event)
            case "n" if self.context.signal == "do":
                self._accept(event)
            case "'" if self.context.signal == "don":
                self._accept(event)
            case "t" if self.context.signal == "don'":
                self._accept(event)
            case "(" if self.context.signal == "don't":
                self._accept(event)
            case ")" if self.context.signal == "don't(":
                self.context.signal = ""
                self.context.set_state(DontState())
            case _:
                self._reject()


class DontState(AbstractState):

    def process_event(self, event: str) -> None:
        # Only way out of DontState is to find "do()" signal
        match event:
            case "d" if self.context.signal == "":
                self._accept(event)
            case "o" if self.context.signal == "d":
                self._accept(event)
            case "(" if self.context.signal == "do":
                self._accept(event)
            case ")" if self.context.signal == "do(":
                self.context.signal = ""
                self.context.set_state(DoState())
            case _:
                self._reject()
