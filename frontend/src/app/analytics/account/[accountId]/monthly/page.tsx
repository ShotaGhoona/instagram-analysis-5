'use client'

import { use } from 'react'
import { MonthlyTable } from '@/components/analytics/monthly-table'
import { MonthlyCharts } from '@/components/analytics/monthly-charts'
import { MonthFilter } from '@/components/analytics/month-filter'
import { useMonthlyAnalytics } from '@/hooks/use-monthly-analytics'
import { useMonthFilter } from '@/hooks/use-month-filter'
import { MonthlyPageSkeleton, ErrorDisplay, NoDataDisplay } from '@/components/ui/loading-skeleton'

interface MonthlyAnalyticsPageProps {
  params: Promise<{ accountId: string }>
}

export default function MonthlyAnalyticsPage({ params }: MonthlyAnalyticsPageProps) {
  const resolvedParams = use(params)
  
  // フィルター状態管理
  const { selectedYear, selectedMonth, handleYearChange, handleMonthChange } = useMonthFilter()
  
  const { data, loading, error, refetch } = useMonthlyAnalytics(resolvedParams.accountId, selectedYear, selectedMonth)

  if (loading) return <MonthlyPageSkeleton />
  if (error) return <ErrorDisplay error={error} onRetry={refetch} />
  if (!data || !data.daily_stats.length) {
    const resetToCurrentMonth = () => {
      const now = new Date()
      const lastMonth = new Date(now.getFullYear(), now.getMonth() - 1)
      handleYearChange(lastMonth.getFullYear())
      handleMonthChange(lastMonth.getMonth() + 1)
    }
    return <NoDataDisplay onClearFilters={resetToCurrentMonth} />
  }

  // データをグラフ用に変換
  const chartData = data.daily_stats.map(stat => ({
    day: new Date(stat.date).getDate(), // 日付を日のみに変換
    date: new Date(stat.date).getDate().toString(),
    新規フォロワー: stat.new_followers,
    リーチ: stat.reach,
    プロフィールアクセス: stat.profile_views,
    ウェブサイトタップ: stat.website_clicks
  }))
  
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">月間 Instagram データ</h1>
        <div className="flex items-center gap-4">
          <MonthFilter 
            selectedYear={selectedYear}
            selectedMonth={selectedMonth}
            onYearChange={handleYearChange}
            onMonthChange={handleMonthChange}
          />
        </div>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2">
        {/* 左：日別データテーブル */}
        <div className="bg-white rounded-lg shadow border p-6">
          <MonthlyTable data={data} />
        </div>
        
        {/* 右：4つの推移グラフ */}
        <div className="">
          <MonthlyCharts data={chartData} />
        </div>
      </div>
    </div>
  )
}