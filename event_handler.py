import team

from TikTokLive.types.events import CommentEvent, ConnectEvent
from player import players


async def on_connect(_: ConnectEvent):
    pass


async def on_comment(event: CommentEvent):
    player = None
    while player is None:
        player = players(event.user.nickname)

    if player.team is None:
        acceptable_answers = ['1', '2', '3']
        for letter in event.comment.lower():
            if letter in acceptable_answers:
                player.team = team.TEAMS[int(letter) - 1]
                break

    elif player.character is None:
        acceptable_answers = ['a', 'b', 'c']
        for letter in event.comment.lower():
            if letter in acceptable_answers:
                player.new_character(letter)
                break

    else:
        acceptable_answers = [str(x) for x in range(19, 1, -1)]
        for letter in acceptable_answers:
            if letter in event.comment.lower():
                player.character.move(int(letter))
                break
