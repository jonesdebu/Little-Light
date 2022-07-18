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


def db_find_discord(discord_name):
    mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_URL"))


def db_upload_user(discord_name: str, bungie_net_user: str, access_token: str, refresh_token: str, membership_type: int,
                   membership_id: str, characters):
    '''
    Uploads User and User's Characters to the db

    :param discord_name: User's discord name
    :param bungie_net_user: User's Bungie name
    :param access_token: Oauth Access Token
    :param refresh_token: Oauth Refresh Token
    :param membership_type: Platform that user and characters belong to
    :param membership_id: User ID for that platform
    :param characters: User's character IDs
    :return: None
    '''

    mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_URL"))
    connection_status = mongo_client.test
    print(connection_status)
    db = mongo_client['Little-Light']
    user_collection = db['Users']
    characters_collection = db['Characters']
    # Build the document

    user_doc = {
        "discordName": discord_name,
        "bungieNetUser": bungie_net_user,
        "accessToken": access_token,
        "refresh_token": refresh_token,
        "membershipType": membership_type,
        "membershipId": membership_id,
    }
    user_collection.insert_one(user_doc)

    for character in characters:
        char_doc = {
            "discord_name": discord_name,
            "bungieNetUser": bungie_net_user,
            "characterId": character,
            "membershipId": membership_id,
            "membershipType": membership_type
        }

        characters_collection.insert_one(char_doc)

    mongo_client.close()
