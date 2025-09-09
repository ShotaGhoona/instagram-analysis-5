'use client'

import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'
import { MediaPost } from '@/lib/types'
import { calculateEngagementRate } from '@/lib/utils'

interface ChartDataPoint {
  date: string
  likes: number
  reach: number
  views: number
  engagementRate: number
}

interface PostsPerformanceChartProps {
  posts: MediaPost[]
}

export function PostsPerformanceChart({ posts }: PostsPerformanceChartProps) {
  // データを日付順にソートしてグラフ用に変換
  const chartData: ChartDataPoint[] = posts
    .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
    .map((post) => {
      const date = new Date(post.timestamp)
      const dateDisplay = `${date.getMonth() + 1}/${date.getDate()}`
      
      return {
        date: dateDisplay,
        likes: post.like_count,
        reach: post.reach || 0,
        views: post.views || 0,
        engagementRate: calculateEngagementRate(post)
      }
    })

  // カスタムツールチップ
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border rounded-lg shadow-lg">
          <p className="font-medium">{`投稿日: ${label}`}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} style={{ color: entry.color }}>
              {entry.name}: {entry.name === 'エンゲージメント率' ? `${entry.value}%` : entry.value.toLocaleString()}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart
          data={chartData}
          margin={{
            top: 20,
            right: 80,
            bottom: 20,
            left: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="date" 
            fontSize={12}
            tick={{ fill: '#666' }}
          />
          <YAxis 
            yAxisId="left"
            fontSize={12}
            tick={{ fill: '#666' }}
          />
          <YAxis 
            yAxisId="right" 
            orientation="right"
            fontSize={12}
            tick={{ fill: '#666' }}
            label={{ value: '%', position: 'outside', offset: 10 }}
          />
          
          {/* 棒グラフ */}
          <Bar 
            yAxisId="left" 
            dataKey="likes" 
            fill="#8884d8" 
            name="いいね"
            opacity={0.8}
          />
          <Bar 
            yAxisId="left" 
            dataKey="reach" 
            fill="#82ca9d" 
            name="リーチ"
            opacity={0.8}
          />
          <Bar 
            yAxisId="left" 
            dataKey="views" 
            fill="#ffc658" 
            name="視聴数"
            opacity={0.8}
          />
          
          {/* 線グラフ */}
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="engagementRate" 
            stroke="#ff7300" 
            strokeWidth={2}
            dot={{ fill: '#ff7300', strokeWidth: 2, r: 4 }}
            name="エンゲージメント率"
          />
          
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{
              paddingTop: '20px'
            }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}