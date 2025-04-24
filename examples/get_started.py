from typing import Tuple

from masthon import Client, DEFAULT_MESSAGE

from time import asctime


# create a client
client = Client("YOUR TOKEN HERE")

# shedule client cyclic actions
@client.looped_every(60)                                        # in seconds = 1 minute
def post_greetings(local_client: Client):                       # default arument passed to back_tasks
    local_client.post_status(DEFAULT_MESSAGE.format(asctime())) # use client method `post_status`

# create commands to be used by you
@client.add_command(name="post")                 # name to use in he cli tool
def post(local_client: Client, *ms: Tuple[str]): # mean 1 default argument for all cmds (client) and a list of str : a sentence
    m = " ".join(ms)                             # rework the sentence to one string
    local_client.post_status(m)                  # use client method `post_status`


# this run your bot !
client.run() 
