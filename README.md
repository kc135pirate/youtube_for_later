# youtube_for_later
Send YouTube links, or other supported video sites, to your very own telegram bot and have some local media ready for consumption when you return to your home.

# Requirements
- Script was built for and assumes user is using Linux
- Requires youtube-dl to be installed.

# Setup
- Create a bot using [The Bot Father](https://core.telegram.org/bots#6-botfather) on Telegram.
- Copy the youtube_for_later.py file to the desired downloads folder.
- Mark the youtube_for_later.py file as executable.
- Run the script in your terminal and paste the bot token when prompted.
- Add script to chronjob.


# Additional Tweaks
- Edit line 98 with different option flags available in youtube-dl.
- Uncomment lines 101 through 103 if you want notifications of successful downloads.
