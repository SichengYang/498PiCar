from http.server import BaseHTTPRequestHandler, HTTPServer
import json

hostName = "ec2-16-171-177-100.eu-north-1.compute.amazonaws.com"
serverPort = 498

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "json")
        self.end_headers()
        result = '{ "type":"position", "x":30, "y":20}'
        self.wfile.write(result)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")