'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

export function useYearFilter() {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  // デフォルト値：現在年
  const defaultYear = new Date().getFullYear()
  
  // URL パラメータから初期値を取得
  const [selectedYear, setSelectedYear] = useState(() => {
    const yearParam = searchParams.get('year')
    if (yearParam) {
      const year = parseInt(yearParam)
      if (year >= 2020 && year <= 2030) {
        return year
      }
    }
    return defaultYear
  })
  
  // URL 同期
  const updateURL = (year: number) => {
    const params = new URLSearchParams()
    params.set('year', year.toString())
    router.push(`?${params.toString()}`, { scroll: false })
  }
  
  // 年変更ハンドラ
  const handleYearChange = (year: number) => {
    if (year >= 2020 && year <= 2030) {
      setSelectedYear(year)
      updateURL(year)
    }
  }
  
  return {
    selectedYear,
    handleYearChange
  }
}