# -*- coding: utf-8 -*-
import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SoCo'))
print path
if not path in sys.path:
    sys.path.insert(1, path)
del path
import re, ConfigParser, soco
from twython import Twython, TwythonStreamer
from soco.plugins.spotify import Spotify, SpotifyTrack

# Available commands
commands = ['pause', 'play', 'next', 'prev']

class MyStreamer(TwythonStreamer):

    def set_device(self, soco_device):
        self.soco_device = soco_device
        self.spotify_plugin = Spotify(soco_device)

    def on_success(self, data):
        if 'text' in data and 'user' in data and 'screen_name' in data['user']:
            text = data['text'].encode('utf-8')
            text = self.strip_receiver(text)
            screen_name = data['user']['screen_name'].encode('utf-8')
            if (text in commands):
                self.do_command(text, screen_name)
            elif self.validate_format(text):
                print "Adding {0} to playlist".format(text)
                self.play_track(text)
            else:
                print "Unknown command or spotify uri format, text: {0}".format(text)

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

    def validate_format(self, spotify_uri):
        """ Example format: spotify:track:20DfkHC5grnKNJCzZQB6KC """
        return re.match(r"spotify\:track\:[A-z0-9]", spotify_uri)

    def strip_receiver(self, text):
        """ When sending tweet to a user the text becomes: @user text, this is to strip on the @user """
        return re.sub(r"\@[A-z0-9]+", "", text).strip()

    def play_track(self, uri):
        print self.spotify_plugin.add_track_to_queue(SpotifyTrack(uri))

    def do_command(self, cmd, screen_name):
        # Dessa borde endast få köras av vissa användare..
        print "Doing command " + cmd + " from " + screen_name
        if cmd == 'pause':
            self.soco_device.pause()
        elif cmd == 'play':
            self.soco_device.play()
        elif cmd == 'next':
            self.soco_device.next()
        elif cmd == 'prev':
            self.soco_device.prev()


def find_device(name):
    name = unicode(name, 'utf-8')
    for zone in soco.discover():
        if zone.player_name == name:
            return zone

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('./settings.cfg')
    device_name = config.get('General', 'sonos_device')
    device = find_device(device_name)

    if device == None:
        print "Couldn't find device with name {0}, terminating".format(device_name)
    else:
        follow_id = config.get('General', 'follow_user_id')
        print "Found device {0}, using this as victim".format(device)

        stream = MyStreamer(config.get('General', 'api_key'), config.get('General', 'api_secret'),
                        config.get('General', 'access_token'), config.get('General', 'access_token_secret'))
        stream.set_device(device)

        print "Stream starting.. following {0}".format(follow_id)
        stream.statuses.filter(follow=follow_id)
