# Masthon

A simple API for linking mastodon to your python codes.

#Author : org.literie.gator

#LastVersion : 0.3 Beta

#FormatedDocumentation : at [Documentation on Gitlab Pages](https://Gator3000.gitlab.io/masthon)
___
# Features
- [x] Version Check [[__main__ py#Version Checker]]
- Masthon engine
	- [x] main loop -> #mainloop
	- [x] asynchronous (actually, threading) #threading
- Server Interactions
	- [x] Make a request to your server #RequestAPI
	- Statuses
	    - [x] Post [[Client py#post_status(...)]]
	    - [x] Delete [[Client py#delete_status(...)]]
	    - [x] Upload a file [[Client py#upload_media(...)]]
	- Users
		- [ ] Get user
	- Timelines
		- Home & Tags
			- [ ] Get timeline
		- Notifications #notifications 
		    - [x] Get unread notification count [[Client py#unread_notifications_count(...)]]
		    - [x] Get last received notifications [[Client py#get_notifications(...)]]
		-  Markers #markers 
		    - [x] Post [[Client py#post_marker(...)]]
		    - [x] Get [[Client py#get_marker(...)]]
- Event managing
	- [x] Handler #events [[Client py#listen_for(...)]]
		- [x] unread notification
		- [x] new mention
		- [ ] new post in timeline
			- [ ] home
			- [ ] account
			- [ ] tag
- CLI interface #CLI
	- [x] Handler
		- [x] some defaults commands [[Client py#commands]]
		- [x] create new command [[Client py#add_command(...)]]
- Scheduling #scheduling #loopedfunctions
	- [x] Handler
		- [x] One time execution [[Client py#schedule(...)]]
		- [x] Loop back [[Client py#looped_every(...)]]
and more at [[Client py]].

___
# Get Started
## Install
-> Go to [[Examples#-1 Installation]]
## How it works

The package is organized around a main class : The [[Client py]]. It contain your app infos a mainloop and some decorator generators like `@schedule()` ([[Client py#scehdule(...)]]).

When you defined all your functions, you can start the #mainloop ([[Client py#run(...)]]) and see it working (normally :) ... ).

You can just try the module with [[__main__ py#Try masthon]]

## Handle the package
At [[Examples]] you can find examples which explain how to handle main features. To go deeper you can [[#Contact me]] or browse [[Client py]], [[Events py]], [[DataClasses py]], [[utils py]], [[Exceptions py]], [[__init__ py]] and so on.
___
# License

This package is under the GNU / General Public License version 3.
___
# Contribute
## How to

To contribute, just contact me, give me some of your programs, so I can choose people with basic python skills. or more.

## Contact me

| Platform         | Link                               | Pseudo / ID                        |
| ---------------- | ---------------------------------- | ---------------------------------- |
| *Mastodon*       | https://mastodon.social/@gator3000 | `@gator3000`                       |
| *Mail*           |                                    | org.literie.gator@h3110.aleeas.com |
| *Discord*        | https://discord.com                | `_gator3000`                       |
| *Discord server* | https://discord.gg/2CVuXXTUVr      | `.gg//2CVuXXTUVr`                  |
