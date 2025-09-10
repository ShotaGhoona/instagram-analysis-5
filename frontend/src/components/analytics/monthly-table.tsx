'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { MonthlyAnalytics } from '@/lib/types'
import { formatNumber } from '@/lib/utils'

interface MonthlyTableProps {
  data: MonthlyAnalytics
}

function formatDayDate(dateStr: string): string {
  const date = new Date(dateStr)
  return `${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`
}

export function MonthlyTable({ data }: MonthlyTableProps) {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">日別データテーブル</h3>
      <div className="rounded-md border max-h-[500px] overflow-y-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[80px]">日付</TableHead>
              <TableHead className="text-right w-[70px]">投稿</TableHead>
              <TableHead className="text-right w-[100px]">新規フォロワー</TableHead>
              <TableHead className="text-right w-[80px]">リーチ</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.daily_stats.map((stat) => (
              <TableRow key={stat.date}>
                <TableCell className="font-medium">
                  {formatDayDate(stat.date)}
                </TableCell>
                <TableCell className="text-right">
                  {stat.posts_count}
                </TableCell>
                <TableCell className="text-right">
                  {stat.new_followers > 0 ? '+' : ''}{formatNumber(stat.new_followers)}
                </TableCell>
                <TableCell className="text-right">
                  {formatNumber(stat.reach)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="text-sm text-gray-500 text-center">
        ページ: 1-{data.daily_stats.length}/{data.daily_stats.length} &nbsp; &lt; &gt;
      </div>
    </div>
  )
}