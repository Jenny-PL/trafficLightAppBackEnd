# Traffic Light App (back end)
## Capstone Project for Ada Developers Academy, C17 
## Problem solved:  
- Many young kids (mine, specifically) can't tell time.  This app will allow them to know when they can get up in the morning (and let me sleep in longer).  We have a clock that does this at home, but it's rather bulky, so I'd like an app that we can pull up on a tablet to use if we're on vacation
- Additionally, older kids or adults who can't tell time may find a visual alarm helpful

## Features:
- Traffic light turns from red --> green when wake up time is reached
- The circular progress bar gives a visual of how much time is left, relative to when the alarm was set.
- There is an option to upload audio and play wake up music, in the case that the user must wake up at a certain time

## Features in production:
- Retrieve stored songs from the mongoDB database
- Have buttons that allow user to play music or audiobooks once the green light is on
- Make it a progressive web app

## Technology used:
- Typescript (front end) with React
- Heroku deployment, to make it available online
- Python with Flask (backend), with a MongoDB database (audio files stored as bson)
- See -trafficLightAppFrontEnd repo 