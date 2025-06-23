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

#### epoch
#attribute #client #mainloop 
The result of `time.time()` when mainloop is started. else, `None`.

#### funcs
#attribute #client #scheduling
`Dict[<float1>, List[Tuple[<float2>, <Callable>]]]`
Associate time (`<float1>`) between `<Callable>` is executed to his last time (`<float2>`).

#### scheduled
#attribute #client #scheduling 
`Dict[Callable, float]`
Associate function (`Callable`) to his delay (`float`) before it will be executed relative to [[#epoch]].

#### commands
#attribute #client #CLI
`Dict[str, Callable]`
Associate the command name (`str`) to its function (`Callable`).

#### cli_last_error
#attribute #client #CLI #exceptionManaging
Contain the last error raised by a command from the CLI system.

#### RUNNING
#attribute #mainloop #client 
`bool` : `True` if the loop is running else, `False`. You can change it to stop the loop but use instead [[#`stop(...)`]].

#### __init__(...)
#method #constructor #client #dunder #events
```py
def __init__(
	self,
	token: str,
	server: str = "https://mastodon.social",
	*,
	used_events: Optional[Event | Tuple[Event]] = None,
	event_reactivity: int = 15,
) -> None:
```

#### stop(...)
#method #mainloop #client
Use this method to stop manually the mainloop.

#### run(...)
#method #mainloop #client 
Start the mainloop. Return `None` when loop is stopped.

#### \_raw_request(...)
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

#### post_status(...)
#method #client #RequestAPI #statuses 
```py
def post_status(
	self,
	text: str = "Hello World from Mastodon API !",
	medias: Optional[List[str]] = [],
	visibility: Visibility = Visibility.UNLISTED,
	in_reply_to_id: Optional[str] = None,
	sensitive: Optional[Literal[None, True]] = None,
	language: Optional[str] = "en",
	**kwargs,
) -> List[Status] | Status:
```
... [[docs/md/DataClasses.py#Status]]

#### upload_media(...)
#method #client #RequestAPI 
```py
def upload_media(
	self, src: str, *, type_: str = "image/{ext}", **kwargs
) -> MediaAttachment:
```
`type_` is the type of the file like `"image/png"` or `"audio/mpeg"
[[docs/md/DataClasses.py#MediaAttachment]]

#### delete_status(...)
#method #client #RequestAPI #statuses
`def delete_status(self, status: Status | str, **kwargs) -> requests.Response:`
Just delete a status with its id or its object.

#### unread_notifications_count(...)
#method #client #RequestAPI #notifications
```py
def unread_notifications_count(
	self, types: Iterable[NotificationType] = [], **kwargs
) -> int:
```
...

#### get_notifications(...)
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
... [[docs/md/DataClasses.py#Notification]]

#### get_marker(...)
#method #client #RequestAPI #notifications #timelines #markers
```py
def get_marker( 
	self, timeline: Iterable[TimelineType], **kwargs
) -> Dict[TimelineType, Marker]:
```
...
[[docs/md/DataClasses.py#TimelineType]]
[[docs/md/DataClasses.py#Marker]]

#### post_marker(...)
#method #client #RequestAPI #notifications #timelines #markers 
```py
def post_marker(
	self, timelines: Dict[str, str], **kwargs
) -> Dict[TimelineType, Marker]:
```
...
[[docs/md/DataClasses.py#TimelineType]]
[[docs/md/DataClasses.py#Marker]]

#### looped_every(...)
#method #client #decoratorGenerator #scheduling #loopedfunctions
`def looped_every(self, time: float = 60) -> Callable:`
Return a decorator to make your function executed every \<`time`\> seconds.

#### schedule(...)
#method #client #decoratorGenerator #scheduling 
`def schedule(self, after: float = 0) -> Callable:`
Make your function executed \<`after`\> seconds after your run the client.

#### add_command(...)
#method #client #decoratorGenerator #CLI 
`def add_command(self, name: str) -> Callable:`
Add your function to the command list.

#### listen_for(...)
#method #client #decoratorGenerator #events 
`def listen_for(self, event: Event) -> Callable:`
Call your function when `event` is triggered.