from pymongo import MongoClient

# Connect to MongoDB as root user
client = MongoClient("mongodb://admin:password@localhost:27017/")

# Access admin database
db = client.admin

# Set up new user with password for example1 database
db.command(
    "createUser",
    "dd_python_codebase",
    pwd="upload_me",
    roles=[{"role": "readWrite", "db": "dwdrun"}],
)

db.command(
    "createUser",
    "dd_python_codebase_down",
    pwd="download_me",
    roles=[{"role": "read", "db": "dwdrun"}],
)


print(
    "User 'example1_user' created with password 'example1_password' for database 'example1'"
)
