from .Client import Client

__version__ = "v0.3b1"


DEFAULT_MESSAGE = """Hello from the #API at time : `{}`.
The project used is **#Masthon** a simple #python package whitch links to #Mastodon coded by an #french student !
Let's check my #code on #gitlab -> https://gitlab.com/Gator3000/masthon.git. It's #opensource !

Talk to me about my project at `@gator3000@mastodon.social` or on discord `_gator3000` / https://discord.gg/2CVuXXTUVr

#mastodonAPI #masto #français #developpement #dev"""

__all__ = (
    "__version__",
    "Client",
    "DataClasses",
    "Events",
    "Exceptions",
    "utils",
    "DEFAULT_MESSAGE",
)
