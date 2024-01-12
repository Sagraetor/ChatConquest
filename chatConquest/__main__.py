import asyncio

from TikTokLive import TikTokLiveClient

from common.constant import TIK_TOK_ID as ID
from tiktok.event_handler import on_comment, on_connect
from game.display import display

if __name__ == '__main__':
    with asyncio.Runner() as runner:
        loop = runner.get_loop()
        #client: TikTokLiveClient = TikTokLiveClient(unique_id=ID, loop=loop)
        #client.add_listener('comment', on_comment)
        #client.add_listener('connect', on_connect)
        #loop.create_task(client.start())
        #loop.run_until_complete(display.start())
        loop.create_task(display.start())
        loop.run_forever()