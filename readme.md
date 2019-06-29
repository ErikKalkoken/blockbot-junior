# blockbot junior
This is a simple bot for Slack. It's function is to create additional announcement style channels on Slack of both public and private channels.
This is achieved by automatically deleting posts from unauthorized users in such channels and informing the user about it.

The architecture of this bot is kept simple so it can run in a serverless environment.

Each instance is supposed to run in one Slack workspace only.

## Installation

Adding slack tokens as secrets
```
$ now secrets add slack_access_token "xoxp-TOKEN"
$ now secrets add slack_bot_token "xoxb-TOKEN"
```