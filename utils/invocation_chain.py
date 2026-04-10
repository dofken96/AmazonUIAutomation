from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional


StepAction = Callable[[], None]


@dataclass(frozen=True)
class InvocationStep:
    """Single executable step inside a chain."""

    name: str
    action: StepAction


class InvocationChainError(RuntimeError):
    """Raised when a chain step fails."""

    def __init__(self, step_name: str, step_index: int, total_steps: int):
        message = (
            f"Invocation failed at step {step_index}/{total_steps}: {step_name}"
        )
        super().__init__(message)
        self.step_name = step_name
        self.step_index = step_index
        self.total_steps = total_steps


class InvocationChain:
    """Executes a sequence of callable steps in order."""

    def __init__(self) -> None:
        self._steps: List[InvocationStep] = []

    def add(self, name: str, action: StepAction) -> "InvocationChain":
        self._steps.append(InvocationStep(name=name, action=action))
        return self

    def execute(self) -> None:
        total_steps = len(self._steps)
        for index, step in enumerate(self._steps, start=1):
            try:
                step.action()
            except Exception as exc:
                chain_error = InvocationChainError(
                    step_name=step.name,
                    step_index=index,
                    total_steps=total_steps,
                )
                raise chain_error from exc

    @property
    def last_step_name(self) -> Optional[str]:
        if not self._steps:
            return None
        return self._steps[-1].name

