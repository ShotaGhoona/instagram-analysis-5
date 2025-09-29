'use client'

import { use } from 'react'
import { YearlyTable } from '@/components/analytics/yearly-table'
import { YearlyFollowerChart } from '@/components/analytics/yearly-follower-chart'
import { YearlyEngagementChart } from '@/components/analytics/yearly-engagement-chart'
import { YearFilter } from '@/components/analytics/year-filter'
import { useYearlyAnalytics } from '@/hooks/use-yearly-analytics'
import { useYearFilter } from '@/hooks/use-year-filter'
import { YearlyPageSkeleton, ErrorDisplay, NoDataDisplay } from '@/components/ui/loading-skeleton'

interface YearlyAnalyticsPageProps {
  params: Promise<{ accountId: string }>
}

export default function YearlyAnalyticsPage({ params }: YearlyAnalyticsPageProps) {
  const resolvedParams = use(params)
  
  // フィルター状態管理
  const { selectedYear, handleYearChange } = useYearFilter()
  
  const { data, loading, error, refetch } = useYearlyAnalytics(resolvedParams.accountId, selectedYear)

  if (loading) return <YearlyPageSkeleton />
  if (error) return <ErrorDisplay error={error} onRetry={refetch} />
  if (!data || !data.monthly_stats.length) {
    const resetToCurrentYear = () => {
      const currentYear = new Date().getFullYear()
      handleYearChange(currentYear)
    }
    return <NoDataDisplay onClearFilters={resetToCurrentYear} />
  }

  // データをグラフ用に変換
  const followerData = data.monthly_stats.map(stat => ({
    month: stat.month,
    followers: stat.followers_count,
    following: Math.max(0, stat.follows_count) // 負数の場合は0に
  }))

  const engagementData = data.monthly_stats.map(stat => ({
    month: stat.month,
    いいね: stat.total_likes,
    コメント: stat.total_comments,
    シェア: stat.total_shares,
    保存: stat.total_saved
  }))
  
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">年間Instagramデータ</h1>
        <YearFilter 
          selectedYear={selectedYear}
          onYearChange={handleYearChange}
        />
      </div>
      
      {/* 月別データテーブル */}
      <div className="bg-white rounded-lg shadow border p-6 mb-6">
        <YearlyTable data={data} />
      </div>

      {/* フォロワー推移とエンゲージメント分析グラフ */}
      <div className="grid gap-6 md:grid-cols-2">
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">フォロワー推移</h2>
          <YearlyFollowerChart data={followerData} />
        </div>
        
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">エンゲージメント分析</h2>
          <YearlyEngagementChart data={engagementData} />
        </div>
      </div>
    </div>
  )
}