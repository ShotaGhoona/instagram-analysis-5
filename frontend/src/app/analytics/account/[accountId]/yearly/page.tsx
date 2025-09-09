import { use } from 'react'
import { YearlyTable } from '@/components/analytics/yearly-table'
import { YearlyFollowerChart } from '@/components/analytics/yearly-follower-chart'
import { YearlyEngagementChart } from '@/components/analytics/yearly-engagement-chart'
import { mockYearlyData, mockFollowerData, mockEngagementData } from '@/lib/mock-data-yearly'

interface YearlyAnalyticsPageProps {
  params: Promise<{ accountId: string }>
}

export default function YearlyAnalyticsPage({ params }: YearlyAnalyticsPageProps) {
  const resolvedParams = use(params)
  
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">年間Instagramデータ</h1>
        <p className="text-gray-600">2022/01/01 - 2025/08/31</p>
      </div>
      
      {/* 月別データテーブル */}
      <div className="bg-white rounded-lg shadow border p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">月別データテーブル</h2>
        <YearlyTable data={mockYearlyData} />
      </div>

      {/* フォロワー推移とエンゲージメント分析グラフ */}
      <div className="grid gap-6 md:grid-cols-2">
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">フォロワー推移</h2>
          <YearlyFollowerChart data={mockFollowerData} />
        </div>
        
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">エンゲージメント分析</h2>
          <YearlyEngagementChart data={mockEngagementData} />
        </div>
      </div>
    </div>
  )
}