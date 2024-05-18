from dataclasses import field, dataclass
from datetime import datetime
from typing import Optional

from utils.serialize import Serializable


@dataclass(kw_only=True)
class Task(Serializable):
    """ Dataclass containing data for a specific task """
    year: int = 2024
    title: str = 'Task 1'
    team_size: int = 1
    deadline_timestamp: int = datetime.now().timestamp()
    submissions: dict = field(default_factory=dict)


@dataclass(kw_only=True)
class SubmissionsMessage(Serializable):
    """ Dataclass containing IDs of the submission list message """
    channel_id: Optional[int] = None
    message_id: Optional[int] = None


@dataclass(kw_only=True)
class Config(Serializable):
    """ Main dataclass containing all persistent data """
    guild_id: Optional[int] = None
    task: Task = Task()
    host_channel_id: Optional[int] = None
    submissions_message: SubmissionsMessage = SubmissionsMessage()
    nicknames: dict = field(default_factory=dict)
    teams: dict = field(default_factory=dict)
