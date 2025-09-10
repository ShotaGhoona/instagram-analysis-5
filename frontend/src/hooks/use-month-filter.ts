'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

export function useMonthFilter() {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  // デフォルト値：先月
  const now = new Date()
  const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1)
  const defaultYear = lastMonth.getFullYear()
  const defaultMonth = lastMonth.getMonth() + 1
  
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
  
  const [selectedMonth, setSelectedMonth] = useState(() => {
    const monthParam = searchParams.get('month')
    if (monthParam) {
      const month = parseInt(monthParam)
      if (month >= 1 && month <= 12) {
        return month
      }
    }
    return defaultMonth
  })
  
  // URL 同期
  const updateURL = (year: number, month: number) => {
    const params = new URLSearchParams()
    params.set('year', year.toString())
    params.set('month', month.toString())
    router.push(`?${params.toString()}`, { scroll: false })
  }
  
  // 年変更ハンドラ
  const handleYearChange = (year: number) => {
    if (year >= 2020 && year <= 2030) {
      setSelectedYear(year)
      updateURL(year, selectedMonth)
    }
  }
  
  // 月変更ハンドラ
  const handleMonthChange = (month: number) => {
    if (month >= 1 && month <= 12) {
      setSelectedMonth(month)
      updateURL(selectedYear, month)
    }
  }
  
  return {
    selectedYear,
    selectedMonth,
    handleYearChange,
    handleMonthChange
  }
}