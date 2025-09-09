'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface YearlyFollowerChartProps {
  data: Array<{
    month: string
    followers: number
    following: number
  }>
}

function formatMonth(monthStr: string): string {
  const parts = monthStr.split('-')
  return `${parts[0]}/${parts[1]}`
}

export function YearlyFollowerChart({ data }: YearlyFollowerChartProps) {
  // グラフ用にデータを整形
  const chartData = data.map(item => ({
    month: formatMonth(item.month),
    フォロワー数: item.followers,
    フォロー数: item.following
  }))

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
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
            domain={[0, 800]} // フォロワー数に合わせた範囲
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
          <Line 
            type="monotone" 
            dataKey="フォロワー数" 
            stroke="#8884d8" 
            strokeWidth={2}
            dot={{ fill: '#8884d8', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: '#8884d8', strokeWidth: 2 }}
          />
          <Line 
            type="monotone" 
            dataKey="フォロー数" 
            stroke="#82ca9d" 
            strokeWidth={2}
            dot={{ fill: '#82ca9d', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: '#82ca9d', strokeWidth: 2 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}