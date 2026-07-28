# -*- coding: utf-8 -*-
"""
pongtrio JSON -> Vercel Blob 실시간 동기화 모듈.

봇(bot.py)이 로컬에 쓰는 JSON 파일들을 감시하다가, 내용이 바뀌면
자동으로 Vercel Blob(공개 저장소)에 같은 이름으로 덮어써 올립니다.
사이트(Vercel에 배포)는 이 공개 URL을 그대로 fetch 해서 실시간으로 읽습니다.

★ 이 방식의 장점
────────────────────────────────────────────────────────────
- 봇의 수십 개 "저장 함수"를 하나도 고칠 필요가 없습니다.
  이 모듈은 파일의 수정시각(mtime)만 감시해서 바뀐 것만 올립니다.
- weirdhost에서는 봇만 돌리면 되고, 웹서버/도메인이 전혀 필요 없습니다.
  (weirdhost는 원래 봇 호스팅이라 외부 접속 도메인이 없어서 흰 화면이 떴던 것)

★ 필요한 것
────────────────────────────────────────────────────────────
1) pip install: vercel_blob        (requirements.txt 참고)
2) 환경변수  BLOB_READ_WRITE_TOKEN  (Vercel 프로젝트 > Storage > Blob 에서 발급)
   weirdhost의 "환경변수(Startup Variables)"에 이 토큰을 넣어주세요.

★ 사용법 (app.py 런처에서 자동 호출됨)
────────────────────────────────────────────────────────────
    from blob_sync import start_blob_sync
    start_blob_sync()   # 백그라운드 스레드로 감시 시작
"""

import json
import os
import threading
import time
import traceback

try:
    import vercel_blob
except Exception:  # 아직 설치 전이면 실행 시점에 안내
    vercel_blob = None


# ── 설정 ─────────────────────────────────────────────────────
# 봇 JSON이 있는 폴더 (기본: 현재 폴더)
DATA_DIR = os.path.abspath(os.environ.get("DATA_DIR", "."))

# Blob 안에서 사용할 폴더(prefix). 사이트의 NEXT_PUBLIC_DATA_BASE 끝부분과 일치.
BLOB_PREFIX = os.environ.get("BLOB_PREFIX", "pongtrio").strip("/")

# 파일이 바뀌었는지 확인하는 주기(초).
POLL_SECONDS = float(os.environ.get("BLOB_SYNC_POLL", "2"))

# 토큰
# weirdhost 환경변수 이름을 뭘로 넣었든(BLOB_READ_WRITE_TOKEN 이든 BLOB_TOKEN 이든)
# 둘 다 인식합니다. 코드에 토큰을 직접 박지 말고 환경변수에 넣어주세요(보안).
BLOB_TOKEN = (
    os.environ.get("vercel_blob_rw_pKMCWZ3Xe8crD9qU_e0l4EHqQcYWtIYVj01HSEXe9FVnYJ9")
    or os.environ.get("vercel_blob_rw_pKMCWZ3Xe8crD9qU_e0l4EHqQcYWtIYVj01HSEXe9FVnYJ9")
    or ""
).strip()

# 패키지가 내부에서 os.environ['BLOB_READ_WRITE_TOKEN'] 을 읽는 경로도 있으므로
# 어떤 이름으로 넣었든 항상 표준 이름으로 맞춰줍니다.
if BLOB_TOKEN:
    os.environ["BLOB_READ_WRITE_TOKEN"] = BLOB_TOKEN

# 사이트가 읽는 JSON 파일 목록 (app.py 의 DATA_FILES 와 반드시 동일)
DATA_FILES = [
    "challenges.json",
    "clears.json",
    "leaderboard.json",
    "users.json",
    "achievements.json",
    "achievement_times.json",
    "packs.json",
    "challenge_submissions.json",
    "checkins.json",
    "bets.json",
    "coupons.json",
    "daily_clears.json",
]


def _upload(name: str, body: bytes) -> str | None:
    """JSON 하나를 Blob 에 덮어쓰기 업로드. 성공 시 공개 URL 반환."""
    pathname = f"{BLOB_PREFIX}/{name}" if BLOB_PREFIX else name
    resp = vercel_blob.put(
        pathname,
        body,
        {
            # 파일명 뒤에 랜덤값을 붙이지 않음 → URL 이 항상 고정
            "addRandomSuffix": "false",
            # 같은 이름 덮어쓰기 허용 (실시간 갱신의 핵심).
            # 이걸 켜지 않으면 두 번째 업로드부터 "이미 존재" 에러가 납니다.
            "allowOverwrite": "true",
            # CDN 캐시를 짧게 (사이트는 추가로 캐시버스팅도 함)
            "cacheControlMaxAge": "0",
            # 토큰(옵션으로 넘기면 패키지가 우선 사용). 위에서 환경변수도 맞춰둠.
            "token": BLOB_TOKEN,
        },
    )
    # 파일명이 .json 이라 contentType 은 패키지가 자동으로 application/json 으로 인식합니다.
    return (resp or {}).get("url")


def _read_valid_json(path: str) -> bytes | None:
    """파일을 읽되, JSON 이 깨진 상태(쓰는 도중)면 None 을 돌려 다음 주기에 재시도."""
    try:
        with open(path, "rb") as f:
            body = f.read()
        json.loads(body.decode("utf-8"))  # 유효성 확인
        return body
    except Exception:
        return None


def _sync_loop():
    if vercel_blob is None:
        print("[blob] ❌ vercel_blob 패키지가 없습니다.  pip install vercel_blob  (requirements.txt)")
        return
    if not BLOB_TOKEN:
        # 진단: 어떤 변수가 실제로 보이는지 마스킹해서 출력 (원인 파악용)
        def _mask(name: str) -> str:
            raw = os.environ.get(name)
            if raw is None:
                return "<정의 안 됨>"
            raw = raw.strip()
            if raw == "":
                return "<빈 값(칸만 존재)>"
            return f"<값 있음: {raw[:14]}… 길이 {len(raw)}>"

        print("[blob] ❌ 토큰을 찾지 못했습니다. 아래 진단을 확인하세요:")
        print(f"[blob]   BLOB_READ_WRITE_TOKEN = {_mask('BLOB_READ_WRITE_TOKEN')}")
        print(f"[blob]   BLOB_TOKEN            = {_mask('BLOB_TOKEN')}")
        print("[blob]   → 위 둘 중 하나에 vercel_blob_rw_ 로 시작하는 실제 토큰이 들어가야 합니다.")
        print("[blob]   → '빈 값(칸만 존재)' 이면 그 칸에 실제 토큰 문자열을 채워주세요.")
        return

    print(f"[blob] 동기화 시작 — 폴더={DATA_DIR}  prefix='{BLOB_PREFIX}'  주기={POLL_SECONDS}s")

    # 파일별 마지막으로 올린 (mtime, size) 기억 → 바뀐 것만 업로드
    last: dict[str, tuple[float, int]] = {}
    base_printed = False

    while True:
        for name in DATA_FILES:
            path = os.path.join(DATA_DIR, name)
            if not os.path.isfile(path):
                continue
            try:
                st = os.stat(path)
                sig = (st.st_mtime, st.st_size)
            except OSError:
                continue

            if last.get(name) == sig:
                continue  # 변화 없음

            body = _read_valid_json(path)
            if body is None:
                continue  # 아직 쓰는 중 → 다음 주기 재시도

            try:
                url = _upload(name, body)
                last[name] = sig
                if url and not base_printed:
                    base = url.rsplit("/", 1)[0]
                    print("[blob] ────────────────────────────────────────────")
                    print(f"[blob] ★ 사이트 환경변수에 넣을 값 (NEXT_PUBLIC_DATA_BASE):")
                    print(f"[blob]   {base}")
                    print("[blob] ────────────────────────────────────────────")
                    base_printed = True
                print(f"[blob] ↑ 업로드: {name}  ({len(body)} bytes)")
            except Exception:
                print(f"[blob] ⚠ 업로드 실패: {name}")
                traceback.print_exc()

        time.sleep(POLL_SECONDS)


def start_blob_sync() -> threading.Thread:
    """백그라운드(데몬) 스레드로 동기화를 시작하고 스레드를 반환."""
    t = threading.Thread(target=_sync_loop, name="blob-sync", daemon=True)
    t.start()
    return t


if __name__ == "__main__":
    # 단독 실행 시: 한 번 감시 루프를 그냥 메인에서 돌림 (테스트용)
    _sync_loop()
