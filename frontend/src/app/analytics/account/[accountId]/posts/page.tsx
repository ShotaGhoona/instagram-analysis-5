'use client'

import { use } from 'react'
import { PostsTable } from '@/components/analytics/posts-table'
import { PostsPerformanceChart } from '@/components/analytics/posts-performance-chart'
import { DateFilter } from '@/components/filters/date-filter'
import { MediaTypeFilter } from '@/components/filters/media-type-filter'
import { useFilterState } from '@/hooks/use-filter-state'
import { Button } from '@/components/ui/button'
import { NoDataDisplay } from '@/components/ui/loading-skeleton'

interface PostsAnalyticsPageProps {
  params: Promise<{ accountId: string }>
}

export default function PostsAnalyticsPage({ params }: PostsAnalyticsPageProps) {
  const resolvedParams = use(params)
  const {
    dateRange,
    mediaTypes,
    filteredPosts,
    filterStats,
    hasActiveFilters,
    loading,
    error,
    setDateRange,
    setMediaTypes,
    resetFilters
  } = useFilterState(resolvedParams.accountId)

  // エラー状態の表示
  if (error) {
    return (
      <div className="space-y-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-red-800 mb-2">データの取得に失敗しました</h2>
          <p className="text-red-600 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>
            ページを再読み込み
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">投稿分析</h1>
        <div className="flex items-center gap-4">
          <DateFilter 
            value={dateRange} 
            onChange={setDateRange} 
          />
          <MediaTypeFilter 
            value={mediaTypes} 
            onChange={setMediaTypes} 
          />
        </div>
      </div>
      
      {/* データがない場合の表示 */}
      {!loading && filteredPosts.length === 0 ? (
        <NoDataDisplay onClearFilters={resetFilters} />
      ) : (
        <>
          {/* 投稿一覧テーブル */}
          <div className="bg-white rounded-lg shadow border p-6 mb-6">
            <PostsTable posts={filteredPosts} />
          </div>

          {/* パフォーマンス推移グラフ */}
          <div className="bg-white rounded-lg shadow border p-6">
            <PostsPerformanceChart posts={filteredPosts} />
          </div>
        </>
      )}
    </div>
  )
}