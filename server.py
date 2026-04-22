# server.py - Update server
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class OTAHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ota/version.txt':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'1.2.3')  # Current version
            
        elif self.path.startswith('/ota/filesystem_v'):
            # Serve the update file
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.send_response(404)
            
    def log_message(self, format, *args):
        # Disable logging
        pass

# Create server
server = HTTPServer(('0.0.0.0', 8000), OTAHandler)
print("OTA Server running on port 8000")
server.serve_forever()