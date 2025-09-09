'use client'

import { PostsTable } from '@/components/analytics/posts-table'
import { PostsPerformanceChart } from '@/components/analytics/posts-performance-chart'
import { mockPostsData } from '@/lib/mock-data'

interface PostsAnalyticsPageProps {
  params: { accountId: string }
}

export default function PostsAnalyticsPage({ params }: PostsAnalyticsPageProps) {
  return (
    <div className="space-y-6">
      {/* フィルター機能 */}
      <div className="bg-white rounded-lg border p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium">フィルター</h2>
          <div className="flex gap-4 text-sm">
            <span>📅 2025/08/01 - 2025/08/31</span>
            <span>タイプ: [All] [IMAGE] [VIDEO] [CAROUSEL] [STORY]</span>
          </div>
        </div>
        {/* TODO: F0601-F0603 フィルター機能実装後に統合 */}
      </div>
      
      {/* 投稿一覧テーブル */}
      <div className="bg-white rounded-lg border p-6">
        <PostsTable posts={mockPostsData} />
      </div>
      
      {/* パフォーマンス推移グラフ */}
      <div className="bg-white rounded-lg border p-6">
        <PostsPerformanceChart posts={mockPostsData} />
      </div>
    </div>
  )
}