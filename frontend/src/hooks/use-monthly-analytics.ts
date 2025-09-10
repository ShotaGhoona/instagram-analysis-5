'use client'

import { useState, useEffect } from 'react'
import { MonthlyAnalytics } from '@/lib/types'
import { apiClient } from '@/lib/api'

export function useMonthlyAnalytics(accountId: string, year: number, month: number) {
  const [data, setData] = useState<MonthlyAnalytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    if (!accountId || !year || !month) return
    
    setLoading(true)
    setError(null)
    
    try {
      const result = await apiClient.getMonthlyAnalytics(accountId, year, month)
      setData(result as MonthlyAnalytics)
    } catch (err) {
      if (err instanceof Error && err.message.includes('400')) {
        setError('無効な年月が指定されました')
      } else if (err instanceof Error && err.message.includes('404')) {
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
  }, [accountId, year, month])

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