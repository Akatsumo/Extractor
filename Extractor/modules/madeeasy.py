import os 
import asyncio
import requests
from Extractor import app
from pyrogram import filters 


headers = {
    "device-type": "4",
    "organization": "9a523aa7-dc66-410a-98bb-8cd66e875f35",
   "version-code": "21",
}


async def otp_login(session, id_login):
  idLogin = "email" if "@" in id_login else "phone"
  data = {
    "organization": "madeeasyprime",
    "authType": "LOGIN",
    idLogin: id_login,
  }    
  response = session.post(url, headers=headers, json=data)
  return response.json()["success"]


async def verify_otp(session, id_login, otp_number):
  idLogin = "email" if "@" in id_login else "phone"
  data = {
    "organization": "9a523aa7-dc66-410a-98bb-8cd66e875f35",
    idLogin : id_login,
    "otp": otp_number,
  }
  response = session.post(url, headers=headers, json=data)
  return response.json()["success"]


  
