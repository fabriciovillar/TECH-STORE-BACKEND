import json
from http.server import BaseHTTPRequestHandler, HTTPServer

CATALOGO_CELULARES = [
    {"id": 1, "marca": "Samsung", "modelo": "Galaxy S24 Ultra", "almacenamiento": "256GB", "precio": 1199.00, "stock": 8},
    {"id": 2, "marca": "Apple", "modelo": "iPhone 15 Pro", "almacenamiento": "128GB", "precio": 999.00, "stock": 5},
    {"id": 3, "marca": "Xiaomi", "modelo": "Redmi Note 13 Pro", "almacenamiento": "256GB", "precio": 320.00, "stock": 15},
    {"id": 4, "marca": "Motorola", "modelo": "Edge 50 Fusion", "almacenamiento": "256GB", "precio": 380.00, "stock": 10}
]

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        if self.path == "/celulares":
            self._set_headers(200)
            self.wfile.write(json.dumps(CATALOGO_CELULARES).encode("utf-8"))
        else:
            self._set_headers(200)
            self.wfile.write(b'{"tienda": "TECH-STORE Celulares", "estado": "activo"}')

    def do_POST(self):
        if self.path == "/celulares":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            datos = json.loads(body.decode("utf-8"))

            nuevo_celular = {
                "id": len(CATALOGO_CELULARES) + 1,
                "marca": datos["marca"],
                "modelo": datos["modelo"],
                "almacenamiento": datos["almacenamiento"],
                "precio": float(datos["precio"]),
                "stock": int(datos["stock"])
            }
            CATALOGO_CELULARES.append(nuevo_celular)

            self._set_headers(201)
            self.wfile.write(json.dumps(nuevo_celular).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), Handler)
    server.serve_forever()