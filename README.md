# Masthon

A simple API for linking mastodon to your python codes.

#Author : org.literie.gator

#LastVersion : 0.2 beta

#FormatedDocumentation : at [Documentation on Gitlab Pages](https://Gator3000.gitlab.io/masthon)

# Features
- Masthon engine
	- [x] main loop
	- [ ] asynchronous
- Server Interactions
	- [x] Make a request to your server
	- Statuses
	    - [x] Post
	    - [x] Delete
	    - [ ] Get home timeline
	    - [x] Upload a file
	- Timelines
		- Home & Tags
			- [ ] Get timeline
		- Notifications
		    - [x] Get unread notification count
		    - [x] Get last received notifications
		-  Markers
		    - [x] Post
		    - [x] Get
- Event managing
	- [x] Handler
		- [x] unread notification
		- [x] new mention
		- [ ] new post in timeline
			- [ ] home
			- [ ] account
			- [ ] tag
- CLI interface
	- [x] Handler
		- [x] some defaults commands
		- [x] create new command
- Scheduling
	- [x] Handler
		- [x] One time execution
		- [x] Loop back

## How it works

The package is organized around a main class : The [[Client]]. It contain your app infos a mainloop and some decorator generators like `@schedule()` ([[Client#schedule(...)|Client.schedule()]]).

When you defined all your functions, you can start the #mainloop ([[Client#run(...)|Client.run()]]) and see it working (normally :) ... ).

# License

This package is under The GNU / General Public License version 3.

# Contribute
## How to

To contribute, just contact me, give me some of your programs, so I can choose people with basic python skills. or more.

## Contact me

| Platform   | Link                               | Pseudo / ID                        |
| ---------- | ---------------------------------- | ---------------------------------- |
| *Mastodon* | https://mastodon.social/@gator3000 | @gator3000                         |
| *Mail*     | -------------------                | org.literie.gator@h3110.aleeas.com |
| *Discord*  | https://discord.com                | \_gator3000                        |
