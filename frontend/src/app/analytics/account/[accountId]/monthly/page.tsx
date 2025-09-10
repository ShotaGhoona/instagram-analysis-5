import { use } from 'react'
import { MonthlyTable } from '@/components/analytics/monthly-table'
import { MonthlyCharts } from '@/components/analytics/monthly-charts'
import { mockMonthlyData, mockMonthlyChartData } from '@/lib/mock-data-monthly'

interface MonthlyAnalyticsPageProps {
  params: Promise<{ accountId: string }>
}

export default function MonthlyAnalyticsPage({ params }: MonthlyAnalyticsPageProps) {
  const resolvedParams = use(params)
  
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">月間 Instagram データ</h1>
        <p className="text-gray-600">2025/03/01 - 2025/03/31</p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2">
        {/* 左：日別データテーブル */}
        <div className="bg-white rounded-lg shadow border p-6">
          <MonthlyTable data={mockMonthlyData} />
        </div>
        
        {/* 右：4つの推移グラフ */}
        <div>
          <h3 className="text-lg font-semibold mb-4">グラフエリア</h3>
          <MonthlyCharts data={mockMonthlyChartData} />
        </div>
      </div>
    </div>
  )
}