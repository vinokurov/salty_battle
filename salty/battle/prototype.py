from datetime import datetime
from time import sleep, time
from typing import NamedTuple
import pandas as pd

import numpy as np
import pylab
from ably import AblyRest
import matplotlib.pyplot as plt

API_KEY = 'iu0Lmw.hC3rhw:MEeGgoGc7kI4xQa1'

def read_messages(message_history):
    timestamp = None
    if message_history.items:
        timestamp = message_history.items[0].timestamp
        for m in message_history.items:
            print(m.as_dict())
    return timestamp

class StatsContext:
    def __init__(self):
        self.filtered_y = np.array([])
        self.window = 10
        self.threshold = 2
        self.influence = 0.5
        self.current_y = None

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
            else:
                return 0

    @property
    def rolling_mean(self):
        return np.mean(self.filtered_y[-self.window - 1:-1])

    @property
    def rolling_stdev(self):
        return np.std(self.filtered_y[-self.window - 1:-1])


def listen_and_read():
    client = AblyRest(API_KEY)
    channel = client.channels.get('salty-voting')

    print('Listening...')

    timestamp_start = int(time())

    while True:
        message_history = channel.history(start=timestamp_start)
        if len(message_history.items) > 0:
            res = read_messages(message_history)
            print(res)
            timestamp_start = message_history.items[0].timestamp + 1
        sleep(1)


def listen():
    client = AblyRest(API_KEY)
    channel = client.channels.get('salty-voting')

    print('Listening...')

    timestamp_start = int(time())
    stats_context = StatsContext()
    while True:
        message_history = channel.history(start=timestamp_start)
        # res = read_messages(message_history)
        if len(message_history.items) > 0:
            # print(res)
            timestamp_start = message_history.items[0].timestamp + 1

        stats_context.add_observation(len(message_history.items))
        # print(len(message_history.items))
        # print(stats_context.observations)
        if len(stats_context.filtered_y) > 11:
            # print(stats_context.mean, stats_context.rolling_mean, stats_context.rolling_stdev)
            print(stats_context.z_score, stats_context.rolling_mean, stats_context.rolling_stdev)
        sleep(1)


def replay_spike_detection(inputs, window):
    stc = StatsContext()
    stc.window = window
    results = []
    z_scores = []
    means = []
    stdevs = []
    abs_thresh = []
    for val in inputs.values:
        stc.add_observation(val)
        z_scores.append(stc.z_score)
        # print(val, stc.z_score)

        if stc.rolling_mean > 1 and stc.rolling_stdev > 1:
            abs_thresh = stc.rolling_mean + stc.rolling_stdev * stc.threshold
        else:
            abs_thresh = 1 + 1 * stc.threshold

        results.append({
            'INPUT': val,
            'Z_SCORE': stc.z_score,
            'ROLLMEAN': stc.rolling_mean,
            'ROLLSTD': stc.rolling_stdev,
            'ABSTHRESH': abs_thresh
        })
    results = pd.DataFrame(results)
    results['FILTERED'] = stc.filtered_y
    # print(results)
    # return pd.Series(z_scores)
    return results


def record_votes_kb():
    from pynput import keyboard
    import random
    res_list = []

    res_list.append({'ts': datetime.now().timestamp(), 'vote': 's'})
    user_ids = [random.randint(0, 100), random.randint(0, 100),]
    keys_mapping = {
        'q': user_ids[0],
        'w': user_ids[0],
        '[': user_ids[1],
        ']': user_ids[1],

    }

    def on_press(key):
        # print('"%s"' % key.char)
        ts = datetime.now().timestamp()
        if key.char in '[q':
            res_list.append({'ts': ts, 'vote': 'L', 'id': keys_mapping[key.char]})
        elif key.char in ']w':
            res_list.append({'ts': ts, 'vote': 'R', 'id': keys_mapping[key.char]})
        elif key.char == 's':
            return False

    print('Listening')
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    df = pd.DataFrame(res_list)
    # print(df)
    with open('c:/temp/voting_data.csv', 'a') as f:
        df.to_csv(f)

    df['ts_sec'] = df.ts.astype('int')
    stats_df = df.groupby(['ts_sec','vote']).vote.count().unstack()
    print(stats_df)


def replay():
    voting_df = pd.read_csv('c:/temp/camp_hollywood_2017_voting_data.csv')
    voting_df['ts_int'] = voting_df.ts.astype('int')

    def print_scores(battle, ts, left, right):
        print('\rBATTLE %s (%s):\t%s\t%s' % (battle, ts, left, right), end='', flush=True)

    for b_id in range(1,6):
        df = voting_df[voting_df.battle == b_id]
        df_aggr = df.groupby(['ts_int', 'vote']).vote.count().unstack()
        df_aggr = df_aggr.reindex(pd.Index(range(df_aggr.index[0], df_aggr.index[-1] + 1))).fillna(0)


        # print(df_aggr)

        print_scores(b_id, 0, 0, 0)
        res_l = replay_spike_detection(df_aggr.L, window=5)
        res_r = replay_spike_detection(df_aggr.R, window=5)

        res_df = pd.concat([
            res_l.ABSTHRESH, res_l.ROLLMEAN, res_l.INPUT,
            -res_r.ABSTHRESH, -res_r.ROLLMEAN, -res_r.INPUT], axis=1)
        res_df.index = df_aggr.index
        res_df.columns = [
            'Threshold L', 'Mean L', 'Freq L',
            'Threshold R', 'Mean R', 'Freq R',
        ]
        res_df = res_df.fillna(0)
        res_df.index = pd.datetime(2018, 1, 1, 0, 1, 30) + pd.to_timedelta(res_df.index, unit='s')

        ax1 = plt.subplot(211)

        res_df[['Threshold L', 'Threshold R']].plot.area(ax=ax1, color='xkcd:silver', legend=False)
        res_df[['Mean L', 'Mean R']].plot.area(ax=ax1, color='xkcd:grey', legend=False)
        res_df[['Freq L', 'Freq R']].plot.line(ax=ax1, title=f'Battle {b_id}')

        # pylab.savefig(f'c:/temp/battle_{b_id}.png')
        # pylab.show()
        # print(res_l)

        score_l = 0
        score_r = 0
        res_df['Score L'] = 0
        res_df['Score R'] = 0
        res_df['Bonus L'] = None
        res_df['Bonus R'] = None
        for ix, i in enumerate(res_l.index.values):
            score_l += res_l['INPUT'][i]
            score_r += res_r['INPUT'][i]

            if res_l.loc[i, 'INPUT'] > res_l.loc[i, 'ABSTHRESH']:
                score_l += 50
                res_df['Bonus L'].iloc[ix] = score_r

            if res_r.loc[i, 'INPUT'] > res_r.loc[i, 'ABSTHRESH']:
                score_r += 50
                res_df['Bonus R'].iloc[ix] = score_r

            res_df['Score L'].iloc[ix] = score_l
            res_df['Score R'].iloc[ix] = score_r

        ax2 = plt.subplot(212, sharex=ax1)
        res_df[['Score L', 'Score R']].plot.line(ax=ax2)
        # res_df[['Bonus L', 'Bonus R']].plot.scatter(x='',ax=ax2, legend=False, color='black')

        # import pdb;pdb.set_trace()
        pylab.savefig(f'c:/temp/battle_{b_id}.png')
        pylab.close()
        #
        #     print_scores(b_id, i, score_l, score_r)
        #     sleep(1)
        # print('')



# algo_resul[[[[t = NamedTuple('AlgoResult',[''])


# def thresholding_algo(y, lag, threshold, influence):
#     signals = np.zeros(len(y))
#     filteredY = np.array(y)
#     avgFilter = [0]*len(y)
#     stdFilter = [0]*len(y)
#     avgFilter[lag - 1] = np.mean(y[0:lag])
#     stdFilter[lag - 1] = np.std(y[0:lag])
#     for i in range(lag, len(y)):
#         if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
#             if y[i] > avgFilter[i-1]:
#                 signals[i] = 1
#             else:
#                 signals[i] = -1
#
#             filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
#         else:
#             signals[i] = 0
#             filteredY[i] = y[i]
#         avgFilter[i] = np.mean(filteredY[(i-lag):i])
#         stdFilter[i] = np.std(filteredY[(i-lag):i])
#
#     return dict(signals = np.asarray(signals),
#                 avgFilter = np.asarray(avgFilter),
#                 stdFilter = np.asarray(stdFilter))


# listen()
# listen_and_read()

if __name__ == '__main__':
    # record_votes_kb()
    replay()