from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os

TEMPLATES_DIR = "templates"

class ShopHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Отдаём нужную страницу, а всё остальное → contacts.html."""
        routes = {
            "/": "index.html",
            "/index": "index.html",
            "/catalog": "catalog.html",
            "/category": "category.html",
            "/contacts": "contacts.html",
        }
        filename = routes.get(self.path, "contacts.html")
        self.serve_html(filename)

    def do_POST(self):
        """Принимаем POST и печатаем данные."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed = parse_qs(post_data)
        print("=" * 40)
        print("📨 POST-данные:")
        for key, value in parsed.items():
            print(f"  {key}: {value[0]}")
        print("=" * 40)
        
        self.send_response(302)
        self.send_header('Location', '/contacts')
        self.end_headers()

    def serve_html(self, filename):
        filepath = os.path.join(TEMPLATES_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

if __name__ == "__main__":
    print(" Сервер запущен на http://localhost:8000")
    print("📄 Доступные страницы: / , /catalog , /category , /contacts")
    HTTPServer(('', 8000), ShopHandler).serve_forever()
