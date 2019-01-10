# Lunch Bot
In my company, we usually eat lunch together, but these day our team have been growing up, so it's little hard to find the place which all of us eat lunch together.

So we need to split us into 2 teams, but it is so hard to decide the way split us, so I developed this slack bot to divide us into 2 temas by programmatically.

## Getting Start
First, you need to create your Slack App on your workspace, webhook to send request from bot server and add event listener which catch events from the workspace.

Then open `.env.sample` file, put your app's signning screet, webhook url and channel id which you want to get events from.
``` inside .env.sample
SLACK_SIGNING_SECRET=PUT_YOUR_SIGNING_SECRET
CHANNEL_WEB_HOOK_URL=PUT_TOUR_WEB_HOOK_URL
CHANNEL_ID=PUT_YOUR_CHANNEL_ID
```
and chang file name from `.env.sample` to `.env`
## Built with
* [Slack Events Api sdk](https://github.com/slackapi/python-slack-events-api) - to get add emoji events from workspace.
* [Flask](http://flask.pocoo.org/) - to open https port on the bot server.
* [Apscheduler](https://apscheduler.readthedocs.io/en/latest/index.html) - add scheduler that do jobs on a specific time using multi thread.
* [Requests](http://docs.python-requests.org/en/master/) - to send rest api request to slack workspace
