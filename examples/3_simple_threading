"""
4th example

Understand "async" (threading actually) with this module
"""

from masthon import Client, DataClasses

from time import sleep


lvl = int(input("Choose your async_level [0|1|2] : "))
"""
0: No threading
-> just execute sequentially your function when they must

1: Step by step threading
-> execute with threads each steps of the main loop and wait them before starting the next step
(not very useful except if you have 2 or more functions which will be executed at the same
loop step but even use level 2 if your hardware has very few RAM because less threads will
run (and be saved) at the same time.)

2: Full threading
-> start threads and just go forward without waiting them to continue
allow you to execute commands event if a thread is working in background
"""

# token not really required because we don't use it in this example
client = Client("YOUR TOKEN HERE! or just 43 chars like this", async_level=lvl)


@client.looped_every(10)
def long_one(local_client: Client):
    print("Long action 1 started !")
    sleep(
        8
    )  # simulate a long action like uploading medias ... that will normally block the loop
    print("Long action 1 finished !")


@client.looped_every(7)
def long_two(local_client: Client):
    print("Long action 2 started !")
    sleep(
        5
    )  # simulate another long action like uploading medias ... that will normally block the loop
    print("Long action 2 finished !")


@client.add_command("print")  # allow you to test comands with every level
def test(local_client: Client):
    print(f'{" Command executed ! ":_^40}')


client.run()
