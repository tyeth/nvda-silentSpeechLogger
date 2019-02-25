# NVDA Add-on: Speech History
# Copyright (C) 2012 Tyler Spivey
# Copyright (C) 2015-2017 James Scholes
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# See the file LICENSE for more details.

import addonHandler
import api
import globalPluginHandler
from queueHandler import eventQueue, queueFunction
import speech
import tones
import ui
import io
import logging
from logging import Logger

#from globalCommands import SCRCAT_SPEECH

addonHandler.initTranslation()

oldSpeak = speech.speak
oldSpeakSpelling = speech.speakSpelling
data = ''
history = []
history_pos = 0
path = 'C:\\Norland\\Logs\\NVDA\\'
log = logging.getLogger('Speech')

def append_to_history(string):
    global log
    log.info(string)

def appendSpelling_to_history(string):
    append_to_history("Spelt-Aloud:" + string)

def mySpeak(sequence, *args, **kwargs):
    global data
    text = u''.join([x for x in sequence if isinstance(x, basestring)])
    if text:
        data = text
        queueFunction(eventQueue, append_to_history, text)
        oldSpeak(text)

def mySpeakSpelling(text, *args, **kwargs):
    global data
    if text:
        data = text
        queueFunction(eventQueue, appendSpelling_to_history, text)
        oldSpeakSpelling(text)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        global oldSpeak, oldSpeakSpelling, log
        oldSpeak = speech.speak
        speech.speak = mySpeak
        oldSpeakSpelling = speech.speakSpelling
        speech.speakSpelling = mySpeakSpelling
        fh = logging.FileHandler(path + 'transcription.log');        fh.setLevel(logging.INFO)        log.addHandler(fh)

    def terminate(self):
        speech.speak = oldSpeak
        speech.speakSpelling = oldSpeakSpelling