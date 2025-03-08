


async def csrf_token(session):
  url = "https://userapi.adda247.com/csrf/token?src=aweb"
  response = await session.get(url)
  data = await resonse.json()
  if data["success"]:
    return data["data"]
  else:
    return None

