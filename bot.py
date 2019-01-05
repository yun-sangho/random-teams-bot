from flask import Flask
from slackeventsapi import SlackEventAdapter
from apscheduler.schedulers.background import BackgroundScheduler
from random import sample
import requests
import json
import os

# Set environment variable.
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
CHANNEL_WEB_HOOK_URL = os.environ['CHANNEL_WEB_HOOK_URL']
CHANNEL_ID = os.environ['CHANNEL_ID']

# Headers for API reqeust.
headers = {'content-type': 'application/json'}

# Array remembering which user add emoji reaction on the message.
persons = ['person1', 'person2', 'person3', 'person4', 'person5']

def createTeams(persons):
  temp = persons.copy()
  teams = {}
  team1 = sample(temp, len(persons) // 2)
  for person in team1:
    temp.remove(person)
  teams['team1'] = team1
  teams['team2'] = temp
  return teams
    
# Implement Scheduler
def sendQuestion():
  persons.clear()
  question = {'text': '<!channel>\n 안녕하세요! 점심 드실분은 이모지달아주세요!'}
  r = requests.post(CHANNEL_WEB_HOOK_URL, data=json.dumps(question), headers=headers)
  print(r)

def sendPairs():
  message = '오늘의 팀은!!!\n'
  
  if len(persons) <= 5:
    teams = ' '.join(persons)
    message = message + teams
  else:
    teams = createTeams(persons)
    team1 = '팀 1 '+ ' '.join(teams['team1']) + '\n'
    team2 = '팀 2 ' + ' '.join(teams['team2']) + '\n'
    message = message + team1 + team2
  
  payoff = {'text': message}
  r = requests.post(CHANNEL_WEB_HOOK_URL, data=json.dumps(payoff), headers=headers)
  print(r)

# Add jobs on the scheulers
sched = BackgroundScheduler()
sched.add_job(sendQuestion, 'cron', day_of_week='mon-fri', hour=11, minute=45,)
sched.add_job(sendPairs,  'cron', day_of_week='mon-fri', hour=12, minute=0,)
sched.start()

# Run Server
app = Flask(__name__)

# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, '/slack/events', app)

# Create an event listener for "reaction_added" events and
# If a user add emoji on the message on specific channel,
# put user's id in the persons Array.
@slack_events_adapter.on('reaction_added')
def reaction_added(event):
  user = '<@%s>' % event['event']['user']
  channel = event['event']['item']['channel']
  # Check the event occured in the specific channel that you wnat to get an evnet from
  if channel == CHANNEL_ID:
    if user not in persons:
      persons.append(user)
  print(persons)
  persons.clear()

# # Start the server on port 3000
if __name__ == '__main__':
  app.run(port=3000)