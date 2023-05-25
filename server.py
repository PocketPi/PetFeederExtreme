import http.server
import socketserver
import sys
import signal


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/save_settings':

            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)

            post_data_str = post_data_bytes.decode("UTF-8")
            post_data_str = post_data_str.replace("=", ":")
            list_of_post_data = post_data_str.split('&')

            print(list_of_post_data)

        self.path = 'index.html'

        return super().do_GET()

# A custom signal handle to allow us to Ctrl-C out of the process


if __name__ == "__main__":
    def signal_handler(signal, frame):
        print('Exiting http server (Ctrl+C pressed)')
        try:
            if (handler_object):
                handler_object.server_close()
        finally:
            sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Create an object of the above class
    handler_object = Handler

    PORT = 8000

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler_object) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
