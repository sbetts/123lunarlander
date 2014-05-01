from network import Handler, poll
import sys
from threading import Thread
from time import sleep


myname = raw_input('What is your name? ')
should_exit = False

class Client(Handler):
    
    def on_close(self):
        global should_exit
        should_exit = True
        
    def on_msg(self, msg):
        if msg.has_key('join'):
            users_string = ''
            for x in msg['users']:
                users_string += x + ', '
            print msg['join'] + ' has joined the chat. Users: ' + users_string
        if msg.has_key('txt'):
            if msg['speak'] != myname:
                print msg['speak'] + ': ' + msg['txt']
        if msg.has_key('left'):
            print msg['left'] + ' left the room.'
        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05) # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True # die when the main thread dies
thread.start()

while 1:
    try:
        mytxt = sys.stdin.readline().rstrip()
        if should_exit == True:
            print('**** Disconnected from server ****')
            sys.exit()
        if mytxt == 'quit':
            print('**** Disconnected from server ****')
            sys.exit()
        if mytxt != '':
            client.do_send({'speak': myname, 'txt': mytxt})
    except KeyboardInterrupt:
        sys.exit()
