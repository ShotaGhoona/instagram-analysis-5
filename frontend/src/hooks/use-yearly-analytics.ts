'use client'

import { useState, useEffect } from 'react'
import { YearlyAnalytics } from '@/lib/types'
import { apiClient } from '@/lib/api'

export function useYearlyAnalytics(accountId: string, year?: number) {
  const [data, setData] = useState<YearlyAnalytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    if (!accountId) return
    
    setLoading(true)
    setError(null)
    
    try {
      const result = await apiClient.getYearlyAnalytics(accountId, year)
      setData(result as YearlyAnalytics)
    } catch (err) {
      if (err instanceof Error && err.message.includes('404')) {
        setError('アカウントが見つかりません')
      } else if (err instanceof Error && err.message.includes('500')) {
        setError('データ取得に失敗しました')
      } else {
        setError('ネットワークエラーです')
      }
      setData(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [accountId, year])

  const refetch = () => {
    fetchData()
  }

  return {
    data,
    loading,
    error,
    refetch
  }
}