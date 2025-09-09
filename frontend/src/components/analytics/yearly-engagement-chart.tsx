'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface YearlyEngagementChartProps {
  data: Array<{
    month: string
    いいね: number
    コメント: number
    シェア: number
    保存: number
  }>
}

function formatMonth(monthStr: string): string {
  const parts = monthStr.split('-')
  return `${parts[0]}/${parts[1]}`
}

export function YearlyEngagementChart({ data }: YearlyEngagementChartProps) {
  // グラフ用にデータを整形
  const chartData = data.map(item => ({
    month: formatMonth(item.month),
    いいね: item.いいね,
    コメント: item.コメント,
    シェア: item.シェア,
    保存: item.保存
  }))

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis 
            dataKey="month" 
            tick={{ fontSize: 12 }}
            stroke="#666"
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            stroke="#666"
            domain={[0, 120]} // ASCIIデザインに合わせた範囲（最大105+余裕）
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #ccc',
              borderRadius: '8px',
              fontSize: '14px'
            }}
          />
          <Legend 
            wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }}
          />
          <Bar 
            dataKey="いいね" 
            stackId="engagement"
            fill="#8884d8" 
          />
          <Bar 
            dataKey="コメント" 
            stackId="engagement"
            fill="#82ca9d" 
          />
          <Bar 
            dataKey="シェア" 
            stackId="engagement"
            fill="#ffc658" 
          />
          <Bar 
            dataKey="保存" 
            stackId="engagement"
            fill="#ff7300" 
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}