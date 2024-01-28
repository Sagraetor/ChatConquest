import asyncio

from TikTokLive import TikTokLiveClient

from common.constant import TIK_TOK_ID as ID
from tiktok.event_handler import on_comment, on_connect, on_disconnect
from game.display import display


if __name__ == '__main__':
    with asyncio.Runner() as runner:
        loop = runner.get_loop()

        def init(ID):
            client: TikTokLiveClient = TikTokLiveClient(unique_id=ID, loop=loop)
            client.add_listener('comment', on_comment)
            client.add_listener('connect', on_connect)
            client.add_listener('disconnect', on_disconnect)
            loop.create_task(client.start())
            return ID

        display.set_tiktok_initialiser(init)
        loop.run_until_complete(display.start())