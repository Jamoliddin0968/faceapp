from decouple import config

DB_NAME = config("DB_NAME", "test")
DB_HOST = config("DB_HOST", "localhost")
DB_PORT = config("DB_PORT", 3306)
DB_PASSWORD = config("DB_PASSWORD", "11111111")
DB_USER = config("DB_USER", "root")
IMAGE_DIR = config("IMAGE_DIR", "images")

DATABASE_URL = f"mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
