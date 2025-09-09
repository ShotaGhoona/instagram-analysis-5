'use client'

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { MediaPost } from '@/lib/types'
import { formatDate, calculateEngagementRate, formatNumber } from '@/lib/utils'
import { Thumbnail } from '@/components/ui/thumbnail'

interface PostsTableProps {
  posts: MediaPost[]
}

function getMediaTypeDisplay(mediaType: string): string {
  switch (mediaType) {
    case 'CAROUSEL_ALBUM':
      return 'カルーセル'
    case 'VIDEO':
      return '動画'
    case 'IMAGE':
      return '画像'
    default:
      return mediaType
  }
}

export function PostsTable({ posts }: PostsTableProps) {
  return (
    <div className="space-y-4">
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[80px]">投稿日</TableHead>
              <TableHead className="w-[60px]">サムネイル</TableHead>
              <TableHead className="w-[80px]">タイプ</TableHead>
              <TableHead className="text-right w-[70px]">リーチ</TableHead>
              <TableHead className="text-right w-[70px]">いいね</TableHead>
              <TableHead className="text-right w-[70px]">コメント</TableHead>
              <TableHead className="text-right w-[70px]">シェア</TableHead>
              <TableHead className="text-right w-[70px]">保存</TableHead>
              <TableHead className="text-right w-[80px]">EG率(%)</TableHead>
              <TableHead className="text-right w-[70px]">視聴数</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {posts.map((post) => {
              const engagementRate = calculateEngagementRate(post)
              const postDate = new Date(post.timestamp)
              const dateDisplay = `${postDate.getMonth() + 1}/${postDate.getDate()}`
              
              return (
                <TableRow key={post.ig_media_id}>
                  <TableCell className="font-medium">
                    {dateDisplay}
                  </TableCell>
                  <TableCell>
                    <Thumbnail 
                      src={post.media_type === 'VIDEO' ? post.thumbnail_url : post.media_url} 
                      alt={`投稿 ${dateDisplay}`}
                      size={48}
                    />
                  </TableCell>
                  <TableCell>
                    {getMediaTypeDisplay(post.media_type)}
                  </TableCell>
                  <TableCell className="text-right">
                    {formatNumber(post.reach || 0)}
                  </TableCell>
                  <TableCell className="text-right">
                    {formatNumber(post.like_count)}
                  </TableCell>
                  <TableCell className="text-right">
                    {formatNumber(post.comments_count)}
                  </TableCell>
                  <TableCell className="text-right">
                    {formatNumber(post.shares || 0)}
                  </TableCell>
                  <TableCell className="text-right">
                    {formatNumber(post.saved || 0)}
                  </TableCell>
                  <TableCell className="text-right font-medium">
                    {engagementRate}
                  </TableCell>
                  <TableCell className="text-right">
                    {post.views ? formatNumber(post.views) : '---'}
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}