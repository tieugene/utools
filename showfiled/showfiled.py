#!/usr/bin/env python3
"""Show file content on demand by HTTP."""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

FPATH: str


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if os.path.isfile(FPATH):  # TODO: handle 'access denied'
            self.send_response(200)
            self.send_header("Content-type", "text/plain")  # TODO: configure/detect mimetype
            self.end_headers()
            self.wfile.write(open(FPATH, 'rb').read())
        else:
            self.send_error(404)


def main():
    global FPATH
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_path> <port>")
        sys.exit(1)
    FPATH = sys.argv[1]
    httpd = HTTPServer(('', int(sys.argv[2])), HttpGetHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    main()
