# flag_server.py

import http.server
import socketserver

# 플래그 문구를 여기에 적어둡니다.
FLAG = "flag{llm_xss_success}"

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    1) /flag 경로로 GET 요청이 오면 FLAG을 반환하고
    2) 기본적으로 모든 응답에 CORS 헤더(Accept all Origin)를 붙여준다.
    """
    def end_headers(self):
        # CORS 헤더를 넣어 줌으로써 브라우저 fetch() 시 차단을 방지
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        # "/flag" 경로가 요청되면 플래그를 순수 텍스트 형태로 돌려준다.
        if self.path == "/flag":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(FLAG.encode())
        else:
            # 그 외 경로는 404 처리
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    # 5001번 포트에서 대기하도록 설정 (원하는 번호로 바꿔도 됩니다)
    PORT = 5001

    # TCPServer를 통해 HTTP 서버를 실행
    with socketserver.TCPServer(("localhost", PORT), CORSRequestHandler) as httpd:
        print(f"✅ Flag server running at http://localhost:{PORT}/flag")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ 서버를 종료합니다.")
            httpd.server_close()
