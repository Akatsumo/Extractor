from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN","8373696951:AAG7XYrjGP5ydGlfRdOge1H45aW4Z4D4e-I")
OWNER_ID = list(map(int, getenv("OWNER_ID", "8462359928").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://Extractor:ohUUMrBcLaCxlWZv@cluster0.nsjqx8b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002405071668"))
PREMIUM_LOGS = int(getenv("PREMIUM_LOGS", "-1002091053529"))


