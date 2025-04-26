from .__init__ import *
from time import asctime


if __name__ == "__main__":
    print("Hello World form the dev branch ! Let's start with posting a simple message.")
    server = input("What's your instance (like `https://mastodon.social`) : ")
    token = input("What's your account token : ")

    client = Client(token=token, server=server)

    @client.schedule()
    def on_starting(local_client: Client) -> None:
        local_client.post_status(DEFAULT_MESSAGE.format(asctime()))
    
    print("Running client ...")

    client.run()