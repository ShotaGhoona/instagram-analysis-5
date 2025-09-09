'use client'

import { PostsTable } from '@/components/analytics/posts-table'
import { PostsPerformanceChart } from '@/components/analytics/posts-performance-chart'
import { DateFilter } from '@/components/filters/date-filter'
import { MediaTypeFilter } from '@/components/filters/media-type-filter'
import { useFilterState } from '@/hooks/use-filter-state'
import { Button } from '@/components/ui/button'

interface PostsAnalyticsPageProps {
  params: { accountId: string }
}

export default function PostsAnalyticsPage({ params }: PostsAnalyticsPageProps) {
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
  } = useFilterState(params.accountId)

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
    <div className="space-y-6">
      {/* フィルター機能 */}
      <div className="bg-white rounded-lg border p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium">フィルター</h2>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <span>{filterStats.filtered} / {filterStats.total} 件表示中</span>
            {hasActiveFilters && (
              <Button 
                variant="outline" 
                size="sm" 
                onClick={resetFilters}
                className="text-xs"
              >
                リセット
              </Button>
            )}
          </div>
        </div>
        
        <div className="flex gap-4">
          <DateFilter 
            value={dateRange} 
            onChange={setDateRange} 
          />
          <MediaTypeFilter 
            value={mediaTypes} 
            onChange={setMediaTypes} 
          />
        </div>
        
        {hasActiveFilters && filterStats.hidden > 0 && (
          <div className="mt-3 text-sm text-gray-500">
            {filterStats.hidden}件の投稿が非表示になっています
          </div>
        )}
      </div>
      
      {/* 投稿一覧テーブル */}
      <div className="bg-white rounded-lg border p-6">
        <h2 className="text-xl font-semibold mb-4">投稿一覧テーブル</h2>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-gray-500">データを読み込み中...</div>
          </div>
        ) : (
          <PostsTable posts={filteredPosts} />
        )}
        
        {filteredPosts.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <p>フィルター条件に一致する投稿がありません</p>
            <Button 
              variant="outline" 
              onClick={resetFilters}
              className="mt-2"
            >
              フィルターをリセット
            </Button>
          </div>
        )}
      </div>
      
      {/* パフォーマンス推移グラフ */}
      <div className="bg-white rounded-lg border p-6">
        {loading ? (
          <div className="h-80 flex items-center justify-center">
            <div className="text-gray-500">グラフを読み込み中...</div>
          </div>
        ) : filteredPosts.length > 0 ? (
          <PostsPerformanceChart posts={filteredPosts} />
        ) : (
          <div className="h-80 flex items-center justify-center text-gray-500 bg-gray-50 rounded border-2 border-dashed border-gray-300">
            <div className="text-center">
              <p className="mb-2">表示する投稿がありません</p>
              <Button 
                variant="outline" 
                onClick={resetFilters}
              >
                フィルターをリセット
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}