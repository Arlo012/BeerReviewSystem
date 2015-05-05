'''
Method to add tab completion for beer input
Code based off pymotw.com/2/readline/
'''
import logging
import readline #include line in appropriate file

LOG_FILENAME = '/tmp/completer.log'
logging.basicConfig(filename = LOG_FILENAME, level = logging.DEBUG,)
beers = ['Budweiser', 'Blue Moon','Miller Lite', 'Pabst Blue Ribbon', 'Stella Artois', 'Coors Light', 'Bud Light', 'Magic Hat 9', 'River Horse Tripple Hops', 'Bud Ligth Lime', 'Samuel Adams Boston Lager', 'Dos Equis', 'Modelo', 'Medalla', 'Heineken', 'Bud Light Platinum', 'Corona', 'Corona Light', 'Corona Extra', 'Coronita'] #dummy data

class TabCompleter(object):
	def __init__(self, beers):
		self.beers = sorted(beers)
		return

	def complete(self, text, state):
		response = None
		if state == 0:
			if text:
				self.matches = [s 
								for s in self.beers
								if s and s.startswith(text)]
				logging.debug('%s matches: %s', repr(text), self.matches)
			else:
				self.matches = self.beers[:]
				logging.debug('(empty input) matches: %s', self.matches)

		try:
			response = self.matches[state]
		except IndexError:
			response = None
		logging.debug('complete(%s, %s_ => %s', repr(text), state, repr(response))
		return response

def input_loop(beers):
	line = ''
	while line != 'stop':
		line = raw_input('Enter you favorite beer: ')
		if line in beers:
			print line
		else:
			print 'Beer not found!'

readline.set_completer(TabCompleter(beers).complete) #include in appropriate file

readline.parse_and_bind('tab: complete') #include in appropriate file

input_loop(beers) #include in appropriate file
