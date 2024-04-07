import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# Replace 'your_username' and 'your_password' with your actual username and password
username = "dd_python_codebase"
password = "upload_me"
# Construct MongoDB connection string with username and password
uri = "mongodb://%s:%s@localhost:27017/dwdrun?authSource=admin&retryWrites=true&w=majority" % (
    quote_plus(username),
    quote_plus(password),
)

# Connect to MongoDB
client = MongoClient(uri)
db = client["dwdrun"]  # Replace 'your_database' with your actual database name
collection = db["codebase"]  # Replace 'your_collection' with your actual collection name


def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    # Upsert content into MongoDB
                    relative_file_path = os.path.relpath(file_path, directory)
                    upsert_document(relative_file_path, content)


def upsert_document(relative_file_path, content):
    # Construct record name by replacing forward slashes with periods and removing '.py' extension if it exists
    record_name = relative_file_path.replace("/", ".")

    if record_name.endswith("__init__.py"):
        record_name = record_name[:-12]  # Remove '.py' from the end

    if record_name.endswith(".py"):
        record_name = record_name[:-3]  # Remove '.py' from the end

    # Upsert content into MongoDB collection
    collection.update_one({"_id": record_name}, {"$set": {"content": content}}, upsert=True)
    print("Upserted document into MongoDB")


def clear_collection():
    # Clear the collection
    collection.delete_many({})
    print("Collection cleared")


if __name__ == "__main__":
    directory_path = "/Users/daviddawson/Library/Mobile Documents/com~apple~CloudDocs/Documents/projects/airflow/python_codebase"  # Replace with the path to your directory
    traverse_directory(directory_path)
    # Uncomment the line below to clear the collection (use with caution)
    # clear_collection()
