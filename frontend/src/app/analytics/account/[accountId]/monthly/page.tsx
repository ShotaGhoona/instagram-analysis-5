interface MonthlyAnalyticsPageProps {
  params: { accountId: string }
}

export default function MonthlyAnalyticsPage({ params }: MonthlyAnalyticsPageProps) {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">月間分析</h1>
      <p className="text-gray-600 mb-6">アカウント ID: {params.accountId}</p>
      
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">日別データテーブル</h2>
          <p className="text-gray-500 mb-4">月間の日別統計データ</p>
          {/* TODO: F0401-F0403 月間分析コンポーネント実装後に統合 */}
          <div className="h-64 bg-gray-100 rounded flex items-center justify-center">
            <span className="text-gray-400">テーブルプレースホルダー</span>
          </div>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div className="bg-white rounded-lg shadow border p-6">
            <h3 className="text-lg font-semibold mb-2">新規フォロワー数</h3>
            <div className="h-32 bg-gray-100 rounded flex items-center justify-center">
              <span className="text-gray-400">グラフ</span>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow border p-6">
            <h3 className="text-lg font-semibold mb-2">リーチ</h3>
            <div className="h-32 bg-gray-100 rounded flex items-center justify-center">
              <span className="text-gray-400">グラフ</span>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow border p-6">
            <h3 className="text-lg font-semibold mb-2">プロフィールアクセス</h3>
            <div className="h-32 bg-gray-100 rounded flex items-center justify-center">
              <span className="text-gray-400">グラフ</span>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow border p-6">
            <h3 className="text-lg font-semibold mb-2">ウェブサイトタップ</h3>
            <div className="h-32 bg-gray-100 rounded flex items-center justify-center">
              <span className="text-gray-400">グラフ</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}