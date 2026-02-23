
import http.server
import socketserver

HOST = "127.0.0.1"
PORT = 8080


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Petición recibida: {self.path}")

        # Contenido HTML de respuesta
        html = f"""
        <html>
        <head>
            <title>Servidor Local</title>
        </head>
        <body>
            <h1>Servidor funcionando correctamente</h1>
            <p>Ruta solicitada: {self.path}</p>
            <p>Esta página fue servida por tu propio servidor Python.</p>
            <p>Si estás viendo esto a través del proxy → ¡FUNCIONA!</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html.encode())))
        self.end_headers()

        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        return  # Evita spam en consola


def main():
    with socketserver.TCPServer((HOST, PORT), CustomHandler) as httpd:
        print(f"Servidor web local activo en: http://{HOST}:{PORT}")
        print("Presiona CTRL+C para detenerlo\n")
        httpd.serve_forever()


if __name__ == "__main__":
    main()