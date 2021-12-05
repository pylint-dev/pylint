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
        result = []
        intermediate_dirs = (message.checker_name, message.symbol[0])
        leaf_dirs = (message.symbol, message.symbol.replace("-", "_"))
        for intermediate_dir in intermediate_dirs:
            for leaf_dir in leaf_dirs:
                result.append(
                    self.base_functional_directory / intermediate_dir / leaf_dir
                )
        return result
