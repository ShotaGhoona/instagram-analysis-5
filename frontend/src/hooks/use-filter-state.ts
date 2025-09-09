'use client'

import { useState, useEffect, useMemo } from 'react'
import { DateRange } from 'react-day-picker'
import { MediaPost, MediaType } from '@/lib/types'
import { apiClient } from '@/lib/api'

export function useFilterState(accountId: string) {
  const [dateRange, setDateRange] = useState<DateRange | undefined>()
  const [mediaTypes, setMediaTypes] = useState<MediaType[]>([])
  const [posts, setPosts] = useState<MediaPost[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // API呼び出しでフィルタリング済みデータを取得
  const fetchFilteredPosts = async () => {
    if (!accountId) return
    
    setLoading(true)
    setError(null)
    
    try {
      const params: any = {}
      
      if (dateRange?.from) {
        params.start_date = dateRange.from.toISOString().split('T')[0]
      }
      if (dateRange?.to) {
        params.end_date = dateRange.to.toISOString().split('T')[0]
      }
      if (mediaTypes.length > 0) {
        params.media_type = mediaTypes
      }
      
      // APIからデータ取得
      const result = await apiClient.getPostsAnalytics(accountId, params)
      setPosts(result as MediaPost[])
      
    } catch (err) {
      console.error('Failed to fetch posts:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch posts')
      setPosts([])
    } finally {
      setLoading(false)
    }
  }

  // 初回読み込み
  useEffect(() => {
    fetchFilteredPosts()
  }, [accountId])

  // フィルター変更時の自動再取得
  useEffect(() => {
    if (accountId) {
      fetchFilteredPosts()
    }
  }, [dateRange, mediaTypes, accountId])

  // フィルター状態をリセット
  const resetFilters = () => {
    setDateRange(undefined)
    setMediaTypes([])
  }

  // フィルター適用中かどうか
  const hasActiveFilters = useMemo(() => {
    return (dateRange?.from || dateRange?.to) || mediaTypes.length > 0
  }, [dateRange, mediaTypes])

  // フィルター結果の統計（mockデータとの互換性のため）
  const filterStats = useMemo(() => {
    return {
      total: posts.length, // APIから取得したデータ数
      filtered: posts.length, // フィルタリング済み
      hidden: 0 // APIレベルでフィルタリング済みなので隠れているものはなし
    }
  }, [posts.length])

  return {
    // 状態
    dateRange,
    mediaTypes,
    filteredPosts: posts, // API取得データ
    loading,
    error,
    
    // 統計
    filterStats,
    hasActiveFilters,
    
    // アクション
    setDateRange,
    setMediaTypes,
    resetFilters,
    refetch: fetchFilteredPosts
  }
}