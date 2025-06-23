Here I'll explain examples.


# 0. Get started
#loopedfunctions #CLI #scheduling 
This example allow you to understand how to set cyclic actions, commands and sheduled functions. It use the client method [[Client py]]
```py
"""
First example !

Just to handle the module.
"""

from masthon import Client, DEFAULT_MESSAGE

from time import asctime

  
# create a client
client = Client("YOUR TOKEN HERE")
  

# shedule client actions after time indicated
@client.schedule(5) # in seconds
def say_hello(local_client: Client): # default arument passed to back_tasks
	local_client.post_status("Hello World from the API !") # use client method `post_status`


# shedule client cyclic actions
@client.looped_every(180) # in seconds = 3 minutes
def post_greetings(local_client: Client): # default arument passed to back_tasks
	local_client.post_status(DEFAULT_MESSAGE.format(asctime())) # use client method `post_status`


# create commands to be used by you
@client.add_command(name="post") # name to use in he cli tool
def post(local_client: Client, *ms: str): # 1 default argument for all cmds (client) and a list of str : a sentence
	"""post a status"""
	m = " ".join(ms) # rework the sentence to one string
	local_client.post_status(m) # use client method `post_status`



# this run your bot !
client.run()
```

# 1. Publish periodical data

# 2. React when event triggered

# 3. Simple threading
