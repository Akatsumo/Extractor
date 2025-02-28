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
    return False, None


async def verify_otp(session, otp_num, org_id, phone, sessionID):
  url = "https://api.classplusapp.com/v2/users/verify"
  data = {
    "otp": otp_num,
    "countryExt": "91",
    "sessionId": sessionID,
    "orgId": org_id,
    "fingerprintId": "",
    "mobile": phone
  }
  response = await session.post(url, json=data)
  output = await response.json()
  if "success" == output["status"]:
     return True, output["token"]
  else:
    return False, None
    




