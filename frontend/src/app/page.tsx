import { AuthGuard } from '@/components/auth/auth-guard'

export default function HomePage() {
  return (
    <AuthGuard requireAuth={true}>
      <div className="min-h-screen p-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Instagram Analytics</h1>
          <p className="text-gray-600 mb-8">Instagram分析アプリのホームページ</p>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="bg-white rounded-lg shadow border p-6">
              <h2 className="text-xl font-semibold mb-2">年間分析</h2>
              <p className="text-gray-600 text-sm mb-4">年次データの傾向とサマリー表示</p>
              <div className="text-sm text-gray-500">実装予定: F0301</div>
            </div>
            
            <div className="bg-white rounded-lg shadow border p-6">
              <h2 className="text-xl font-semibold mb-2">月間分析</h2>
              <p className="text-gray-600 text-sm mb-4">月次詳細データとグラフ表示</p>
              <div className="text-sm text-gray-500">実装予定: F0401</div>
            </div>
            
            <div className="bg-white rounded-lg shadow border p-6">
              <h2 className="text-xl font-semibold mb-2">投稿分析</h2>
              <p className="text-gray-600 text-sm mb-4">個別投稿のパフォーマンス分析</p>
              <div className="text-sm text-gray-500">実装予定: F0201</div>
            </div>
          </div>
          
          <div className="mt-8 text-center">
            <p className="text-gray-500 text-sm">PoC版 - 基本的な認証機能まで実装完了</p>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
