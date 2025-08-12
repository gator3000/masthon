The client is defined here.

# TOKEN_FORMAT
#constant #compiled_regex

The format of the token with regex.

# SERVER_FORMAT
#constant #compiled_regex 

The format of an instance's url.

___
# Client
#class #client #exported

The client !
[[#__init__()|Initialisation here]]

### RUNNING
#mainloop #client 

<<<<<<< HEAD
`bool` : `True` if the loop is running else, `False`. You can change it to stop the loop but use instead [[#`stop()`]].

### \_\_repr__()
#method #client #dunder

...

### \_\_format__()
#method #client #dunder 

Allowing user to display the client with token or without. 

### \_\_init__()
=======
`bool` : `True` if the loop is running else, `False`. You can change it to stop the loop but use instead [[#`stop(...)`]].

### \_\_repr__(...)
#method #client #dunder

...

### \_\_format__(...)
#method #client #dunder 

Allowing user to display the client with token or without. 

### \_\_init__(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #constructor #client #dunder #events

```py
def __init__(
	self,
	token: str,
	server: str = "https://mastodon.social",
	*,
    async_level: int = 0,
    used_events: Optional[Event | Tuple[Event]] = None,
    event_reactivity: int = 15,
) -> None:
```

> [!NOTE] `async_level` :
> #threading 
> > [!NOTE]- `0`: No threading
> > -> just execute sequentially your function when they must
>
> > [!NOTE]- `1`: Step by step threading
> > -> execute with threads each steps of the main loop and wait them before starting the next step
> > (not very useful except if you have two or more functions which will be executed at the same loop step but even use level 2 if your hardware has very few RAM because less threads will run (and be saved) at the same time.)
>
> > [!NOTE]- `2`: Full threading `[RECOMENDED]`
> > -> start threads and just go forward without waiting them to continue
> > allowing you to execute commands event if a thread is working in background

> [!NOTE] `event_reactivity` :
> #events 
> Every x seconds, client will check possible events triggered


<<<<<<< HEAD
### stop()
=======
### stop(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #mainloop #client

Use this method to stop manually the mainloop.

<<<<<<< HEAD
### run()
=======
### run(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #mainloop #client 

Start the mainloop. Return `None` when loop is finished or raise a `RuntimeError` if you try to start 2 instances of the same client at the same time.

<<<<<<< HEAD
### \_raw_request()
=======
### \_raw_request(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #client #RequestAPI

```py
def _raw_request(
	self,
	path: str,
	method: RequestMethod,
	annonymous: Optional[bool] = False,
	files: Optional[Dict[str, Tuple[str, IO, str]]] = None,
	additional_data: Dict[str, str] = {},
	json_data: bool = False,
	ratelimit_security: bool = True,
	**kwargs: Dict[str, str],
) -> requests.Response:
```
Use it to make a request to the api. `path` must start with a `"/"` like `"/api/v1/statuses`.

<<<<<<< HEAD
### post_status()
=======
### post_status(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #client #RequestAPI #statuses 

```py
def post_status(
	self,
	text: str,
	medias: Optional[List[str]] = [],
	visibility: Visibility = Visibility.UNLISTED,
	in_reply_to_id: Optional[str] = None,
	sensitive: Optional[Literal[None, True]] = None,
	language: Optional[str] = "en",
	**kwargs,
) -> List[Status] | Status:
```
...

> [!Example] References
> [[DataClasses py#Status]]

<<<<<<< HEAD
### upload_media()
=======
### upload_media(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #client #RequestAPI 

```py
def upload_media(
	self, src: str, *, type_: str = "image/{ext}", **kwargs
) -> MediaAttachment:
```
`type_` is the type of the file like `"image/png"` or `"audio/mpeg"

> [!Example] References
> [[DataClasses py#MediaAttachment]]

<<<<<<< HEAD
### delete_status()
=======
### delete_status(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #client #RequestAPI #statuses

`def delete_status(self, status: Status | str, **kwargs) -> requests.Response:`
Just delete a status with its id or its object.

<<<<<<< HEAD
### unread_notifications_count()
=======
### unread_notifications_count(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #client #RequestAPI #notifications

```py
def unread_notifications_count(
	self, types: Iterable[NotificationType] = [], **kwargs
) -> int:
```
...

<<<<<<< HEAD
### get_notifications()
=======
### get_notifications(...)
>>>>>>> cdd0657 (Update testing with my weirds commits on main before)
#method #client #RequestAPI #notifications

```py
def get_notifications(
	self,
	types: Iterable[NotificationType] = [],
	limit: Optional[int] = None,
	min_id: Optional[str] = None,
	**kwargs,
) -> List[Notification]:
```
...

> [!Example] References
> [[DataClasses py#Notification]]

### get_marker()
#method #client #RequestAPI #notifications #timelines #markers

```py
def get_marker( 
	self, timeline: Iterable[TimelineType], **kwargs
) -> Dict[TimelineType, Marker]:
```
...

> [!Example] References
> [[DataClasses py#TimelineType]]
> [[DataClasses py#Marker]]

### post_marker()
#method #client #RequestAPI #notifications #timelines #markers 

```py
def post_marker(
	self, timelines: Dict[str, Dict[str, str]], **kwargs
) -> Dict[TimelineType, Marker]:
```
...

> [!Example] References
> [[DataClasses py#TimelineType]]
> [[DataClasses py#Marker]]

### looped_every()
#method #client #decoratorGenerator #scheduling #loopedfunctions

`def looped_every(self, time: float = 60) -> Callable:`
Return a decorator to make your function executed every \<`time`\> seconds.

### schedule()
#method #client #decoratorGenerator #scheduling 

`def schedule(self, after: float = 0) -> Callable:`
Make your function executed \<`after`\> seconds after your run the client.

### add_command()
#method #client #decoratorGenerator #CLI 

`def add_command(self, name: str) -> Callable:`
Add your function to the command list.

### listen_for()
#method #client #decoratorGenerator #events 

`def listen_for(self, event: Event) -> Callable:`
Call your function when `event` is triggered.

### execute()
#method #client #decorator #simpleevents 

`def execute(self, func: Callable) -> Callable:`
Use the name of  the decorated function to call it.
Must be part of `("on_start", "on_loop_step", "on_stop")`.