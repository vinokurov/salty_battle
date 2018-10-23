import numpy as np
from dataclasses import dataclass, field
from salty.battle.messages import ScoreUpdateMsg, ScoreUpdateOne


@dataclass
class StatsContext:
    filtered_y: np.array = None
    current_y: int = None
    window: int = 10
    threshold: float = 2.0
    influence: float = 0.5

    def __post_init__(self):
        self.filtered_y = np.array([])

    def add_observation(self, y):
        self.current_y = y
        if len(self.filtered_y) > self.window:
            if y - self.rolling_mean > self.rolling_stdev * self.threshold:
                self.filtered_y = np.append(self.filtered_y, y*self.influence + self.filtered_y[-1] * (1-self.influence))
            else:
                self.filtered_y = np.append(self.filtered_y, y)
        else:
            self.filtered_y = np.append(self.filtered_y, y)

    @property
    def z_score(self):
        if len(self.filtered_y) > self.window:
            if self.rolling_stdev > 1 and self.rolling_mean > 1:
                return (self.current_y - self.rolling_mean) / self.rolling_stdev
        return 0

    @property
    def rolling_mean(self):
        return np.mean(self.filtered_y[-self.window - 1:-1])

    @property
    def rolling_stdev(self):
        return np.std(self.filtered_y[-self.window - 1:-1])


@dataclass
class BattleContext:
    scores: ScoreUpdateMsg = field(default_factory=ScoreUpdateMsg)
    stats_left: StatsContext = field(default_factory=StatsContext)
    stats_right: StatsContext = field(default_factory=StatsContext)

    bonus_score: int = 100
    bonus_z_threshold: int = 2

    def _calculate_score(self, stats_context, score_other):
        score = stats_context.current_y * 1
        is_bonus = False
        if stats_context.z_score and stats_context.z_score > self.bonus_z_threshold:
            score += max(int(score_other / 3.0), self.bonus_score)
            is_bonus = True
        return score, is_bonus

    @staticmethod
    def _update_score(score_msg: ScoreUpdateOne, new_score, is_bonus):
        score_msg.increment = new_score
        score_msg.total += new_score
        score_msg.is_bonus = is_bonus

    def add_votes(self, votes_left, votes_right):
        self.stats_left.add_observation(votes_left)
        self.stats_right.add_observation(votes_right)

        score_l, is_bonus_l = self._calculate_score(self.stats_left, self.scores.right.total)
        score_r, is_bonus_r = self._calculate_score(self.stats_right, self.scores.left.total)

        self._update_score(self.scores.left, score_l, is_bonus_l)
        self._update_score(self.scores.right, score_r, is_bonus_r)

        print(self.stats_left.rolling_mean, self.stats_left.rolling_stdev, self.stats_left.z_score)
