from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            message = body.get("message", "").strip()

            if not message:
                self.send_error(400, "Message is required")
                return

            client = OpenAI(
                api_key=os.environ["OPENAI_API_KEY"]
            )

            response = client.responses.create(
                model="gpt-5.6-luna",
                input=message
            )

            answer = response.output_text

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({"answer": answer}).encode()
            )

        except Exception as error:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "error": "Server error"
                }).encode()
            )
