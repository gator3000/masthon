from typing import Self, Dict
from enum import Enum

from .definitions import Client
from .DataClasses import *
from .Exceptions import *

import json


class ListenerOutput:
    def __init__(self, status: EventStatus, data: Dict):
        self.status = status
        self.data = data


class Listeners:
    # def __init__(self, client: Client):
    def __init__(self, client):
        self.client = client

    def listen_for(self, event: Event, *args, **kwargs) -> ListenerOutput:
        output: ListenerOutput
        match event:
            case Event.UNREAD_NOTIFICATION:
                output = self.listen_notification(*args, **kwargs)
            case Event.NEW_MENTION:
                output = self.listen_mention(*args, **kwargs)
            case _:
                raise ValueError(
                    "Argument event must be of type `masthon.Events.Event` (`Event`)"
                )
        return output

    def listen_notification(self) -> ListenerOutput:
        try:
            number: int = self.client.unread_notifications_count()
            notifications: List[Notification] = list()
            if number > 0:
                notifications = self.client.get_notifications(limit=number)
                # reset unread marker
                self.client.post_marker(
                    {
                        TimelineType.NOTIFICATIONS.value: {
                            "last_read_id": notifications[-1].id
                        }
                    }
                )
        except HTTPError as e:
            if len(e.args) > 2:
                return ListenerOutput(EventStatus.ERROR, json.loads(e.args[2]))
            else:
                return ListenerOutput(EventStatus.ERROR, {"error": "unknow"})
        else:
            return ListenerOutput(
                status=EventStatus.TRIGGERED if number > 0 else EventStatus.NONE,
                data={"count": number, "notifications": notifications, "notification": notifications[-1] if len(notifications) > 0 else None},
            )

    def listen_mention(self) -> ListenerOutput:
        try:
            number: int = self.client.unread_notifications_count(types=[NotificationType.MENTION])
            notifications: List[Notification] = list()
            if number > 0:
                notifications = self.client.get_notifications(types=[NotificationType.MENTION], limit=number)
                # reset unread marker
                self.client.post_marker(
                    {
                        TimelineType.NOTIFICATIONS.value: {
                            "last_read_id": notifications[-1].id
                        }
                    }
                )
        except HTTPError as e:
            if len(e.args) > 2:
                return ListenerOutput(EventStatus.ERROR, json.loads(e.args[2]))
            else:
                return ListenerOutput(EventStatus.ERROR, {"error": "unknow"})
        else:
            return ListenerOutput(
                status=EventStatus.TRIGGERED if number > 0 else EventStatus.NONE,
                data={"count": number, "notifications": notifications, "notification": notifications[-1] if len(notifications) > 0 else None},
            )
