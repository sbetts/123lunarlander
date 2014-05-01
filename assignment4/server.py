from network import Listener, Handler, poll
import sys
 
handlers = {} # map client handler to user name
 
class MyHandler(Handler):
     
    def on_open(self):
        self._username = ''
        pass
         
    def on_close(self):
        del handlers[self._username]
        for x in handlers:
                handlers[x].do_send({'left': self._username})
        pass
     
    def on_msg(self, msg):
        if msg.has_key('join'):
            self._username = msg['join']
            handlers[msg['join']] = self
            list_of_users = []
            for x in handlers:
                list_of_users.append(x)
            msg['users'] = list_of_users
            for x in handlers:
                handlers[x].do_send(msg)
        if msg.has_key('txt'):
            for x in handlers:
                handlers[x].do_send(msg)
 

port = 8888
server = Listener(port, MyHandler)
while 1:
    try:
        poll(timeout=0.05) # in seconds
    except KeyboardInterrupt:
        sys.exit()

