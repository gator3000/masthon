from .__init__ import Client, __version__ as version, DEFAULT_MESSAGE

# from masthon import Client, __version__ as version, DEFAULT_MESSAGE
from time import asctime
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-v":
            print("Made with <3 by   @gator3000@mastodon.social")
            print("Issues          : https://gitlab.com/Gator3000/masthon/-/issues")
            print("Documentation   : https://gator3000.gitlab.io/masthon/")
            print("Discord Server  : https://discord.gg/2CVuXXTUVr")
            print()
            print(f"Current version : '{version}'")
            sys.exit(0)
    print("Hello World ! Let's start with posting a simple message.")
    # server = input("What's your instance (like `https://mastodon.social`) : ")
    # token = input("What's your account token :")

    server = str(os.environ.get("SERVER"))
    token = os.environ.get("TOKEN_ACCESS")

    client = Client(token=token, server=server)

    @client.schedule()
    def on_starting(local_client: Client) -> None:
        s = local_client.post_status(DEFAULT_MESSAGE.format(asctime()))
        print(f"\nYou can view the post at `{s.uri}` or on your bot's feed feed.")
        local_client.stop()

    print("Running client ...")

    client.run()
