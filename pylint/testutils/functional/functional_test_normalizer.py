from pathlib import Path
from typing import List, Union

from pylint.message import MessageDefinition, MessageDefinitionStore


class FunctionalTestNormalizer:

    """Help normalize the functional tests based on the content of the MessageStore."""

    def __init__(
        self,
        base_functional_directory: Union[Path, str],
        msg_store: MessageDefinitionStore,
    ):
        self.base_functional_directory = Path(base_functional_directory)
        self.message_store = msg_store

    def __iter__(self):
        yield from self.message_store.messages

    def expected_directories(self, message: MessageDefinition) -> List[Path]:
        """The normalized directory that should contain the functional test for a message"""
        return [
            self.base_functional_directory / message.symbol[0] / d
            for d in (
                message.symbol,
                message.symbol.replace("-", "_"),
            )
        ]
