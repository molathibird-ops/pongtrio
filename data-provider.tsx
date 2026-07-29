'use client'

// ★ 이 파일은 사이트 프로젝트의 components/data-provider.tsx 를 대체합니다.
//   (수정본) 바뀐 부분:
//   1) DATA_BASE 에 blob prefix('/pongtrio') 를 포함시켰습니다.
//      blob_sync.py 가 'pongtrio/challenges.json' 위치에 올리므로
//      사이트도 반드시 같은 경로에서 읽어야 합니다. (이게 빠져서 404 → {} 였음)
//   2) DATA_BASE 를 환경변수 NEXT_PUBLIC_DATA_BASE 로도 덮어쓸 수 있게 했습니다.
//   3) fetch URL 에 캐시버스팅(?t=...)을 붙여 항상 최신 JSON 을 받습니다.

import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { DATA_FILES, setRawData } from '@/lib/bot-data'

// JSON 이 있는 곳. 봇이 Vercel Blob 에 올린 공개 URL(+prefix)을 가리킵니다.
// Vercel 프로젝트 환경변수에 아래처럼 설정하는 걸 권장합니다(하드코딩 대신):
//   NEXT_PUBLIC_DATA_BASE=https://pkmcwz3xe8crd9qu.public.blob.vercel-storage.com/pongtrio
// 설정이 없으면 아래 기본값(=prefix 포함)을 사용합니다.
const DATA_BASE = (
  process.env.NEXT_PUBLIC_DATA_BASE ||
  'https://pkmcwz3xe8crd9qu.public.blob.vercel-storage.com/pongtrio'
).replace(/\/+$/, '') // 끝의 슬래시 제거

// 실시간 자동 새로고침 주기(ms). 0 이면 자동 새로고침 끔.
// 환경변수 NEXT_PUBLIC_DATA_POLL_MS 로 조절 가능 (기본 15초).
const POLL_MS = Number(process.env.NEXT_PUBLIC_DATA_POLL_MS ?? '15000')

type DataState = {
  ready: boolean
  error: string | null
  reload: () => void
  // 데이터가 갱신될 때마다 증가. 컴포넌트가 이 값을 구독하면 자동 리렌더됨.
  version: number
}

const DataContext = createContext<DataState | null>(null)

export function DataProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [nonce, setNonce] = useState(0)
  const [version, setVersion] = useState(0)

  const reload = useCallback(() => {
    setReady(false)
    setError(null)
    setNonce((n) => n + 1)
  }, [])

  // 최초 로드 + 수동 reload() 시 실행 (로딩 표시 O)
  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        const bust = Date.now()
        const entries = await Promise.all(
          DATA_FILES.map(async (file) => {
            try {
              const res = await fetch(`${DATA_BASE}/${file}?t=${bust}`, {
                cache: 'no-store',
              })
              if (!res.ok) return [file, {}] as const
              return [file, await res.json()] as const
            } catch {
              return [file, {}] as const
            }
          }),
        )
        if (cancelled) return
        const bundle: Record<string, any> = {}
        for (const [file, data] of entries) bundle[file] = data
        setRawData(bundle)
        setVersion((v) => v + 1)
        setReady(true)
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : String(e))
      }
    }

    load()
    return () => {
      cancelled = true
    }
  }, [nonce])

  // 실시간 자동 새로고침: 주기적으로 조용히 데이터만 갱신 (로딩 표시 X → 깜빡임 없음)
  useEffect(() => {
    if (!POLL_MS || POLL_MS <= 0) return

    let cancelled = false

    async function silentRefresh() {
      try {
        const bust = Date.now()
        const entries = await Promise.all(
          DATA_FILES.map(async (file) => {
            try {
              const res = await fetch(`${DATA_BASE}/${file}?t=${bust}`, {
                cache: 'no-store',
              })
              if (!res.ok) return [file, {}] as const
              return [file, await res.json()] as const
            } catch {
              return [file, {}] as const
            }
          }),
        )
        if (cancelled) return
        const bundle: Record<string, any> = {}
        for (const [file, data] of entries) bundle[file] = data
        setRawData(bundle)
        setVersion((v) => v + 1)
      } catch {
        // 폴링 실패는 조용히 무시 (다음 주기에 재시도)
      }
    }

    const id = setInterval(silentRefresh, POLL_MS)
    // 탭이 다시 활성화되면 즉시 한 번 갱신
    const onVisible = () => {
      if (document.visibilityState === 'visible') silentRefresh()
    }
    document.addEventListener('visibilitychange', onVisible)

    return () => {
      cancelled = true
      clearInterval(id)
      document.removeEventListener('visibilitychange', onVisible)
    }
  }, [])

  return (
    <DataContext.Provider value={{ ready, error, reload, version }}>{children}</DataContext.Provider>
  )
}

export function useData(): DataState {
  const ctx = useContext(DataContext)
  if (!ctx) throw new Error('useData must be used within DataProvider')
  return ctx
}

export function useDataReady(): boolean {
  return useData().ready
}

// 데이터 버전. 이 값이 바뀌면 데이터가 갱신된 것.
// 자동 새로고침을 확실히 반영하고 싶은 컴포넌트에서 useDataVersion() 을 호출하면
// 새 데이터가 올 때마다 자동으로 리렌더됩니다.
export function useDataVersion(): number {
  return useData().version
}
