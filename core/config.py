from dataclasses import field, dataclass
from typing import Optional

from utils.serialize import Serializable

"""
This file contains all the dataclasses that make up the persistent data model. 
All properties should be given defaults, and each dataclass should extend Serializable so 
that they can be converted to JSON automatically.
"""

@dataclass(kw_only=True)
class Task(Serializable):
    """ Dataclass containing data for a specific task """
    year: int = 2024
    title: str = 'Task 1'
    team_size: int = 1
    is_accepting: bool = False
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
