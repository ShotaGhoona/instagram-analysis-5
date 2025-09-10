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
import { calculateEngagementRate, formatNumber } from '@/lib/utils'
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
  // 投稿を日付順（古い順）にソート
  const sortedPosts = [...posts].sort((a, b) => 
    new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  )

  const rowLabels = [
    '投稿日', 
    'サムネイル', 
    'タイプ', 
    'リーチ', 
    'いいね', 
    'コメント', 
    'シェア', 
    '保存', 
    'EG率(%)', 
    '視聴数'
  ]

  const getRowData = (post: MediaPost, rowIndex: number): string | React.ReactNode => {
    const postDate = new Date(post.timestamp)
    const dateDisplay = `${postDate.getMonth() + 1}/${postDate.getDate()}`
    const engagementRate = calculateEngagementRate(post)

    switch (rowIndex) {
      case 0: return dateDisplay
      case 1: return (
        <Thumbnail 
          src={post.media_type === 'VIDEO' ? post.thumbnail_url : post.media_url} 
          alt={`投稿 ${dateDisplay}`}
          size={96}
        />
      )
      case 2: return getMediaTypeDisplay(post.media_type)
      case 3: return formatNumber(post.reach || 0)
      case 4: return formatNumber(post.like_count)
      case 5: return formatNumber(post.comments_count)
      case 6: return formatNumber(post.shares || 0)
      case 7: return formatNumber(post.saved || 0)
      case 8: return engagementRate
      case 9: return post.views ? formatNumber(post.views) : '---'
      default: return ''
    }
  }

  return (
    <div className="">
      <div className="overflow-x-auto">
        <Table>
          {/* <TableHeader>
            <TableRow>
              <TableHead className="w-[120px] sticky left-0 bg-white"></TableHead>
              {sortedPosts.map((post, index) => {
                const postDate = new Date(post.timestamp)
                const dateDisplay = `${postDate.getMonth() + 1}/${postDate.getDate()}`
                return (
                  <TableHead key={post.ig_media_id} className="w-[80px] text-center">
                    投稿{index + 1}
                  </TableHead>
                )
              })}
            </TableRow>
          </TableHeader> */}
          <TableBody>
            {rowLabels.map((label, rowIndex) => (
              <TableRow key={label}>
                <TableCell className="font-medium sticky left-0 bg-white border-r z-10">
                  {label}
                </TableCell>
                {sortedPosts.map((post) => (
                  <TableCell 
                    key={`${post.ig_media_id}-${rowIndex}`} 
                    className={`text-center ${rowIndex === 1 ? 'h-[120px] align-middle items-center justify-center' : ''}`}
                  >
                    {getRowData(post, rowIndex)}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}