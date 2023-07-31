import asyncio
import json
import re
import traceback

from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.urls.resolvers import _route_to_regex

from loguru import logger

class WebSocketRequest(ASGIRequest):
  def __init__(self, scope, body_file):
    scope['method'] = 'GET'
    super().__init__(scope, body_file)


class JsonWebSocket:
  connect_tasks = []

  def __init__(self, scope, receive, send):
    self.closed = False
    self.connected = False
    self.scope = scope
    self.receive = receive
    self.send = send
    self.tasks = set()
    self.request = WebSocketRequest(scope, None)

  async def init_socket(self):
    pass

  async def on_connect(self):
    logger.info('Websocket Opened')
    await self.send({'type': 'websocket.accept'})
    self.connected = True
    await self.start_tasks()

  async def on_disconnected(self):
    logger.info("Disconnect from client")
    self.closed = True

  async def on_closed(self):
    logger.info("Websocket closed")

  async def process_event(self, event):
    data = await self.load_message(event['text'])
    logger.info('Received:', data)

  async def load_message(self, msg):
    return json.loads(msg)

  async def run_task(self, task):
    try:
      return await getattr(self, task)()

    except:
      traceback.print_exc()
      raise

  async def start_tasks(self):
    for t in self.connect_tasks:
      task = asyncio.create_task(self.run_task(t))
      self.tasks.add(task)
      task.add_done_callback(self.tasks.discard)

  async def send_message(self, data):
    print(data, type(data))
    if type(data) == bytes:
      message = data.decode()

    elif type(data) != str:
      message = json.dumps(data)

    else:
      message = data

    await self.send({'type': 'websocket.send', 'text': message})

  async def run (self):
    while 1:
      event = await self.receive()

      if event['type'] == 'websocket.connect':
        await self.on_connect()

      elif event['type'] == 'websocket.disconnect':
        await self.on_disconnected()

      elif event['type'] == 'websocket.receive':
        await self.process_event(event)

      if self.closed:
        break

    while 1:
      if self.tasks:
        # wait for tasks to finish
        await asyncio.sleep(0.1)

      else:
        break

    await self.on_closed()


class RoomSocket(JsonWebSocket):
  connect_tasks = ['room_listener']

  async def init_socket(self, org_id, room_id):
    self.org_id = org_id
    self.room_id = room_id

  async def room_listener(self):
    async with settings.REDIS_ASYNC_CLIENT.pubsub() as pubsub:
      await pubsub.subscribe(f"room_{self.room_id}")

      while 1:
        if self.closed:
          break

        msg = await pubsub.get_message(ignore_subscribe_messages=True)
        if msg is not None:
          await self.send_message(msg['data'])


routes = (
  {"route": "ws-v1/org/<int:org_id>/room/<int:room_id>/", "class": RoomSocket},
)

for route in routes:
  regex, converters = _route_to_regex("/" + route["route"])
  route["regex"] = regex
  route["converters"] = converters


def route_matches(route, path):
  matched = re.search(route["regex"], path)
  if matched:
    args = []
    for key, value in matched.groupdict().items():
      args.append(route["converters"][key].to_python(value))

    if args:
      return args

    return True

  return False


def add_ws_apps(original_app, schema=None):
  async def chat_app(scope, receive, send):
    if scope["type"] == "websocket":
      for route in routes:
        matched = route_matches(route, scope["path"])
        if matched:
          ws = route['class'](scope, receive, send)

          try:
            if route['converters']:
              await ws.init_socket(*matched)

            else:
              await ws.init_socket()

            await ws.run()

          except:
            traceback.print_exc()

          finally:
            return

      logger.info("Closing Connection")
      await send({'type': 'websocket.close', 'code': 1011, 'reason': '404 - Route not found'})

    else:
      await original_app(scope, receive, send)

  return chat_app
