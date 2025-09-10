'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface MonthlyChartsProps {
  data: Array<{
    day: number
    date: string
    新規フォロワー: number
    リーチ: number
    プロフィールアクセス: number
    ウェブサイトタップ: number
  }>
}

function ChartContainer({ title, children }: { title: string, children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-lg border p-4">
      <h4 className="font-medium mb-2 text-center">{title}</h4>
      <div className="h-[120px]">
        {children}
      </div>
    </div>
  )
}

export function MonthlyCharts({ data }: MonthlyChartsProps) {
  return (
    <div className="space-y-4">
      {/* 新規フォロワー数 */}
      <ChartContainer title="新規フォロワー数">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis 
              dataKey="day" 
              tick={{ fontSize: 10 }}
              stroke="#666"
              interval={2} // 表示する目盛りを間引き
            />
            <YAxis 
              tick={{ fontSize: 10 }}
              stroke="#666"
              domain={[-10, 20]} // 新規フォロワー用範囲
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="新規フォロワー" 
              stroke="#8884d8" 
              strokeWidth={2}
              dot={{ fill: '#8884d8', strokeWidth: 1, r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>

      {/* リーチ */}
      <ChartContainer title="リーチ">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis 
              dataKey="day" 
              tick={{ fontSize: 10 }}
              stroke="#666"
              interval={2}
            />
            <YAxis 
              tick={{ fontSize: 10 }}
              stroke="#666"
              domain={[0, 200]} // リーチ用範囲
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="リーチ" 
              stroke="#82ca9d" 
              strokeWidth={2}
              dot={{ fill: '#82ca9d', strokeWidth: 1, r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>

      {/* プロフィールアクセス */}
      <ChartContainer title="プロフィールのアクセス">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis 
              dataKey="day" 
              tick={{ fontSize: 10 }}
              stroke="#666"
              interval={2}
            />
            <YAxis 
              tick={{ fontSize: 10 }}
              stroke="#666"
              domain={[0, 20]} // プロフィールアクセス用範囲
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="プロフィールアクセス" 
              stroke="#ffc658" 
              strokeWidth={2}
              dot={{ fill: '#ffc658', strokeWidth: 1, r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>

      {/* ウェブサイトのタップ */}
      <ChartContainer title="ウェブサイトのタップ">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis 
              dataKey="day" 
              tick={{ fontSize: 10 }}
              stroke="#666"
              interval={2}
            />
            <YAxis 
              tick={{ fontSize: 10 }}
              stroke="#666"
              domain={[0, 2]} // ウェブサイトタップ用範囲
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'white',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="ウェブサイトタップ" 
              stroke="#ff7300" 
              strokeWidth={2}
              dot={{ fill: '#ff7300', strokeWidth: 1, r: 3 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>
    </div>
  )
}