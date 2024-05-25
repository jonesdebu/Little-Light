import aiobungie
from aiobungie.internal import enums
from db import *
import asyncio
import json
import pprint

aiobungie_client = aiobungie.Client(os.environ.get("api_key"))


async def get_characters(membership_id, membership_type, components_list):
    my_profile = await aiobungie_client.fetch_profile(membership_id, membership_type, components_list)
    characters = {}
    for character in my_profile.characters.values():
        characters[str(character.class_type)] = {
            'light': str(character.light),
            'gender': str(character.gender),
            'race': str(character.race),
            'emblem': str(character.emblem),
            'emblem_icon': str(character.emblem_icon),
            'total_played_time': str(character.total_played_time),
            'level': str(character.level)
        }
    pprint.pprint(characters)
    return characters


async def get_characters_stats(membership_id, membership_type, components_list):
    my_profile = await aiobungie_client.fetch_profile(membership_id, membership_type, components_list)
    characters = {}
    for character in my_profile.characters.values():
        stats = {}
        for stat, value in character.stats.items():
            stats[str(stat)] = str(value)
        characters[str(character.class_type)] = stats
    pprint.pprint(characters)
    return characters


async def get_manifest():
    print('downloading file')
    json_manifest = await aiobungie_client.rest.download_json_manifest()
    print('reading file')
    with open("manifest.json", "r") as f:
        manifest_json = json.loads(f.read())
        pprint.pprint(manifest_json['DestinyLoreDefinition'].values())


async def get_random_lore():
    try:
        with open("manifest.json", "r") as f:
            manifest_json = json.loads(f.read())
            manifest_lore_keys = list(manifest_json['DestinyLoreDefinition'].keys())
            pprint.pprint(manifest_lore_keys[0])
            print(manifest_json['DestinyLoreDefinition'][manifest_lore_keys[0]]['displayProperties']['description'])
    except OSError as e:
        print("Manifest not found downloading now.....")
        json_manifest = await aiobungie_client.rest.download_json_manifest()
        await get_random_lore()


async def main():
    await get_random_lore()
    # mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_URL"))
    # connection_status = mongo_client.test
    # db = mongo_client['Little-Light']
    # user_collection = db['Users']
    # characters_collection = db['Characters']
    # test_char = characters_collection.find_one({"characterId": "2305843009388816162"})
    # test_user = user_collection.find_one(({"discordName": "Stoicalneo"}))
    # chars = await get_characters_stats(test_user['membershipId'], test_user['membershipType'],
    #                                    [aiobungie.ComponentType.CHARACTERS])
    # mongo_client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
