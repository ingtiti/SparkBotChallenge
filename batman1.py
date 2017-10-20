from itty import *
import urllib2
import json
import sys

def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,headers={"Accept" : "application/json","Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents

def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json", "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    return contents


@post('/')
def index(request):
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    /batman    - replies to the room with text
    /batcave   - echoes the incoming text to the room
    /batsignal - replies to the room with an image
    """
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if 'estado del cajero' in in_message or "cajero" in in_message or "estado" in in_message:
            msg = "Elija la zona:"
            msj = "1. Pachuca /n 2. Mineral del Monte /n 3. CDMX"
        elif '1' in in_message:
            msg = "Porque Beto hizo todo esto: https://sites.google.com/view/beto-top-pse"
        elif 'batcave' in in_message:
            message = result.get('text').split('batcave')[1].strip(" ")
            if len(message) > 0:
                msg = "The Batcave echoes, '{0}'".format(message)
            else:
                msg = "The Batcave is silent..."
        elif 'batsignal' in in_message:
            print "NANA NANA NANA NANA"
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bat_signal})
        if msg != None:
            print msg
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
    return "true"

####CHANGE THESE VALUES#####
bot_email = "bank_security@sparkbot.io"
bot_name = "bank_security"
bearer = "YWM0Y2Q4Y2YtNTkxYS00ZDVmLTk0MWYtOGIzMWRhNzMwYjNhNjg5ODQwMTItODNk"
bat_signal  = "https://i2.wp.com/www.diariobitcoin.com/wp-content/uploads/2014/05/lamassu-bitcoin-atm-3c.png"
run_itty(server='wsgiref', host='107.170.197.112', port=10010)
