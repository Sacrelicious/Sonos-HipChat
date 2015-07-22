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

zone = SoCo(settings['SONOS_IP_ADDRESS'])
hipchat = HypChat(settings['HIP_CHAT_AUTH_TOKEN'])
hipChatRoomName = settings['HIP_CHAT_ROOM']

hipChatRoom = None
currentTrackInfo = None

needToQuit = False

##list all available hipchat rooms
for room in hipchat.rooms()['items']:
    print room['name']
    if(room['name'] == hipChatRoomName):
        hipChatRoom = room
print 'joined room: ' + hipChatRoom['name']


while not needToQuit:
    try:
        newTrackInfo = zone.get_current_track_info()
##        only procede if the player is playing
        if zone.get_current_transport_info()['current_transport_state'] == 'PLAYING':
##              if the current track exists and is different from the last we found procede
            if(currentTrackInfo == None or newTrackInfo['title'] != currentTrackInfo['title']):
                searchStr = unicode(newTrackInfo['title']) +' ' + unicode(newTrackInfo['artist']) + ' ' +unicode(newTrackInfo['album'])
                searchStr = searchStr.replace(' ','+')
                print searchStr
                noteStr = '<a href="http://www.google.com/search?q='+searchStr + '">'
                if(currentTrackInfo == None or newTrackInfo['album'] != currentTrackInfo['album']):
                    noteStr += '<img style="float:left; width:50px;height:50px;" src="' + unicode(newTrackInfo['album_art'])+ '">'
                noteStr += '<p >'
                noteStr += '<b>' + unicode(newTrackInfo['title']) + '</b>'
                noteStr += ' - <b>' + unicode(newTrackInfo['artist'])+ '</b>'
                noteStr +=' - <b>' + unicode(newTrackInfo['album'])+ '</b>'
                noteStr += '</p></a>'
        ##        hipChatRoom.topic( 'Title: ' + unicode(newTrackInfo['title']) + ' Artist: ' + unicode(newTrackInfo['artist']) + ' Album: ' + unicode(newTrackInfo['album']))
                hipChatRoom.message( noteStr)
                print unicode(newTrackInfo)
                
                currentTrackInfo = newTrackInfo
    except Exception as e:
##        keep the bot alive even if there is a problem
        hipChatRoom.message( 'A problem occurred while trying to get the track info!' )
        print 'An exception occurred!!!'
        print type(e)
        print e.args
        print e
    time.sleep(5)


