'use client'

import { PostsTable } from '@/components/analytics/posts-table'
import { PostsPerformanceChart } from '@/components/analytics/posts-performance-chart'
import { DateFilter } from '@/components/filters/date-filter'
import { MediaTypeFilter } from '@/components/filters/media-type-filter'
import { mockPostsData } from '@/lib/mock-data'
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
    setDateRange,
    setMediaTypes,
    resetFilters
  } = useFilterState(mockPostsData)

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
        <PostsTable posts={filteredPosts} />
        
        {/* さらに読み込むボタン */}
        {filteredPosts.length > 0 && (
          <div className="mt-6 flex justify-center">
            <button className="px-6 py-2 border rounded-md hover:bg-gray-50 transition-colors">
              さらに読み込む
            </button>
          </div>
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
        <h2 className="text-xl font-semibold mb-4">パフォーマンス推移グラフ</h2>
        <p className="text-sm text-gray-600 mb-4">エンゲージメント率 (%)</p>
        
        {filteredPosts.length > 0 ? (
          <>
            <PostsPerformanceChart posts={filteredPosts} />
            <div className="mt-4 flex justify-center">
              <div className="flex items-center gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-[#8884d8] opacity-80"></div>
                  <span>いいね</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-[#82ca9d] opacity-80"></div>
                  <span>リーチ</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-[#ffc658] opacity-80"></div>
                  <span>視聴数</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-[#ff7300] rounded-full"></div>
                  <span>EG率</span>
                </div>
              </div>
            </div>
          </>
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