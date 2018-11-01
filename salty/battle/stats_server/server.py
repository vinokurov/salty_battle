import time
from datetime import datetime
import logging

from dataclasses import dataclass, field
from salty.battle.messages import get_client, get_channel, CHANNEL_VOTES, CHANNEL_CONTROL, CHANNEL_STATS, \
    read_all_messages, CONTROL_START_BATTLE, CONTROL_STOP_BATTLE, VOTE_LEFT, VOTE_RIGHT, publish_message, \
    CHANNEL_VOTES_LEFT, CHANNEL_VOTES_RIGHT, count_messages
from salty.battle.stats_server.algo import BattleContext


logger = logging.getLogger('stats')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('stat_server.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

@dataclass
class StatsServer:
    battle: BattleContext = None

    client = None
    channel_votes = None
    channel_control = None
    channel_stats = None

    timestamp_start: datetime = field(default_factory=datetime.utcnow)
    timestamp_end: datetime = field(default_factory=datetime.utcnow)
    battle_started: bool = False

    def __post_init__(self):
        self.client = get_client()
        self.channel_votes_left = get_channel(self.client, CHANNEL_VOTES_LEFT)
        self.channel_votes_right = get_channel(self.client, CHANNEL_VOTES_RIGHT)
        self.channel_control = get_channel(self.client, CHANNEL_CONTROL)
        self.channel_stats = get_channel(self.client, CHANNEL_STATS)

    def run(self):
        logger.info('SERVER STARTED')
        while True:
            self.timestamp_end = datetime.utcnow()
            self.read_control_messages()
            if self.battle_started:
                self.read_vote_messages()
                self.publish_stats()
            self.timestamp_start = self.timestamp_end
            time.sleep(1 - datetime.now().microsecond/1e6)

    def start_battle(self):
        self.battle = BattleContext()
        self.battle_started = True

        publish_message(self.channel_stats, 'start_battle', '')
        logger.info('BATTLE STARTED')

    def stop_battle(self):
        self.battle_started = False
        #TODO: winner
        if self.battle.scores.left.total >= self.battle.scores.right.total:
            winner = 'left'
        else:
            winner = 'right'
        publish_message(self.channel_stats, 'stop_battle', winner)
        logger.info(f'BATTLE STOPPED, winner: {winner}')

    def read_vote_messages(self):
        left = count_messages(self.channel_votes_left, self.timestamp_start, self.timestamp_end)
        right = count_messages(self.channel_votes_right, self.timestamp_start, self.timestamp_end)

        logger.info(f'Received votes. Left: {left}. Right: {right}')
        self.battle.add_votes(left, right)
        # print(self.battle.scores)

    def read_control_messages(self):
        for message in read_all_messages(self.channel_control, self.timestamp_start, self.timestamp_end):
            name, data, timestamp = message
            logger.info(message)
            if name == CONTROL_START_BATTLE:
                self.start_battle()
            elif name == CONTROL_STOP_BATTLE:
                self.stop_battle()
            elif name == 'bonus_z_threshold':
                self.battle.bonus_z_threshold = float(data)
                print('bonus_z_threshold', self.battle.bonus_z_threshold)

    def publish_stats(self):
        msg = self.battle.scores.to_json()
        publish_message(self.channel_stats, 'score', msg)
        logger.info(msg)
        # publish_message(self._channel_stats, 'scores', msg)
        msg_details = {
            'l_mean': self.battle.stats_left.rolling_mean,
            'l_std': self.battle.stats_left.rolling_stdev,
            'l_val': self.battle.stats_left.current_y,
            'l_z': self.battle.stats_left.z_score,
            'l_total': self.battle.scores.left.total,
            'r_mean': self.battle.stats_right.rolling_mean,
            'r_std': self.battle.stats_right.rolling_stdev,
            'r_val': self.battle.stats_right.current_y,
            'r_z': self.battle.stats_right.z_score,
            'r_total': self.battle.scores.right.total,
        }
        publish_message(self.channel_stats, 'stats_details', msg_details)
        logger.info(msg_details)


def main():
    # logger.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    server = StatsServer()
    server.run()


if __name__ == '__main__':
    main()
