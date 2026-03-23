from os import getenv


API_ID = int(getenv("API_ID", "26850449"))
API_HASH = getenv("API_HASH", "72a730c380e68095a8549ad7341b0608")
BOT_TOKEN = getenv("BOT_TOKEN", "8780107200:AAFwiRdXWdrToMS09Swa7qXD72jPd1HpxAE")
OWNER_ID = list(map(int, getenv("OWNER_ID", "8462359928 7980470023 6414073613").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://Extractor:ohUUMrBcLaCxlWZv@cluster0.nsjqx8b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

CHANNEL_ID = int(getenv("CHANNEL_ID", "-1003768543718"))
LOGS_CHANNEL = int(getenv("LOGS_CHANNEL", "-1003732727468"))


