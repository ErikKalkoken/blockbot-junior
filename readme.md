# blockbot junior
This is a simple bot for Slack. It's function is to turn a channel into an announcement style channel, so that only certain users are able to post messages. It's design has been kept simple, so it can run on a basic serverless platform.

## What this bot does
This bot can turn any channel (public or private) into an announcement style channel, where only a subset of users are allowed to post and all other users are blocked. 

It works by automatically deleting posts from any user that is not authorized to post in a specific channel. Note that the user will not get any notification from the bot about the deletion. His/her messages will just vanish shortly after posting.

To keep things simple this bot is meant to be install for one workspace only, but it can establish multiple announcement channels if needed.


## Installation
In the following we explain how to install this bot to a Slack workspace.

### Requirements
In order to be able to install this bot the following is needed:
- User with admin account for your Slack workspace (this is mandatory)
- A [github](https://github.com/) account for forking this repo and storing the source code
- A [Zeit-Now](https://zeit.co/) account for hosting the bot

**Note:**
This bot will in principle run on any serverless platform and - when supplied with the needed additional infrastructure - also on standard web servers. We are using Now here only as example. Check out [this article](https://geekflare.com/serverless-computing-platform/) on Geek Flare for an overview of serverless platform providers.

### 1 - Create a Slack app
Create a new [Slack app](https://api.slack.com/start/overview). We will assume you called the app by its intended name, which is "blockbot-junior".

Make sure to add a short description. If you want you can also use the provided icon image as App Icon and define a color.

On the page "Bot Users" click on "Add a Bot User" to add a bot user. You can change the name, but we would recommend to leave it as "blockbot-junior".

On the page "OAuth & Permissions" add the additional scope `chat:write:users`.

Then click on "Install App" to install the app to your workspace. Make sure you install the app with an admin user.

Note that we will add events later.

### 2 - Fork this repo
Fork this repo to your own github. Make sure to connect the repo to your now account.

Note that now will report an deployment error this time, since you have not yet defined the required now secret. We will do that next.

### 3 - Add tokens 
You need to add three tokens for your app, which are all configured as environment variable and need to be stored in Now secrets.

- access token: Oauth Access Token on the Oauth & Permissions page under "Tokens for Your Workspace"
- bot token: Oauth Bot Token on the Oauth & Permissions page under "Tokens for Your Workspace"
- verification token: Verification Token on the Basic Information page under "App Credentials"

To store your token as Now secrets use the following commands in the Now CLI for the respective tokens:

```
$ now secrets add slack_access_token "xoxp-TOKEN"
$ now secrets add slack_bot_token "xoxb-TOKEN"
$ now secrets add slack_verification_token "TOKEN"
```

Make sure to re-deploy your app to now, e.g. with the `now` command in the CLI.

This time the deployment should be successful and your app should be running normally on the now platform.

### 4 - Adding slash command
Now that the app is running we can add the slash command.

Under "Slash Commands" click on "Create New Command" and set the parameter as follows:
- Command: `/blockbot-junior`
- Request URL: Is the alias to your Now server plus `/slash`, so something like `https://blockbot-junior.username.now.sh/slash`
- Short Description: `Show configuration of this channel`

Click on "Save" to commit your changes.

You will not be prompted to re-install the app. Please follow those instructions.

### 5 - Adding events
The next step is to add the events. For that open the app management page and go to "Event Subscriptions".

Activate the events by setting the switch to "On". 

Then add the alias for your now service as request URL. It should be something like `https://blockbot-junior.username.now.sh/events`. 

You should get a green "Verified" as result, which means that your service is responding correctly.

Next add the following events under "Subscribe to Bot Events":
- `message.channels`
- `message.groups`

Finally click on "Save Changes" to commit your events configuration.

### 6 - Configure authorized users
Now we want to tell the bot which users are allowed to post to announcement channels. 

For that we have two list that you both find in the file `config.py`:
- `ADMIN_USERS`: list of users that can see use the slash command to see the configuration for a channel and are allowed to post in any announcement type channel. This is a simple list of user IDs.
- `ALLOWED_CHANNEL_USERS`: list of users than can post in a specific announcement channel. This is a dictionary of channel IDs, which each contain a list of user IDs.


Example:
```
ADMIN_USERS = [
   "U123456XY",
   "U987654AB"
]

ALLOWED_CHANNEL_USERS = {
   "C123456XY": [
        "U123456XY",
        "U987654AB"
   ]
   
}
```
**Tip for getting user IDs**: To get the user ID of a specific user you can either call just call the API to get the list of all users with https://slack.com/api/users.list?token=TOKEN (just put your token from above in here and open the link with a browser) or if you are on the Slack Web client you can see the user ID e.g. by hovering over the name of a user. Your browser will then show the link to the user's profile which contains its ID.

**Tip for getting channel IDs**: If you use the Slack web client the easiest way to get the channel ID of a channel is go into that channel and then extract it from the URL. The URL looks something like this `https://workspace.slack.com/messages/C12345678/details/` where `C12345678` is the channel ID.

After you configured all users make sure to re-deploy your app to Now.

### 7 - Turn a channel into announcement mode
To activate the bot for a channel and turning it into announcement mode just add the bot user to any public or private channel. Once added the bot will be active and delete any unauthorized posts.

Example command on Slack:
```
/invite @blockbot-junior
```

To disable the bot for a channel and turn it back into a normal channel simply remove the bot user from that channel.

Example command on Slack:
```
/kick @blockbot-junior
```

# Support
If you need support or discover any errors feel free to raise an issue on this github.

# Licence
See licence file on this repo for details.