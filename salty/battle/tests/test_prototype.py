import pandas as pd
from io import StringIO

import pytest
from pandas.util.testing import assert_series_equal

from salty.battle.prototype import replay_spike_detection


def text_to_df(df_str):
    return pd.read_table(StringIO(df_str),
                         index_col=0,
                         header=0,
                         delim_whitespace=True,
                         parse_dates=True,
                         )

def test_():
    df = text_to_df("""
                 A   B
    2018-05-01   1   2
    2018-05-02   1   20
    """)
    print(df)
    print(df.index)


def test_spike_detect():
    data = text_to_df("""
       INPUT  SPIKES  FILTERED
    0  2      0       2
    1  1      0       1
    2  3      0       3       
    3  3      0       3
    4  10     1       6.5
    5  3      0       3
    """)
    spikes = replay_spike_detection(data.INPUT, window=3) > 2
    spikes = spikes.apply(lambda x: int(x))
    assert_series_equal(data.SPIKES.reset_index(drop=True),
                        spikes, check_names=False)


def test_spike_detect_2():
    data = text_to_df("""
       INPUT  SPIKES  FILTERED
    0  2      0       2
    1  1      0       1
    2  3      0       3       
    3  3      0       3
    4  10     1       6.5
    5  10     1       3
    5  7      0       3
    5  3      0       3
    5  3      0       3
    5  3      0       3
    """)
    spikes = replay_spike_detection(data.INPUT, window=3) > 2
    spikes = spikes.apply(lambda x: int(x))
    assert_series_equal(data.SPIKES.reset_index(drop=True),
                        spikes, check_names=False)

@pytest.mark.skip
def process_data_camp_hollywood():
    battles = pd.read_csv('c:/temp/camp_hollywood_2017.csv')
    voting_raw = pd.read_csv('c:/temp/camp_hollywood_2017_voting.csv')
    battles_rel_ts = battles.ts - battles.ts.iloc[0]
    # voting_raw['rel_ts'] = None
    voting_raw['ts_rel'] = voting_raw[voting_raw.vote == 's'].ts
    voting_raw.ts_rel = voting_raw.ts_rel.ffill()
    voting_raw.ts -= voting_raw.ts_rel
    voting_data = voting_raw[voting_raw.vote != 's'][['ts', 'vote', 'id']]
    voting_data.sort_values('ts', inplace=True)
    voting_data['battle'] = ''
    for ix, b_ts in battles_rel_ts.iteritems():
        voting_data.loc[voting_data.ts >= b_ts, 'battle'] = ix +1

    voting_data.to_csv('c:/temp/camp_hollywood_2017_voting_data.csv', index=False)
    # print voting_data


def test_camp_hollywood():
    voting_df = pd.read_csv('c:/temp/camp_hollywood_2017_voting_data.csv')
    voting_df['ts_int'] = voting_df.ts.astype('int')
    for b_id in range(1,6):
        df = voting_df[voting_df.battle == b_id]
        df_aggr = df.groupby(['ts_int', 'vote']).vote.count().unstack()
        df_aggr = df_aggr.reindex(pd.Index(range(df_aggr.index[-1] + 1))).fillna(0)

        print('BATTLE %s' % b_id)
        res_l = replay_spike_detection(df_aggr.L, window=10)
        res_r = replay_spike_detection(df_aggr.R, window=10)
        # print(replay_spike_detection(df_aggr.R, window=10))
        score_l = res_l.INPUT.sum() + res_l[res_l.Z_SCORE > 2].Z_SCORE.count() * 20
        score_r = res_r.INPUT.sum() + res_r[res_r.Z_SCORE > 2].Z_SCORE.count() * 20

        print(score_l, score_r)
        print(res_l.INPUT.sum(), res_r.INPUT.sum())
        print(res_l[res_l.Z_SCORE > 2])
        print(res_r[res_r.Z_SCORE > 2])
