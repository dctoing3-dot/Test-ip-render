import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

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

        # Cek berapa lama harus nunggu
        retry_after = r.headers.get('retry-after', '?')
        x_ratelimit = r.headers.get('x-ratelimit-reset-after', '?')

        print(f'   Status       : {status}', flush=True)
        print(f'   Server       : {server}', flush=True)
        print(f'   CF-Ray       : {cf_ray}', flush=True)
        print(f'   Retry-After  : {retry_after} detik', flush=True)
        print(f'   Rate Reset   : {x_ratelimit}', flush=True)

        if status == 200:
            hasil = '✅ IP AMAN! Bot bisa jalan normal'
            warna = '#00ff00'
        elif status == 403:
            hasil = '❌ IP KENA BAN CLOUDFLARE! Pindah hosting!'
            warna = '#ff0000'
        elif status == 429:
            hasil = f'⚠️ Rate limited! Tunggu {retry_after} detik. Tapi IP TIDAK DI-BAN!'
            warna = '#ffaa00'
        else:
            hasil = f'❓ Status tidak dikenal: {status}'
            warna = '#888888'

        # Cek body response
        try:
            body = r.json()
            print(f'   Body: {body}', flush=True)
        except:
            print(f'   Body: {r.text[:200]}', flush=True)

    except Exception as e:
        hasil = f'💀 GAGAL TOTAL: {e}'
        warna = '#ff0000'
        retry_after = '?'

    print(f'\n{hasil}', flush=True)
    print('==========================================\n', flush=True)

    return ip, hasil, warna


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ip, hasil, warna = cek_ip()

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
            <h2 style="color: {warna};">{hasil}</h2>
            <hr style="border-color: #333;">
            <h3>Penjelasan:</h3>
            <p>200 = ✅ IP Aman</p>
            <p>403 = ❌ IP Kena Ban Cloudflare</p>
            <p>429 = ⚠️ Rate Limited (BUKAN ban, cuma disuruh sabar)</p>
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


if __name__ == '__main__':
    print('\n🚀 Starting Discord IP Checker...\n', flush=True)
    cek_ip()
    run_server()
