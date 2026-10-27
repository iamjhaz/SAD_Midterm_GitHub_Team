from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import html

items = []

class LostFoundServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.show_page()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode("utf-8")
        form = parse_qs(data)

        name = form.get("name", [""])[0].strip()
        item_type = form.get("type", ["Lost"])[0]
        location = form.get("location", [""])[0].strip()

        if name and location and item_type in ["Lost", "Found"]:
            items.append({
                "name": name,
                "type": item_type,
                "location": location
            })

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def show_page(self):
        item_cards = ""

        for item in items:
            item_cards += f"""
            <div class="card">
                <h3>{html.escape(item['name'])}</h3>
                <p>Type: {html.escape(item['type'])}</p>
                <p>Location: {html.escape(item['location'])}</p>
            </div>
            """

        if not item_cards:
            item_cards = "<p>No items reported yet.</p>"

        page = f"""
        <!-- Member 2 and Member 3 add their code here -->
        """

        content = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


server = HTTPServer(("127.0.0.1", 8000), LostFoundServer)

print("Lost and Found Management System is running!")
print("Open http://127.0.0.1:8000 in your browser.")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Server stopped.")
    server.server_close()