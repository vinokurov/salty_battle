from datetime import datetime

from ably import AblyRest
from ably.rest.channel import Channel
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from salty.battle.config import ALBY_KEY

CHANNEL_VOTES = 'votes'
CHANNEL_VOTES_LEFT = 'votes_left'
CHANNEL_VOTES_RIGHT = 'votes_right'
CHANNEL_STATS = 'stats'
CHANNEL_CONTROL = 'control'

CONTROL_START_BATTLE = 'start_battle'
CONTROL_STOP_BATTLE = 'stop_battle'

VOTE_LEFT = 'left'
VOTE_RIGHT = 'right'


@dataclass
class BattleStartMsg(DataClassJsonMixin):
    name: str = ''
    left_name: str = None
    right_name: str = None


@dataclass
class ScoreUpdateOne(DataClassJsonMixin):
    total: int = 0
    increment: int = 0
    is_bonus: bool = False
    bonus_message: str = ''


@dataclass
class ScoreUpdateMsg(DataClassJsonMixin):
    left: ScoreUpdateOne = field(default_factory=ScoreUpdateOne)
    right: ScoreUpdateOne = field(default_factory=ScoreUpdateOne)


def get_client():
    return AblyRest(ALBY_KEY)


def get_channel(client: AblyRest, channel_name: str):
    return client.channels.get(channel_name)


def publish_message(channel: Channel, name, data):
    channel.publish(name, data)


def read_all_messages(channel: Channel, timestamp_start: datetime, timestamp_end: datetime = None):
    message_history = channel.history(start=timestamp_start, end=timestamp_end, limit=1000)
    if len(message_history.items) > 0:
        for message in message_history.items:
            yield (message.name, message.data, message.timestamp)


def count_messages(channel: Channel, timestamp_start: datetime, timestamp_end: datetime = None):

    def _get_length(hist):
        if len(hist.items) > 0:
            return len(hist.items)
        return 0

    message_history = channel.history(start=timestamp_start, end=timestamp_end, limit=1000)
    count = _get_length(message_history)
    while message_history.has_next():
        message_history = message_history.next()
        count += _get_length(message_history)
    return count
