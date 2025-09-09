'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { YearlyAnalytics } from '@/lib/types'
import { formatNumber } from '@/lib/utils'

interface YearlyTableProps {
  data: YearlyAnalytics
}

function formatMonth(monthStr: string): string {
  const date = new Date(monthStr + '-01')
  return `${date.getFullYear()}年${date.getMonth() + 1}月`
}

export function YearlyTable({ data }: YearlyTableProps) {
  return (
    <div className="space-y-4">
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">月</TableHead>
              <TableHead className="text-right w-[80px]">フォロワー</TableHead>
              <TableHead className="text-right w-[100px]">新規フォロワー</TableHead>
              <TableHead className="text-right w-[120px]">プロフィールアクセス</TableHead>
              <TableHead className="text-right w-[100px]">ウェブサイト</TableHead>
              <TableHead className="text-right w-[70px]">いいね</TableHead>
              <TableHead className="text-right w-[70px]">コメント</TableHead>
              <TableHead className="text-right w-[70px]">シェア</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.monthly_stats.map((stat) => (
              <TableRow key={stat.month}>
                <TableCell className="font-medium">
                  {formatMonth(stat.month)}
                </TableCell>
                <TableCell className="text-right">
                  {formatNumber(stat.followers_count)}
                </TableCell>
                <TableCell className="text-right">
                  {stat.follows_count > 0 ? '+' : ''}{formatNumber(stat.follows_count)}
                </TableCell>
                <TableCell className="text-right">
                  {formatNumber(stat.profile_views)}
                </TableCell>
                <TableCell className="text-right">
                  {formatNumber(stat.website_clicks)}
                </TableCell>
                <TableCell className="text-right">
                  {formatNumber(stat.total_likes)}
                </TableCell>
                <TableCell className="text-right">
                  {formatNumber(stat.total_comments)}
                </TableCell>
                <TableCell className="text-right">
                  {formatNumber(stat.total_shares)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}