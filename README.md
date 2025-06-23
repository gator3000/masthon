# Masthon

A simple API for linking mastodon to your python codes.

#Author : org.literie.gator

#LastVersion : 0.3 alpha

#FormatedDocumentation : at [Documentation on Gitlab Pages](https://Gator3000.gitlab.io/masthon)

# Features
- Masthon engine
	- [x] main loop -> #mainloop
	- [x] asynchronous (actually, threading) #threading
- Server Interactions
	- [x] Make a request to your server #RequestAPI
	- Statuses
	    - [x] Post
	    - [x] Delete
	    - [x] Upload a file
	- Users
		- [ ] Get user
	- Timelines
		- Home & Tags
			- [ ] Get timeline
		- Notifications #notifications 
		    - [x] Get unread notification count
		    - [x] Get last received notifications
		-  Markers #markers 
		    - [x] Post
		    - [x] Get
- Event managing
	- [x] Handler #events
		- [x] unread notification
		- [x] new mention
		- [ ] new post in timeline
			- [ ] home
			- [ ] account
			- [ ] tag
- CLI interface #CLI
	- [x] Handler
		- [x] some defaults commands
		- [x] create new command
- Scheduling #scheduling #loopedfunctions
	- [x] Handler
		- [x] One time execution
		- [x] Loop back

## How it works

The package is organized around a main class : The [[Client py]]. It contain your app infos a mainloop and some decorator generators like `@schedule()` ([[Client py#scehdule(...)]]).

When you defined all your functions, you can start the #mainloop ([[Client py#run(...)]]) and see it working (normally :) ... ).

### Get Started
At [[Examples]] you can find examples which explain how to handle main features. To go deeper you can [[#Contact me]] or browse [[Client py]], [[Events py]], [[DataClasses py]], [[utils py]], [[Exceptions py]], [[__init__ py]] and so on.

# License

This package is under the GNU / General Public License version 3.

# Contribute
## How to

To contribute, just contact me, give me some of your programs, so I can choose people with basic python skills. or more.

## Contact me

| Platform   | Link                               | Pseudo / ID                        |
| ---------- | ---------------------------------- | ---------------------------------- |
| *Mastodon* | https://mastodon.social/@gator3000 | `@gator3000`                       |
| *Mail*     |                                    | org.literie.gator@h3110.aleeas.com |
| *Discord*  | https://discord.com                | `_gator3000`                       |
