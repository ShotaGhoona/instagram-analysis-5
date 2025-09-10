export function YearlyPageSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="flex justify-between items-center mb-6">
        <div className="h-8 bg-gray-200 rounded w-64"></div>
        <div className="h-6 bg-gray-200 rounded w-48"></div>
      </div>
      
      {/* テーブルSkeleton */}
      <div className="bg-white rounded-lg shadow border p-6 mb-6">
        <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex space-x-4">
              <div className="h-4 bg-gray-200 rounded w-24"></div>
              <div className="h-4 bg-gray-200 rounded w-16"></div>
              <div className="h-4 bg-gray-200 rounded w-20"></div>
              <div className="h-4 bg-gray-200 rounded w-16"></div>
              <div className="h-4 bg-gray-200 rounded w-16"></div>
            </div>
          ))}
        </div>
      </div>

      {/* グラフSkeleton */}
      <div className="grid gap-6 md:grid-cols-2">
        <div className="bg-white rounded-lg shadow border p-6">
          <div className="h-6 bg-gray-200 rounded w-32 mb-4"></div>
          <div className="h-[300px] bg-gray-200 rounded"></div>
        </div>
        <div className="bg-white rounded-lg shadow border p-6">
          <div className="h-6 bg-gray-200 rounded w-40 mb-4"></div>
          <div className="h-[300px] bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>
  )
}

export function ErrorDisplay({ error, onRetry }: { error: string, onRetry: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
      <div className="text-red-500 text-lg mb-4">⚠️ {error}</div>
      <button 
        onClick={onRetry}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        再試行
      </button>
    </div>
  )
}

export function MonthlyPageSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="flex justify-between items-center mb-6">
        <div className="h-8 bg-gray-200 rounded w-64"></div>
        <div className="h-6 bg-gray-200 rounded w-48"></div>
      </div>
      
      <div className="grid gap-6 md:grid-cols-2">
        {/* テーブルSkeleton */}
        <div className="bg-white rounded-lg shadow border p-6">
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex space-x-4">
                <div className="h-4 bg-gray-200 rounded w-20"></div>
                <div className="h-4 bg-gray-200 rounded w-16"></div>
                <div className="h-4 bg-gray-200 rounded w-16"></div>
                <div className="h-4 bg-gray-200 rounded w-16"></div>
              </div>
            ))}
          </div>
        </div>

        {/* グラフSkeleton */}
        <div>
          <div className="h-6 bg-gray-200 rounded w-32 mb-4"></div>
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg shadow border p-4">
                <div className="h-[150px] bg-gray-200 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export function NoDataDisplay() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] text-center">
      <div className="text-gray-500 text-lg mb-4">📊 データがありません</div>
      <div className="text-gray-400 text-sm">
        データが収集されるまでお待ちください
      </div>
    </div>
  )
}