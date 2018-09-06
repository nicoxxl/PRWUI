from aiohttp import web
import aiohttp
import asyncio
import json
from .page import PageManager
import time



class App:
    def render(self):
        return ''

    def handle(self, data):
        pass


async def handler_loop(send, event_q, app, ws):
    while True:
        event = await event_q.get()
        t0 = time.perf_counter_ns()
        if event is None:
            print('"event is None": left')
            break
        app.handle(event)
        print('event', event)
        if event_q.empty():
            # print('yo')
            await send(json.dumps(app.render()), compress=None)
            await ws.drain()
            t1 = time.perf_counter_ns()
            print('Delta:', (t1-t0)/1e6, (t1-event['_t_ev'])/1e6)

class Runner:
    def __init__(self, app_factory, page_manager=None):
        self.app_factory = app_factory
        self.page_manager = PageManager() if page_manager is None else page_manager
        self.app = web.Application()
        self.app.add_routes([
            web.get('/', self.index_handler),
            web.get('/ws', self.websocket_handler),
        ])
    
    async def index_handler(self, request):
        return web.Response(text=self.page_manager(), content_type='text/html')
    
    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        if ws is None:
            print(request)
            return web.Response(text='WTF?')
        await ws.prepare(request)
        app = self.app_factory()
        event_q = asyncio.queues.Queue()
        asyncio.create_task(handler_loop(ws.send_str, event_q, app, ws))

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                t_ev = time.perf_counter_ns()
                try:
                    data = json.loads(msg.data)
                except json.decoder.JSONDecodeError:
                    print("json.decoder.JSONDecodeError: event is None")
                    await event_q.put(None)
                    print(msg.data)
                    raise
                else:
                    data['_src'] = 'websocket'
                    data['_t_ev'] = t_ev
                    await event_q.put(data)
            if msg.type == aiohttp.WSMsgType.CLOSE:
                await envent_q.put(None)
    
    def run(self):
        web.run_app(self.app)
    
    def add_heading(self, heading):
        self.page_manager.add_heading(heading)