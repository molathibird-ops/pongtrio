'use client'

// ★ 이 파일은 사이트 프로젝트의 components/data-provider.tsx 를 대체합니다.
//   바뀐 부분은 fetch URL 에 캐시버스팅(?t=...)을 붙인 것뿐입니다.
//   Vercel Blob 공개 URL 은 CDN 캐시가 걸리므로, 매 요청마다 다른 쿼리를
//   붙여 항상 최신 JSON 을 받도록 합니다. (실시간 반영)

import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { DATA_FILES, setRawData } from '@/lib/bot-data'

// JSON 이 있는 곳. 이제 봇이 Vercel Blob 에 올린 공개 URL 을 가리킵니다.
// .env(.local) 또는 Vercel 프로젝트 환경변수에 아래처럼 설정하세요:
//   NEXT_PUBLIC_DATA_BASE=https://<스토어ID>.public.blob.vercel-storage.com/pongtrio
// (이 값은 weirdhost 에서 app.py 를 처음 실행하면 로그에 출력됩니다.)
const DATA_BASE = (process.env.NEXT_PUBLIC_DATA_BASE ?? '/data').replace(/\/$/, '')

type DataState = {
  ready: boolean
  error: string | null
  reload: () => void
}

const DataContext = createContext<DataState | null>(null)

export function DataProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [nonce, setNonce] = useState(0)

  const reload = useCallback(() => {
    setReady(false)
    setError(null)
    setNonce((n) => n + 1)
  }, [])

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        // 캐시버스팅용 토큰. reload 할 때마다 새 값이 되어 CDN 캐시를 우회.
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

  return (
    <DataContext.Provider value={{ ready, error, reload }}>{children}</DataContext.Provider>
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