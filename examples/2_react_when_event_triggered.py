"""
3rd example :)

Interact with other accounts !
"""

from typing import List, Dict

from masthon import Client, Exceptions
from masthon.DataClasses import *


c = Client(
    "YOUR TOKEN HERE",
    used_events=Event.NEW_MENTION,  # A list of events used in the program if one, it can be just the event
    event_reactivity=3,  # Every x seconds, client will check possible events triggered
)


@c.listen_for(Event.NEW_MENTION)                                       # Will be triggered only when NEW_MENTION is
def mention(
    client: Client, data: Dict[str, List[Notification] | Notification]
):                                                                     # Defaults arguments to handle
    # Mypy checker crap
    assert isinstance(data["notification"], Notification), Exceptions.MasthonException
    assert isinstance(data["notification"].status, Status), Exceptions.MasthonException

    # reply !
    client.post_status(
        "You've called me ??\nDon't worry, I'm here sir !\n\nSent from #masthon with <3",
        in_reply_to_id=data["notification"].status.id,
    )


c.run()
