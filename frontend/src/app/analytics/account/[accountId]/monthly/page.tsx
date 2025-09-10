'use client'

import { use } from 'react'
import { MonthlyTable } from '@/components/analytics/monthly-table'
import { MonthlyCharts } from '@/components/analytics/monthly-charts'
import { useMonthlyAnalytics } from '@/hooks/use-monthly-analytics'
import { MonthlyPageSkeleton, ErrorDisplay, NoDataDisplay } from '@/components/ui/loading-skeleton'

interface MonthlyAnalyticsPageProps {
  params: Promise<{ accountId: string }>
}

export default function MonthlyAnalyticsPage({ params }: MonthlyAnalyticsPageProps) {
  const resolvedParams = use(params)
  
  // デフォルト年月設定（テスト用固定値）
  const year = 2025
  const month = 3
  
  const { data, loading, error, refetch } = useMonthlyAnalytics(resolvedParams.accountId, year, month)

  if (loading) return <MonthlyPageSkeleton />
  if (error) return <ErrorDisplay error={error} onRetry={refetch} />
  if (!data || !data.daily_stats.length) return <NoDataDisplay />

  // データをグラフ用に変換
  const chartData = data.daily_stats.map(stat => ({
    date: new Date(stat.date).getDate().toString(), // 日付を日のみに変換
    new_followers: stat.new_followers,
    reach: stat.reach,
    profile_views: stat.profile_views,
    website_clicks: stat.website_clicks
  }))
  
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">月間 Instagram データ</h1>
        <p className="text-gray-600">{data.month}</p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2">
        {/* 左：日別データテーブル */}
        <div className="bg-white rounded-lg shadow border p-6">
          <MonthlyTable data={data} />
        </div>
        
        {/* 右：4つの推移グラフ */}
        <div>
          <h3 className="text-lg font-semibold mb-4">グラフエリア</h3>
          <MonthlyCharts data={chartData} />
        </div>
      </div>
    </div>
  )
}