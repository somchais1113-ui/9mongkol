#!/bin/bash
# Starts the real FastAPI application (with persistent SQLite storage).
set -e
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo 'ไม่พบ Python 3 กรุณาติดตั้ง Python 3 ก่อนใช้งาน'
  read -r -p 'กด Enter เพื่อปิดหน้าต่าง...'
  exit 1
fi
if [ ! -d .venv ]; then
  echo 'ครั้งแรก: กำลังเตรียม Python environment...'
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install -q -r requirements.txt
PORT="${PORT:-8000}"
python -m uvicorn app.main:app --host 127.0.0.1 --port "$PORT" &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT
python - "$PORT" <<'PY'
import socket,sys,time
port=int(sys.argv[1])
for _ in range(60):
    try:
        with socket.create_connection(('127.0.0.1',port),timeout=.2):
            sys.exit(0)
    except OSError:
        time.sleep(.2)
print('ไม่สามารถเชื่อมต่อเว็บเซิร์ฟเวอร์ได้')
sys.exit(1)
PY
open "http://127.0.0.1:${PORT}"
echo "9 มงคล v0.7 เปิดที่ http://127.0.0.1:${PORT}"
echo 'ปิด Terminal หน้าต่างนี้เพื่อหยุดเซิร์ฟเวอร์'
wait "$SERVER_PID"
