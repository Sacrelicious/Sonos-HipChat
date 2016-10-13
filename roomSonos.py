#!/usr/bin/env python
# -*- coding: utf-8 -*-
from soco import SoCo
import soco
import sys
import cgi
from hypchat import *
import time
import json
import logging

logging.basicConfig(filename='output.log',level=logging.DEBUG)

#print to output and to the log file
def printlog(a):
    logging.debug(a)
    print a

#load settings
f = open('config.txt','r')
settings = json.load(f)
f.close()

zone = SoCo(settings['SONOS_IP_ADDRESS'])
hipchat = HypChat(settings['HIP_CHAT_AUTH_TOKEN'])
hipChatRoomName = settings['HIP_CHAT_ROOM']
hipChatRoomId = settings['HIP_CHAT_ROOM_ID']

hipChatRoom = None
currentTrackInfo = None

needToQuit = False

##list all available hipchat rooms
##and connect to the one specified in config.txt
if hipChatRoomName:
    for room in hipchat.rooms()['items']:
        printlog(room['name'])
        if(room['name'] == hipChatRoomName):
            hipChatRoom = room
else:
    hipChatRoom = hipchat.get_room(hipChatRoomId)

printlog('joined room: ' + hipChatRoom['name'])

while not needToQuit:
    try:
        newTrackInfo = zone.get_current_track_info()
##        only procede if the player is playing
        if zone.get_current_transport_info()['current_transport_state'] == 'PLAYING':
##              if the current track exists and is different from the last we found procede
            if(currentTrackInfo == None or newTrackInfo['title'] != currentTrackInfo['title']):
                #format a cool hipchat message containing a search link an album image and the track info
                #put together a google search url
                searchStr = unicode(newTrackInfo['title']) +' ' + unicode(newTrackInfo['artist']) + ' ' +unicode(newTrackInfo['album'])
                searchStr = searchStr.replace(' ','+')
                printlog(searchStr)

                noteStr = '<a href="http://www.google.com/search?q='+searchStr + '">'
                #only include the album image if this track has a different album from the last one
                if(currentTrackInfo == None or newTrackInfo['album'] != currentTrackInfo['album']):
                    noteStr += '<img style="float:left; width:50px;height:50px;" src="' + unicode(newTrackInfo['album_art'])+ '">'
                noteStr += '<p >'
                noteStr += 'Now playing at ' + unicode(zone.player_name) + ': '
                noteStr += '<b>' + unicode(newTrackInfo['title']) + '</b>'
                noteStr += ' - <b>' + unicode(newTrackInfo['artist'])+ '</b>'
                noteStr +=' - <b>' + unicode(newTrackInfo['album'])+ '</b>'
                noteStr += '</p></a>'
        ##        hipChatRoom.topic( 'Title: ' + unicode(newTrackInfo['title']) + ' Artist: ' + unicode(newTrackInfo['artist']) + ' Album: ' + unicode(newTrackInfo['album']))
                #send the message to hipchat
                hipChatRoom.notification(noteStr)
                printlog(unicode(newTrackInfo))

                currentTrackInfo = newTrackInfo
    except Exception as e:
##        keep the bot alive even if there is a problem
        hipChatRoom.message( 'A problem occurred while trying to get the track info!' )
        printlog('An exception occurred!!!')
        printlog(type(e))
        printlog(e.args)
        printlog(e)

    #don't scan again for another 5 seconds
    time.sleep(5)
