
def add_ws_apps(original_app, schema=None):
  async def chat_app(scope, receive, send):
    if scope["type"] == "websocket":
      print(scope)

    else:
      await original_app(scope, receive, send)

  return chat_app
