All data-classes of the package.
The type `datetime`  come from the module `datetime`.

# Dataclasses
## Emoji
#dataclass
- shortcode: `str`
- url: `str`
- static_url: `str`
- visible_in_picker: `bool`

## Field
#dataclass
- name: `str`
- value: `str`
- verified_at: `datetime`

## ImageMetaInfos
#dataclass
- width: `int`
- height: `int`
- size: `str`
- aspect: `float`

## Focus
#dataclass
- x: `float`
- y: `float`

## Meta
#dataclass
- original: `ImageMetaInfos` [[docs/md/DataClasses.py#ImageMetaInfos]]
- small: `ImageMetaInfos` [[docs/md/DataClasses.py#ImageMetaInfos]]
- focus: `Focus` [[docs/md/DataClasses.py#Focus]]

## Source
#dataclass
- privacy: `str`
- sensitive: `bool`
- language: `str`
- note: `str`
- fields: `List[Field]` [[docs/md/DataClasses.py#Field]]
- follow_requests_count: `int`

## Role
#dataclass
- id: `str`
- name: `str`
- permissions: `str`
- color: `str`
- highlighted: `bool`

## Account
#dataclass
- id: `str`
- username: `str`
- acct: `str`
- url: `str`
- display_name: `str`
- note: `str`
- avatar: `str`
- avatar_static: `str`
- header: `str`
- header_static: `str`
- locked: `bool`
- fields: `List[Field]` [[docs/md/DataClasses.py#Field]]
- emojis: `List[Emoji]` [[docs/md/DataClasses.py#Emoji]]
- bot: `bool`
- created_at: `datetime`
- statuses_count: `int`
- followers_count: `int`
- following_count: `int`
- last_status_at: `Optional[datetime]`
- noindex: `Optional[bool]`
- moved: `Optional[Account]` [[docs/md/DataClasses.py#Account]]
- suspended: `Optional[bool]`
- limited: `Optional[bool]`
- group: `Optional[bool]`
- discoverable: `Optional[bool]`
- attribution_domains: `Optional[List[str]]`
- source: `Optional[Source]` [[docs/md/DataClasses.py#Source]]
- role: `Optional[Role]` [[docs/md/DataClasses.py#Role]]
- mute_expires_at: `Optional[datetime]`
- indexable: `Optional[bool]`
- uri: `Optional[str]`
- hide_collections: `Optional[bool]`
- roles: `Optional[List[Role]]` [[docs/md/DataClasses.py#Role]]

## Application
#dataclass
- name: `str`
- website: `Optional[str]`

## Mention
#dataclass
- id: `str`
- username: `str`
- url: `str`
- acct: `str`

## Tag
#dataclass
- name: `str`
- url: `str`

## MediaAttachment
#dataclass
- id: `str`
- type: `str`
- url: `str`
- preview_url: `str`
- preview_remote_url: `str`
- meta: `Meta` [[docs/md/DataClasses.py#Meta]]
- text_url: `Optional[str]`
- remote_url: `Optional[str]`
- description: `Optional[str]`
- blurhash: `Optional[str]`

## Poll_Option
#dataclass 
- title: `str`
- votes_count: `Optional[int]`

## Poll
#dataclass
- id: `str`
- expires_at: `datetime`
- expired: `bool`
- multiple: `bool`
- votes_count: `int`
- voters_count: `int`
- options: `List[Poll_Option]` [[docs/md/DataClasses.py#Poll_Option]]
- emojis: `List[Emoji]` [[docs/md/DataClasses.py#Emoji]]
- voted: `Optional[bool]`

## PreviewCard
#dataclass
- url: `str`
- title: `str`
- description: `str`
- type: `str`
- author_name: `str`
- author_url: `str`
- provider_name: `str`
- provider_url: `str`
- html: `str`
- width: `int`
- height: `int`
- embed_url: `str`
- image: `Optional[str]`
- blurhash: `Optional[str]`

## Quote
#dataclass 
- state: `str`
- status: `Optional[Status]` [[docs/md/DataClasses.py#Status]]

## Status
#dataclass #statuses 
- id: `str`
- uri: `str`
- created_at: `datetime`
- account: `Account` [[docs/md/DataClasses.py#Account]]
- content: `str`
- visibility: `str`
- sensitive: `bool`
- spoiler_text: `str`
- media_attachments: `List[MediaAttachment]` [[docs/md/DataClasses.py#MediaAttachment]]
- mentions: `List[Mention]` [[docs/md/DataClasses.py#Mention]]
- tags: `List[Tag]` [[docs/md/DataClasses.py#Tag]]
- emojis: `List[Emoji]` [[docs/md/DataClasses.py#Emoji]]
- reblogs_count: `int`
- favourites_count: `int`
- replies_count: `int`
- application: `Optional[Application]` [[docs/md/DataClasses.py#Application]]
- url: `Optional[str]`
- in_reply_to_id: `Optional[str]`
- in_reply_to_account_id: `Optional[str]`
- reblog: `Optional[Status]` [[docs/md/DataClasses.py#Status]]
- poll: `Optional[Poll]` [[docs/md/DataClasses.py#Poll]]
- card: `Optional[PreviewCard]` [[docs/md/DataClasses.py#PreviewCard]]
- language: `Optional[str]`
- text: `Optional[str]`
- edited_at: `Optional[str]`
- favourited: `Optional[bool]`
- reblogged: `Optional[bool]`
- muted: `Optional[bool]`
- bookmarked: `Optional[bool]`
- pinned: `Optional[bool]`
- filtered: `Optional[List[Dict[str, Any]]]`
- quote: `Optional[Quote]` [[docs/md/DataClasses.py#Quote]]

## Report
#dataclass 
- id: `str`
- action_taken: `bool`
- action_taken_at: `Optional[datetime]`
- category: `str`
- comment: `str`
- forwarded: `bool`
- created_at: `datetime`
- status_ids: `Optional[List[str]]`
- rule_ids: `Optional[List[str]]`
- target_account: `Account` [[docs/md/DataClasses.py#Account]]

## RelationshipSeveranceEvent
#dataclass 
- id: `str`
- type: `str`
- purged: `bool`
- target_name: `str`
- followers_count: `int`
- following_count: `int`
- created_at: `datetime`

## Appeal
#dataclass 
- text: `str`
- state: `str`

## AccountWarning
#dataclass 
- id: `str`
- action: `str`
- text: `str`
- status_ids: `Optional[List[str]]`
- target_account: `Account` [[docs/md/DataClasses.py#Account]]
- appeal: `Optional[Appeal]` [[docs/md/DataClasses.py#Appeal]]
- created_at: `datetime`

## Notification
#dataclass #notifications 
- id: `str`
- type: `str`
- group_key: `str`
- created_at: `datetime`
- account: `Account` [[docs/md/DataClasses.py#Account]]
- status: `Optional[Status]`
- report: `Optional[Report]` [[docs/md/DataClasses.py#Report]]
- event: `Optional[RelationshipSeveranceEvent]` [[docs/md/DataClasses.py#RelationshipSeveranceEvent]]
- moderation_warning: `Optional[AccountWarning]` [[docs/md/DataClasses.py#AccountWarning]]

## Marker
#dataclass #markers 
- last_read_id: `str`
- version: `int`
- updated_at: `datetime`

# Enums

## RequestMethod
#enum
- GET
- POST
- DELETE
- PUT
- PATCH

## Visibility
#enum 
- PUBLIC
- UNLISTED
- PRIVATE
- DIRECT

## Event
#enum 
- UNREAD_NOTIFICATION
- NEW_MENTION

## EventStatus
#enum 
- TRIGGERED
- NONE
- ERROR

## NotificationType
#enum #notifications 
- MENTION
- STATUS
- REBLOG
- FOLLOW
- FOLLOW_REQUEST
- FAVOURITE
- POLL
- UPDATE
- ADMIN_SIGN_UP
- ADMIN_REPORT

## TimelineType
#enum  #timelines 
- HOME
- NOTIFICATIONS