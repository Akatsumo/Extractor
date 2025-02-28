import os
import aiohttp



async def classplus_org_id(org_id, session):
    async with session.get(f"https://{org_id}.courses.store") as response:
        html_content = await response.text()
        org_id_match = re.search(r'"orgId":(\d+)', html_content)
        name_match = re.search(r'"name":"([^"]+)"', html_content)
        org_id = org_id_match.group(1) if org_id_match else None
        name = name_match.group(1) if name_match else None
    return org_id, name


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
    
    if output.get("status") == "success":  
        sessionId = output["data"]["sessionId"]
        return True, sessionId  
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

    if output.get("status") == "success":  
        return True, output.get("token")  
    else:
        return False, None










    




