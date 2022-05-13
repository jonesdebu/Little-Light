import os
from pymongo import MongoClient
import pprint


def db_get_auth(discord_name):
    mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_URL"))
    # connection_status = mongo_client.test  # Cluster
    db = mongo_client['Little-Light']  # database
    collection = mongo_client['Little-Light']['Users']  # database table
    one_document = db['Users'].find_one({
        'discordName': discord_name
    })
    mongo_client.close()
    if one_document:
        return one_document.get("bungieNetUser")
    return False


def db_upload_user(discord_name, bungie_net_user, access_token, refresh_token):
    mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_URL"))
    connection_status = mongo_client.test
    print(connection_status)
    db = mongo_client['Little-Light']
    collection = db['Users']
    # Build the document
    doc = {
        "discordName": discord_name,
        "bungieNetUser": bungie_net_user,
        "accessToken": access_token,
        "refresh_token": refresh_token
    }
    collection.insert_one(doc)
    mongo_client.close()
