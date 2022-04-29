import aiohttp.web
import aiobungie
import os
import ssl
import urllib.parse
import asyncio
import motor.motor_asyncio
import asyncio

'''
Credit to nxtlo for the example on oauth2 with aiohttp and aiobungie:
https://github.com/nxtlo/aiobungie/blob/399ebd63448ee68256dea639e8a12ce69462f571/examples/user_oauth2.py#L44
'''
# Web router
router = aiohttp.web.RouteTableDef()


def parse_url(url: str) -> str:
    """Parse the url to get authorization code"""
    parser = urllib.parse.urlparse(url)
    return parser.query.removeprefix('code=')


def parse_discord(url: str) -> str:  # TODO: Need to correctly parse the url for the discord username
    """Parse the url for discord username"""
    parser = urllib.parse.urlparse(url)
    username = url.rsplit('_', 1)[-1]
    return username


client = aiobungie.RESTPool(os.environ.get("api_key"), client_secret=os.environ.get('client_secret'),
                            client_id=int(os.environ['client_id']))

# mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_CONNECTION_URL"))
# connection_status = mongo_client.test  # Cluster
# db = mongo_client['Little-Light']  # database
# collection = db['Users']  # database table
# num = await collection.count_documents({})
# print(db)
# print(num)
#
# exit()


def combinational_logic_get_oauth2_url(user):
    url = client.acquire().build_oauth2_url()
    url = url + '_' + user  # Hack n' a half: Discord username is appended to the state for the oauth and redirect urls
    print(url)
    return url


async def get_oauth2_url():
    async with client.acquire() as rest:
        oauth_url = rest.build_oauth2_url()
        print(oauth_url)


@router.get("/redirect")
async def redirect(request: aiohttp.web.Request) -> aiohttp.web.Response:
    print(str(request.url))
    discord_name = parse_discord(str(request.url))
    print(discord_name)
    if code := parse_url(str(request.url)):
        code = str(code)
        tokens = ""
        async with client.acquire() as rest:
            tokens = await rest.fetch_oauth2_tokens(code)
            print(tokens)
            text_file = open("placeholder.txt", "wt")
            n = text_file.write(tokens.access_token)
            text_file.close()
            request.app["token"] = tokens.access_token

        async with client.acquire() as rest:
            my_user = await rest.fetch_current_user_memberships(tokens.access_token)
            print(my_user.get("bungieNetUser").get("uniqueName"))

            # TODO: Store data in db (needs to be done before user starts making calls from bot.py
            raise aiohttp.web.HTTPFound(location='/me', reason="Oauth2 Success!")

    else:
        # Otherwise return 404 and couldn't authenticate.
        raise aiohttp.web.HTTPNotFound(text="Code not found and couldn't authenticate.")


@router.get('/me')
async def me(request: aiohttp.web.Request) -> aiohttp.web.Response:
    if access_token := request.app.get("token"):

        async with client.acquire() as rest:
            my_user = await rest.fetch_current_user_memberships(access_token)
            # print(my_user.get("bungieNetUser").get("uniqueName"))
            return aiohttp.web.json_response(my_user)
    else:
        raise aiohttp.web.HTTPUnauthorized(text="No access token found, Unauthorized.")


def start_server():  # TODO: Need to automatically close the server connection (maybe once the tokens are received?)
    # asyncio.new_event_loop().run_until_complete(get_oauth2_url())
    # url = combinational_logic_get_oauth2_url()
    app = aiohttp.web.Application()
    app.add_routes(router)

    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # TODO: Won't need for production (use https server instead of localhost)
    ctx.load_cert_chain(certfile="../pkeys/cacert.pem", keyfile="../pkeys/little_light_pkey")

    # TODO: Run on cloud localhost
    aiohttp.web.run_app(app, host="localhost", port=8000, ssl_context=ctx)


if __name__ == '__main__':
    start_server()

# TODO: As a test write a bot function that will give a user's join code
