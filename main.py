import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ===== CEK IP & CLOUDFLARE =====
def cek_ip():
    print('========== CEK IP & CLOUDFLARE ==========\n')

    # 1. Cek IP
    try:
        ip = requests.get('https://api.ipify.org').text
        print(f'🌐 IP Render kamu: {ip}\n')
    except:
        print('❌ Gagal cek IP\n')
        ip = 'Tidak diketahui'

    # 2. Tes Discord API
    print('📡 Tes koneksi ke Discord...')
    try:
        r = requests.get(
            'https://discord.com/api/v10/gateway',
            timeout=10
        )
        status = r.status_code
        server = r.headers.get('server', '?')
        cf_ray = r.headers.get('cf-ray', '?')

        print(f'   Status : {status}')
        print(f'   Server : {server}')
        print(f'   CF-Ray : {cf_ray}')

        if status == 200:
            hasil = '✅ IP AMAN! Bot bisa jalan normal'
        elif status == 403:
            hasil = '❌ IP KENA BAN CLOUDFLARE! Pindah hosting!'
        elif status == 429:
            hasil = '⚠️ Rate limited, coba lagi nanti'
        else:
            hasil = f'❓ Status tidak dikenal: {status}'

    except Exception as e:
        hasil = f'💀 GAGAL TOTAL: {e}'

    print(f'\n{hasil}')
    print('==========================================\n')

    return ip, hasil


# ===== WEB SERVER (biar Render gak matiin) =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ip, hasil = cek_ip()

        response = f"""
        <html>
        <head><title>Discord IP Checker</title></head>
        <body style="font-family: Arial; padding: 40px; background: #1a1a2e; color: white;">
            <h1>🔍 Discord IP Checker</h1>
            <hr>
            <h2>🌐 IP Render: {ip}</h2>
            <h2>📡 Hasil: {hasil}</h2>
            <hr>
            <p>Refresh halaman untuk cek ulang</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode())

    # Biar gak spam log
    def log_message(self, format, *args):
        return


def run_server():
    port = 10000
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'🌐 Web server jalan di port {port}')
    server.serve_forever()


# ===== MAIN =====
if __name__ == '__main__':
    print('\n🚀 Starting Discord IP Checker...\n')

    # Cek pertama kali
    cek_ip()

    # Jalanin web server (wajib biar Render gak stop)
    run_server()
