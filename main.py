import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# ===== CEK IP & CLOUDFLARE =====
def cek_ip():
    print('========== CEK IP & CLOUDFLARE ==========\n', flush=True)

    # 1. Cek IP
    try:
        ip = requests.get('https://api.ipify.org', timeout=10).text
        print(f'🌐 IP Render kamu: {ip}\n', flush=True)
    except Exception as e:
        print(f'❌ Gagal cek IP: {e}\n', flush=True)
        ip = 'Tidak diketahui'

    # 2. Tes Discord API
    print('📡 Tes koneksi ke Discord...', flush=True)
    try:
        r = requests.get(
            'https://discord.com/api/v10/gateway',
            timeout=10
        )
        status = r.status_code
        server = r.headers.get('server', '?')
        cf_ray = r.headers.get('cf-ray', '?')

        print(f'   Status : {status}', flush=True)
        print(f'   Server : {server}', flush=True)
        print(f'   CF-Ray : {cf_ray}', flush=True)

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

    print(f'\n{hasil}', flush=True)
    print('==========================================\n', flush=True)

    return ip, hasil


# ===== WEB SERVER =====
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ip, hasil = cek_ip()

        # Tentuin warna berdasarkan hasil
        if '✅' in hasil:
            warna = '#00ff00'
            emoji = '✅'
        elif '❌' in hasil:
            warna = '#ff0000'
            emoji = '❌'
        else:
            warna = '#ffaa00'
            emoji = '⚠️'

        response = f"""
        <html>
        <head>
            <title>Discord IP Checker</title>
            <meta charset="utf-8">
        </head>
        <body style="font-family: Arial; padding: 40px; background: #1a1a2e; color: white; text-align: center;">
            <h1>🔍 Discord IP Checker</h1>
            <hr style="border-color: #333;">
            <h2>🌐 IP Render: <span style="color: #00d4ff;">{ip}</span></h2>
            <h2 style="color: {warna};">{emoji} {hasil}</h2>
            <hr style="border-color: #333;">
            <p style="color: #888;">Refresh halaman untuk cek ulang</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode())

    def log_message(self, format, *args):
        return


def run_server():
    port = 10000
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'🌐 Web server jalan di port {port}', flush=True)
    server.serve_forever()


# ===== MAIN =====
if __name__ == '__main__':
    print('\n🚀 Starting Discord IP Checker...\n', flush=True)

    # Cek pertama kali saat start
    cek_ip()

    # Jalanin web server
    run_server()
