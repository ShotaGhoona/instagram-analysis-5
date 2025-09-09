interface PostsAnalyticsPageProps {
  params: { accountId: string }
}

export default function PostsAnalyticsPage({ params }: PostsAnalyticsPageProps) {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">投稿分析</h1>
      <p className="text-gray-600 mb-6">アカウント ID: {params.accountId}</p>
      
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow border p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">フィルター</h2>
            <div className="flex gap-2">
              <div className="px-3 py-1 bg-gray-100 rounded text-sm">📅 期間選択</div>
              <div className="px-3 py-1 bg-gray-100 rounded text-sm">🎬 タイプ選択</div>
            </div>
          </div>
          {/* TODO: F0601-F0603 フィルター機能実装後に統合 */}
          <p className="text-gray-500">フィルター機能はF0601-F0603で実装予定</p>
        </div>
        
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">投稿一覧テーブル</h2>
          <p className="text-gray-500 mb-4">投稿のパフォーマンスデータを表示</p>
          {/* TODO: F0201-F0205 投稿分析コンポーネント実装後に統合 */}
          <div className="h-64 bg-gray-100 rounded flex items-center justify-center">
            <span className="text-gray-400">投稿テーブルプレースホルダー</span>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">パフォーマンス推移グラフ</h2>
          <p className="text-gray-500 mb-4">時系列でのエンゲージメント率推移</p>
          {/* TODO: F0201-F0205 投稿分析コンポーネント実装後に統合 */}
          <div className="h-48 bg-gray-100 rounded flex items-center justify-center">
            <span className="text-gray-400">グラフプレースホルダー</span>
          </div>
        </div>
      </div>
    </div>
  )
}