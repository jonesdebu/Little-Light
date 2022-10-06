import aiohttp.web
import aiobungie
import os
import ssl
import urllib.parse
from db import db_upload_user
from aiobungie.internal import enums

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


def parse_discord(url: str) -> str:
    """Parse the url for discord username"""
    parser = urllib.parse.urlparse(url)
    username = url.rsplit('_', 1)[-1]
    return username


client = aiobungie.RESTPool(os.environ.get("api_key"), client_secret=os.environ.get('client_secret'),
                            client_id=int(os.environ['client_id']))


def combinational_logic_get_oauth2_url(user):
    url = client.acquire().build_oauth2_url()
    url = url + '_' + user  # Hack n' a half: Discord username is appended to the state for the oauth and redirect urls
    print(url)
    return url


async def get_oauth2_url():
    async with client.acquire() as rest:
        oauth_url = rest.build_oauth2_url()
        print(oauth_url)


@router.get("/redirect")  # Bungie portal redirect url: AWS url/redirect mot likely
async def redirect(request: aiohttp.web.Request) -> aiohttp.web.Response:
    discord_name = parse_discord(str(request.url))
    if code := parse_url(str(request.url)):
        code = str(code)
        tokens = ""
        async with client.acquire() as rest:  # tokens is an OAuth2Response from aiobungie builders.py line 61
            tokens = await rest.fetch_oauth2_tokens(code)
            request.app["token"] = tokens.access_token

        async with client.acquire() as rest:
            my_user = await rest.fetch_current_user_memberships(tokens.access_token)
            bungieNetUser = my_user.get("bungieNetUser").get("uniqueName")
            membershipType = my_user.get("destinyMemberships")[0].get("membershipType")
            membershipId = my_user.get("destinyMemberships")[0].get("membershipId")

        async with client.acquire() as rest:
            my_profile = await rest.fetch_profile(membershipId, membershipType, [enums.ComponentType["CHARACTERS"]])
            characters = []
            # TODO: Maybe store the characters all in their own db table and link using memebrship type, id,
            #  and bungieNetUser
            for character in my_profile.get("characters").get("data"):
                char_id = my_profile.get("characters").get("data").get(character).get("characterId")
                characters.append(char_id)
            db_upload_user(discord_name, bungieNetUser, tokens.access_token, tokens.refresh_token, membershipType,
                           membershipId, characters)
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

    # TODO: Run on cloud localhost (exposed as url) (AWS)
    aiohttp.web.run_app(app, host="localhost", port=8000, ssl_context=ctx)


if __name__ == '__main__':
    start_server()
