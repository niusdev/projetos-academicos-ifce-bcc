# servidor.py
# Inicia um servidor HTTP local (necessário porque visualizacao.html usa
# fetch() para ler resultado_genetico.json, e fetch não funciona com file://)
# e abre a página de visualização automaticamente no navegador padrão.

import http.server
import socketserver
import threading
import webbrowser
import os


def iniciar_visualizacao(porta: int = 8080,
                          pasta: str = None,
                          arquivo: str = "index.html") -> None:
    """
    Sobe um servidor HTTP simples servindo a pasta do projeto e abre
    o navegador na página de visualização.

    O servidor roda em uma thread separada e continua ativo enquanto
    o processo principal estiver vivo. Pressione Ctrl+C no terminal
    para encerrar.
    """
    if pasta is None:
        pasta = os.path.dirname(os.path.abspath(__file__))

    os.chdir(pasta)

    handler = http.server.SimpleHTTPRequestHandler

    # allow_reuse_address evita erro "Address already in use" em reinícios rápidos
    class Servidor(socketserver.TCPServer):
        allow_reuse_address = True

    httpd = Servidor(("", porta), handler)

    url = f"http://localhost:{porta}/{arquivo}"

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    print(f"\n  Servidor rodando em http://localhost:{porta}")
    print(f"  Abrindo visualização: {url}")
    print("  Pressione Ctrl+C para encerrar o servidor.\n")

    webbrowser.open(url)

    try:
        while True:
            input()  # mantém o processo principal vivo até Ctrl+C
    except KeyboardInterrupt:
        print("\n  Encerrando servidor...")
        httpd.shutdown()
