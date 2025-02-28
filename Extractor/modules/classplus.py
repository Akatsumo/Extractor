import os
import aiohttp



async def otp_login(session, org_code, org_id, phone):
  url = "https://api.classplusapp.com/v2/otp/generate"
  data = {
    "countryExt": "91",
    "orgCode": org_code,
    "viaSms": "1",
    "viaEmail": "0",
    "retry": 0,
    "orgId": org_id,
    "otpCount": 0,
    "mobile": phone
  }
  response = await session.post(url, json=data)
  output = await response.json()
  if "success" == output["status"]:
     sessionId = output["data"]["sessionId"]
     return True, sessionID
  else:
    retrun False, None





