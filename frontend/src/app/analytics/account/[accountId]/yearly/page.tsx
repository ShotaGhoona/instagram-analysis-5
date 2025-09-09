interface YearlyAnalyticsPageProps {
  params: { accountId: string }
}

export default function YearlyAnalyticsPage({ params }: YearlyAnalyticsPageProps) {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">年間分析</h1>
      <p className="text-gray-600 mb-6">アカウント ID: {params.accountId}</p>
      
      <div className="grid gap-6 md:grid-cols-2">
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">フォロワー推移</h2>
          <p className="text-gray-500 mb-4">年間のフォロワー数の変動を表示</p>
          {/* TODO: F0301-F0304 年間分析コンポーネント実装後に統合 */}
          <div className="h-64 bg-gray-100 rounded flex items-center justify-center">
            <span className="text-gray-400">グラフプレースホルダー</span>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">エンゲージメント分析</h2>
          <p className="text-gray-500 mb-4">いいね、コメント、シェアの分析</p>
          {/* TODO: F0301-F0304 年間分析コンポーネント実装後に統合 */}
          <div className="h-64 bg-gray-100 rounded flex items-center justify-center">
            <span className="text-gray-400">グラフプレースホルダー</span>
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow border p-6 md:col-span-2">
          <h2 className="text-xl font-semibold mb-4">月別データテーブル</h2>
          <p className="text-gray-500 mb-4">月ごとの詳細な統計データ</p>
          {/* TODO: F0301-F0304 年間分析コンポーネント実装後に統合 */}
          <div className="h-48 bg-gray-100 rounded flex items-center justify-center">
            <span className="text-gray-400">テーブルプレースホルダー</span>
          </div>
        </div>
      </div>
    </div>
  )
}