import json
import asyncore, socket

class connection_handler(asyncore.dispatcher_with_send):
	
	def __init__(self, sock, handlers):
		asyncore.dispatcher_with_send.__init__(self, sock)
		self.handlers = handlers
	
	def handle_read(self):
		data = self.recv(100000)
		if data:
			data_struct = json.loads(data)
			event = data_struct['event']
			params = data_struct['params']
			state = data_struct['state']
			if self.handlers[event]:
				self.handlers[event](state, params)

class communicator(asyncore.dispatcher):

	handlers = {}
	
	def __init__(self, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)
	
	#private network handling function
	def handle_accept(self):
		pair = self.accept()

		if pair is None:
			pass
		else:
			sock, addr = pair
			print 'Incoming connection from %s' % repr(addr)
			handler = connection_handler(sock, "text")
			
	#Add a handler for the event of:
	#	map_data - the map data which is sent at the start of a game
	#	place_armies - placing new armies at the start of a turn
	#	take_turn - making a move, either attack, reinforce (ends turn) or end turn
	#	status_update - an updated state of the map, no response is needed
	def add_handler(self, event, function):
		handlers[event] = function

def loop():
	asyncore.loop()

class 
