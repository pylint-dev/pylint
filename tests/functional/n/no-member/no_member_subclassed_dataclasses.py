from abc import ABCMeta, abstractmethod
import dataclasses as dc
from typing import Any, Dict

@dc.dataclass(frozen=True)
class DeploymentState(metaclass=ABCMeta):
    type: str

    @abstractmethod
    def to_dict(self) -> Dict:
        """
        Serializes given DeploymentState instance to Dict.
        :return:
        """

@dc.dataclass(frozen=True)
class DeploymentStateEcs(DeploymentState):
    blue: Any
    green: Any
    candidate: Any

    def to_dict(self) -> Dict:
        return {
            'type': self.type,
            'blue': dc.asdict(self.blue),
            'green': dc.asdict(self.green),
            'candidate': self.candidate.value,
        }

@dc.dataclass(frozen=True)
class DeploymentStateLambda(DeploymentState):
    current: Any
    candidate: Any

    def to_dict(self) -> Dict:
        return {
            'type': self.type,
            'current': dc.asdict(self.current),
            'candidate': dc.asdict(self.candidate) if self.candidate else None,
        }
