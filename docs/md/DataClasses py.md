All data-classes and enums of the package.
The type `datetime`  come from the module `datetime`.


# Enums

### RequestMethod
#enum #RequestAPI 

> [!Example]- Items
> - GET
> - POST
> - DELETE
>- PUT
> - PATCH

___
### Visibility
#enum #statuses 

> [!Example]- Items
> - PUBLIC
> - UNLISTED
> - PRIVATE
> - DIRECT

___
### Event
#enum #events 

> [!Example]- Items
> - UNREAD_NOTIFICATION
> - NEW_MENTION 

___
### EventStatus
#enum #events 

> [!Example]- Items
> - TRIGGERED
> - NONE
> - ERROR

___
### NotificationType
#enum #notifications 

> [!Example]- Items
> - MENTION
> - STATUS
> - REBLOG
> - FOLLOW
> - FOLLOW_REQUEST
> - FAVOURITE
> - POLL
> - UPDATE
> - ADMIN_SIGN_UP
> - ADMIN_REPORT

___
### TimelineType
#enum  #timelines 

> [!Example]- Items
> - HOME
> - NOTIFICATIONS

___
### MediaType
#enum 

> [!Example]- Items
> - UNKNOWN
> - IMAGE
> - GIFV
> - VIDEO
> - AUDIO

___
### PreviewCardType
#enum 

> [!Example]- Items
> - LINK
> - PHOTO
> - VIDEO
> - RICH

___
### Context
#enum 

> [!Example]- Items
> - HOME
> - NOTIFICATIONS
> - PUBLIC
> - THREAD
> - ACCOUNT

___
### FilterAction
#enum 

> [!Example]- Items
> - WARN
> - HIDE
> - BLUR

___
### QuoteState
#enum 

> [!Example]- Items
> - PENDING
> - ACCEPTED
> - REJECTED
> - REVOKED
> - DELETED
> - UNAUTHORIZED

___
### ReportCategory
#enum 

> [!Example]- Items
> - SPAM
> - VIOLATION
> - OTHER

___
### RelationshipSeveranceEventType
#enum 

> [!Example]- Items
> - DOMAIN_BLOCK
> - USER_DOMAIN_BLOCK
> - ACCOUNT_SUSPENSION

___
### AppealState
#enum 

> [!Example]- Items
> - APPROVED
> - REJECTED
> - PENDING

___
### WarningAction
#enum 

> [!Example]- Items
> - NONE
> - DISABLE
> - MARK_STATUSES_AS_SENSITIVE
> - DELETE_STATUSES
> - SENSITIVE
> - SILENCE
> - SUSPEND

___

# Dataclasses

### Aliases
`URL` -> `str`
`ID` -> `str`
`DATETIME` -> `str | datetime`

## APIDATACLASS
#decoratorGenerator 

Define `__post_init__` for all #dataclass and auto convert arguments thanks to `DATETIME`, `API_OBJECT`, `ENUM` Type Aliases.

___
### Emoji
#dataclass

> [!Example]- Attributes
> - shortcode: `str`
> - url: `URL`
> - static_url: `URL`
> - visible_in_picker: `bool`
> - category: `str`

___
### Field
#dataclass

> [!Example]- Attributes
> - name: `str`
> - value: `str`
> - verified_at: `DATETIME`

___
### ImageMetaInfos
#dataclass

> [!Example]- Attributes
> - width: `int`
> - height: `int`
> - size: `str`
> - aspect: `float`

___
### Focus
#dataclass

> [!Example]- Attributes
> - x: `float`
> - y: `float`

___
### Meta
#dataclass

> [!Example]- Attributes
> - original: `ImageMetaInfos` [[#ImageMetaInfos]]
> - small: `ImageMetaInfos` [[#ImageMetaInfos]]
> - focus: `Focus` [[#Focus]]

___
### Source
#dataclass

> [!Example]- Attributes
> - privacy: `Visibility` [[#Visibility]]
> - sensitive: `bool`
> - language: `str`
> - note: `str`
> - fields: `List[Field]` [[#Field]]
> - follow_requests_count: `int`

___
### Role
#dataclass

> [!Example]- Attributes
> - id: `ID`
> - name: `str`
> - permissions: `str`
> - color: `str`
> - highlighted: `bool`

___
### Account
#dataclass

> [!Example]- Attributes
> - id: `ID`
> - username: `str`
> - acct: `str`
> - url: `URL`
> - display_name: `str`
> - note: `str`
> - avatar: `URL`
> - avatar_static: `URL`
> - header: `URL`
> - header_static: `URL`
> - locked: `bool`
> - fields: `List[Field]` [[#Field]]
> - emojis: `List[Emoji]` [[#Emoji]]
> - bot: `bool`
> - created_at: `DATETIME`
> - statuses_count: `int`
> - followers_count: `int`
> - following_count: `int`
> - last_status_at: `DATETIME`
> - noindex: `bool`
> - moved: `Account` [[#Account]]
> - suspended: `bool`
> - limited: `bool`
> - group: `bool`
> - discoverable: `bool`
> - attribution_domains: `List[URL]`
> - source: `Source]` [[#Source]]
> - role: `Role]` [[#Role]]
> - mute_expires_at: `DATETIME`
> - indexable: `bool`
> - uri: `URL]`
> - hide_collections: `bool`
> - roles: `List[Role]` [[#Role]]

___
### Application
#dataclass

> [!Example]- Attributes
> - name: `str`
> - scopes: `List[str]`
> - redirect_uris: `List[URL]`
> - website: `URL`
> - redirect_uri: `URL`
> - vapid_key: `str`
> - client_id: `ID`
> - client_secret: `str`
> - client_secret_expires_at: `DATETIME | int`
> - website: `str`

___
### Mention
#dataclass

> [!Example]- Attributes
> - id: `ID`
> - username: `str`
> - url: `URL`
> - acct: `str`

___
### Tag
#dataclass

> [!Example]- Attributes
> - name: `str`
> - url: `URL`

___
### MediaAttachment
#dataclass

> [!Example]- Attributes
> - id: `ID`
> - type: `MediaType` [[#MediaType]]
> - url: `URL`
> - preview_url: `URL`
> - preview_remote_url: `URL`
> - meta: `Meta` [[#Meta]]
> - text_url: `URL`
> - remote_url: `URL`
> - description: `str`
> - blurhash: `str`

___
### Poll_Option
#dataclass 

> [!Example]- Attributes
> - title: `str`
> - votes_count: `int`

___
### Poll
#dataclass

> [!Example]- Attributes
> - id: `ID`
> - expires_at: `DATETIME`
> - expired: `bool`
> - multiple: `bool`
> - votes_count: `int`
> - voters_count: `int`
> - options: `List[Poll_Option]` [[#Poll_Option]]
> - emojis: `List[Emoji]` [[#Emoji]]
> - voted: `bool`

___
### PreviewCardAuthor
#dataclass 

> [!Example]- Attributes
> - name: `str`
> - url: `URL`
> - account: `Account` [[#Account]]

___
### PreviewCard
#dataclass

> [!Example]- Attributes
> - url: `URL`
> - title: `str`
> - description: `str`
> - type: `PreviewCardType` [[#PreviewCardType]]
> - author_name: `str`
> - author_url: `URL`
> - provider_name: `str`
> - provider_url: `URL`
> - html: `str`
> - width: `int`
> - height: `int`
> - embed_url: `URL`
> - authors: `List[PreviewCardAuthor]]`
> - image: `str`
> - blurhash: `str`
> - language: `str`

___
### Quote
#dataclass 

> [!Example]- Attributes
> - state: `QuoteState` [[#QuoteState]]
> - status: `Status` [[#Status]]

___
### ShallowQuote
#dataclass 

> [!Example]- Attributes
> - state: `QuoteState` [[#QuoteState]]
> - status_id: `ID`

___
### FilterKeyword
#dataclass 

> [!Example]- Attributes
> - id: `ID`
> - keyword: `str`
> - whole_word: `bool`

___
### FilterStatus
#dataclass 

> [!Example]- Attributes
> - id: `ID`
> - status_id: `ID`

___
### Filter
#dataclass 

> [!Example]- Attributes
> - id: `ID`
> - title: `str`
> - context: `List[Context]` [[#Context]]
> - expires_at: `DATETIME`
> - filter_action: `FilterAction` [[#FilterAction]]
> - keywords: `List[FilterKeyword]` [[#FilterKeyword]]
> - statuses: `List[FilterStatus]` [[#FilterStatus]]

___
### FilterResult
#dataclass 

> [!Example]- Attributes
> - filter: `Filter` [[#Filter]]
> - keyword_matches: `List[str]
> - status_matches: `List[str]

___
### Status
#dataclass #statuses 

> [!Example]- Attributes
> - id: `ID`
> - uri: `URL`
> - created_at: `DATETIME`
> - account: `Account` [[#Account]]
> - content: `str`
> - visibility: `Visibility` [[#Visibility]]
> - sensitive: `bool`
> - spoiler_text: `str`
> - media_attachments: `List[MediaAttachment]` [[#MediaAttachment]]
> - mentions: `List[Mention]` [[#Mention]]
> - tags: `List[Tag]` [[#Tag]]
> - emojis: `List[Emoji]` [[#Emoji]]
> - reblogs_count: `int`
> - favourites_count: `int`
> - replies_count: `int`
> - application: `Application` [[#Application]]
> - url: `URL`
> - in_reply_to_id: `ID`
> - in_reply_to_account_id: `ID`
> - reblog: `Status` [[#Status]]
> - poll: `Poll` [[#Poll]]
> - card: `PreviewCard` [[#PreviewCard]]
> - language: `str`
> - text: `str`
> - edited_at: `DATETIME`
> - favourited: `bool`
> - reblogged: `bool`
> - muted: `bool`
> - bookmarked: `bool`
> - pinned: `bool`
> - filtered: `List[FilterResult]` [[#FilterResult]]
> - quote: `Quote | ShallowQuote` [[#Quote]] [[#ShallowQuote]]

___
### Report
#dataclass 

> [!Example]- Attributes
> - id: `ID`
> - action_taken: `bool`
> - action_taken_at: `DATETIME`
> - category: `ReportCategory` [[#ReportCategory]]
> - comment: `str`
> - forwarded: `bool`
> - created_at: `DATETIME`
> - status_ids: `List[ID]`
> - rule_ids: `List[ID]`
> - target_account: `Account` [[#Account]]

___
### RelationshipSeveranceEvent
#dataclass 

> [!Example]- Attributes
> - id: `ID`
> - type: `RelationshipSeveranceEventType` [[#RelationshipSeveranceEventType]]
> - purged: `bool`
> - target_name: `str`
> - followers_count: `int`
> - following_count: `int`
> - created_at: `DATETIME`

___
### Appeal
#dataclass 

> [!Example]- Attributes
> - text: `str`
> - state: `AppealState` [[#AppealState]]

___
### AccountWarning
#dataclass 

> [!Example]- Attributes
> - id: `ID`
> - action: `WarningAction` [[#WarningAction]]
> - text: `str`
> - status_ids: `List[ID]`
> - target_account: `Account` [[#Account]]
> - appeal: `Appeal` [[#Appeal]]
> - created_at: `DATETIME`

___
### Notification
#dataclass #notifications 

> [!Example]- Attributes
> - id: `ID`
> - type: `NotificationType` [[#NotificationType]]
> - group_key: `str`
> - created_at: `DATETIME`
> - account: `Account` [[#Account]]
> - status: `Status` [[#Status]]
> - report: `Report` [[#Report]]
> - event: `RelationshipSeveranceEvent` [[#RelationshipSeveranceEvent]]
> - moderation_warning: `AccountWarning` [[#AccountWarning]]

___
### Marker
#dataclass #markers 

> [!Example]- Attributes
> - last_read_id: `ID`
> - version: `int`
> - updated_at: `DATETIME`
