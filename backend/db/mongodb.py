import motor.motor_asyncio
import certifi
from core.config import get_settings

settings = get_settings()

class MongoDB:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_to_storage(cls):
        # The Port error usually happens when special characters in password aren't handled.
        # Motor/PyMongo handles the URI string directly.
        uri = settings.MONGODB_URI
        cls.client = motor.motor_asyncio.AsyncIOMotorClient(
            uri, 
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=True
        )
        cls.db = cls.client.get_database("mindmate")
        print(f"Connected to MongoDB Atlas cluster.")

    @classmethod
    async def close_storage_connection(cls):
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed")

async def get_database():
    return MongoDB.db
