from TikTokLive.types.events import CommentEvent, ConnectEvent, DisconnectEvent
from chatConquest.common import team
from chatConquest.game.game_space import game_data
from chatConquest.tiktok.player import players


async def on_connect(_: ConnectEvent):
    game_data.connected = True


async def on_disconnect(event: DisconnectEvent):
    game_data.connected = False


async def on_comment(event: CommentEvent):
    player = None
    while player is None:
        player = players(event.user.nickname, await event.user.avatar.download())

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
