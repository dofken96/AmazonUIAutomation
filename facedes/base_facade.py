from __future__ import annotations

from typing import Callable, Iterable, Tuple

from factories.page_factory import PageFactory
from utils.invocation_chain import InvocationChain


Step = Tuple[str, Callable[[], None]]


class BaseFacade:
    def __init__(self, page):
        self.page = page
        self.page_factory = PageFactory(page)

    def invoke(self, steps: Iterable[Step]) -> None:
        chain = InvocationChain()
        for name, action in steps:
            chain.add(name=name, action=action)
        chain.execute()

