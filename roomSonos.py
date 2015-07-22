#!/usr/bin/env python
# -*- coding: utf-8 -*-
from soco import SoCo
import soco
import sys
from hypchat import *
import time
import json

#load settings
f = open('config.txt','r')
settings = json.load(f)
f.close()


AUTH_TOKEN = settings['HIP_CHAT_AUTH_TOKEN']
hipchat = HypChat(AUTH_TOKEN)

hipChatRoomName = settings['HIP_CHAT_ROOM']
hipChatRoom = None

zone = SoCo('10.102.52.156')

currentTrackInfo = None

needToQuit = False

##list all available hipchat rooms
for room in hipchat.rooms()['items']:
    print room['name']
    if(room['name'] == hipChatRoomName):
        hipChatRoom = room

print 'joining room: ' + hipChatRoom['name']


while not needToQuit:
    try:
        newTrackInfo = zone.get_current_track_info()
        if(currentTrackInfo == None or newTrackInfo['title'] != currentTrackInfo['title']):
            searchStr = unicode(newTrackInfo['title']) +' ' + unicode(newTrackInfo['artist']) + ' ' +unicode(newTrackInfo['album'])
            searchStr = searchStr.replace(' ','+')
            print searchStr
            noteStr = '<a href="http://www.google.com/search?q='+searchStr + '">'
            if(currentTrackInfo == None or newTrackInfo['album'] != currentTrackInfo['album']):
                noteStr += '<img style="float:left; width:50px;height:50px;" src="' + unicode(newTrackInfo['album_art'])+ '">'
            noteStr += '<p style="float:right">'
            noteStr += 'Title: <b>' + unicode(newTrackInfo['title']) + '</b><br>'
            noteStr += ' Artist: <b>' + unicode(newTrackInfo['artist'])+ '</b><br>'
            noteStr +=' Album: <b>' + unicode(newTrackInfo['album'])+ '</b>'
            noteStr += '</p></a>'
    ##        hipChatRoom.topic( 'Title: ' + unicode(newTrackInfo['title']) + ' Artist: ' + unicode(newTrackInfo['artist']) + ' Album: ' + unicode(newTrackInfo['album']))
            hipChatRoom.message( noteStr)
            print unicode(newTrackInfo)
            currentTrackInfo = newTrackInfo
    except Exception as e:
        # keep the bot alive even if there is a problem
        hipChatRoom.message( 'A problem occurred while trying to get the track info!' )
        print 'An exception occurred!!!'
        print type(e)
        print e.args
        print e
    time.sleep(5)


