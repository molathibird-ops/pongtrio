# -*- coding: utf-8 -*-
"""
weirdhost용 런처 (신버전) — 디스코드 봇 + Vercel Blob 동기화.

★ 무엇이 바뀌었나
────────────────────────────────────────────────────────────
- 예전 app.py 는 "정적 사이트 웹서버 + 봇"을 함께 돌렸습니다.
  하지만 weirdhost 는 봇 호스팅이라 외부 접속용 도메인/포트가 없어서
  사이트가 흰 화면만 떴습니다 (There are no available domain...).
- 그래서 사이트는 Vercel 로 옮기고, weirdhost 는 "봇 + JSON 업로드"만
  담당합니다. 봇이 JSON 을 쓰면 blob_sync 가 자동으로 Vercel Blob 에
  올리고, Vercel 의 사이트가 그걸 실시간으로 읽습니다.

★ weirdhost 설정
────────────────────────────────────────────────────────────
1) 시작(startup) 명령:  python app.py
2) 환경변수(Startup Variables):
     BLOB_READ_WRITE_TOKEN = vercel_blob_rw_...   (Vercel Blob 토큰)
3) 업로드할 파일: app.py, bot.py, blob_sync.py, *.json, requirements.txt
   (out/ 정적 폴더는 이제 필요 없습니다 — 사이트는 Vercel 에 있음)

환경변수(선택):
   DATA_DIR         봇 JSON 폴더 (기본 현재 폴더 ".")
   BOT_FILE         함께 실행할 봇 파일 (기본 bot.py)
   BOT_RESTART      봇 크래시 후 재시작 대기 초 (기본 10, 0이면 재시작 안 함)
   BLOB_PREFIX      Blob 안 폴더명 (기본 "pongtrio")
   BLOB_SYNC_POLL   JSON 변경 확인 주기 초 (기본 2)
"""

import os
import runpy
import time
import traceback

from blob_sync import start_blob_sync

BOT_RESTART = int(os.environ.get("BOT_RESTART", "10"))


def _detect_bot_file() -> str:
    env = os.environ.get("BOT_FILE")
    if env:
        return env
    here = os.path.abspath(__file__)
    for name in ("bot.py", "app.py"):
        cand = os.path.abspath(name)
        if os.path.isfile(cand) and cand != here:  # 자기 자신(app.py)은 실행 안 함
            return name
    return "bot.py"


def main():
    # 1) JSON → Vercel Blob 동기화 (백그라운드 데몬 스레드)
    start_blob_sync()

    # 2) 봇은 메인에서 계속 실행 (죽으면 자동 재시작)
    bot_file = _detect_bot_file()
    bot_path = os.path.abspath(bot_file)
    if not os.path.isfile(bot_path):
        print(f"[launch] ❌ 봇 파일을 찾을 수 없습니다: {bot_file}")
        print("[launch]   그래도 Blob 동기화는 계속 돕니다. (Ctrl+C 로 종료)")
        while True:
            time.sleep(3600)

    while True:
        print(f"[launch] 봇 실행 → {bot_path}")
        try:
            runpy.run_path(bot_path, run_name="__main__")
            print("[launch] ⚠ 봇이 정상 종료되었습니다(예외 없음).")
        except SystemExit as e:
            print(f"[launch] ⚠ 봇이 sys.exit({e.code}) 로 종료되었습니다.")
        except Exception:
            print("[launch] ❌ 봇이 예외로 종료되었습니다. 트레이스백:")
            traceback.print_exc()

        if BOT_RESTART <= 0:
            print("[launch] BOT_RESTART=0 → 봇 재시작 안 함. (Blob 동기화는 계속 동작)")
            while True:
                time.sleep(3600)
        print(f"[launch] {BOT_RESTART}초 후 봇을 다시 시작합니다...")
        time.sleep(BOT_RESTART)


if __name__ == "__main__":
    main()