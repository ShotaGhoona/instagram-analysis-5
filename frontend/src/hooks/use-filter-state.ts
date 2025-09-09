'use client'

import { useState, useMemo } from 'react'
import { DateRange } from 'react-day-picker'
import { MediaPost, MediaType } from '@/lib/types'
import { isDateInRange } from '@/lib/utils'

interface FilterState {
  dateRange: DateRange | undefined
  mediaTypes: MediaType[]
}

export function useFilterState(initialPosts: MediaPost[]) {
  const [dateRange, setDateRange] = useState<DateRange | undefined>()
  const [mediaTypes, setMediaTypes] = useState<MediaType[]>([])

  // フィルタリング済みのデータを計算
  const filteredPosts = useMemo(() => {
    return initialPosts.filter(post => {
      // 日付フィルター
      if (dateRange?.from || dateRange?.to) {
        const postDate = new Date(post.timestamp)
        
        if (dateRange.from && postDate < dateRange.from) {
          return false
        }
        if (dateRange.to) {
          // 終了日は当日を含むため、翌日の開始時刻と比較
          const endOfDay = new Date(dateRange.to)
          endOfDay.setHours(23, 59, 59, 999)
          if (postDate > endOfDay) {
            return false
          }
        }
      }
      
      // メディアタイプフィルター（空配列の場合は全て表示）
      if (mediaTypes.length > 0) {
        if (!mediaTypes.includes(post.media_type)) {
          return false
        }
      }
      
      return true
    })
  }, [initialPosts, dateRange, mediaTypes])

  // フィルター状態をリセット
  const resetFilters = () => {
    setDateRange(undefined)
    setMediaTypes([])
  }

  // フィルター適用中かどうか
  const hasActiveFilters = useMemo(() => {
    return (dateRange?.from || dateRange?.to) || mediaTypes.length > 0
  }, [dateRange, mediaTypes])

  // フィルター結果の統計
  const filterStats = useMemo(() => {
    return {
      total: initialPosts.length,
      filtered: filteredPosts.length,
      hidden: initialPosts.length - filteredPosts.length
    }
  }, [initialPosts.length, filteredPosts.length])

  return {
    // 状態
    dateRange,
    mediaTypes,
    filteredPosts,
    
    // 統計
    filterStats,
    hasActiveFilters,
    
    // アクション
    setDateRange,
    setMediaTypes,
    resetFilters
  }
}