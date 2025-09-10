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
      <div className="">
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
                <TableCell className="font-medium py-1">
                  {formatDayDate(stat.date)}
                </TableCell>
                <TableCell className="text-right py-1">
                  {stat.posts_count}
                </TableCell>
                <TableCell className="text-right py-1">
                  {stat.new_followers > 0 ? '+' : ''}{formatNumber(stat.new_followers)}
                </TableCell>
                <TableCell className="text-right py-1">
                  {formatNumber(stat.reach)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
  )
}