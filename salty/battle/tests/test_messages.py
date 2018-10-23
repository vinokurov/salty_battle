from salty.battle.messages import ScoreUpdateMessage, ScoreUpdateOne


def test_ScoreUpdateMessage():
    message = ScoreUpdateMessage(
        left=ScoreUpdateOne(
            increment=5,
            total=100,
        ),
        right=ScoreUpdateOne(
            increment=5,
            total=100,
            is_bonus=True,
            bonus_message='x2'
        ),
    )
    json_str = '{"left": {"total": 100, "increment": 5, "is_bonus": false, "bonus_message": ""}, ' \
               '"right": {"total": 100, "increment": 5, "is_bonus": true, "bonus_message": "x2"}}'

    assert message.to_json() == json_str
    assert message == ScoreUpdateMessage.from_json(json_str)
