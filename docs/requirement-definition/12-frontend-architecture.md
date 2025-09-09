# フロントエンドアーキテクチャ設計

**プロジェクト**: Instagram分析アプリ（PoC）  
**対象**: PC専用、機能重視、TypeScript  
**スタック**: Next.js + TailwindCSS + shadcn/ui + Recharts

## 🏗️ アプリケーション構成

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js App Router                   │
├─────────────────────────────────────────────────────────┤
│  Layout: Header + Navigation + Account Selector        │
├─────────────────┬─────────────────┬─────────────────────┤
│   年間分析       │    月間分析      │      投稿分析        │
│   (Recharts)    │   (Recharts)    │   (Table + Filter)  │
└─────────────────┴─────────────────┴─────────────────────┘
```

## 📁 ディレクトリ構造

```
frontend/
├── app/                          # App Router
│   ├── layout.tsx               # 全体レイアウト
│   ├── page.tsx                 # トップページ (リダイレクト)
│   ├── login/
│   │   └── page.tsx            # ログインページ
│   └── analytics/
│       └── account/
│           └── [accountId]/
│               ├── layout.tsx   # アカウント専用レイアウト
│               ├── yearly/
│               │   └── page.tsx # 年間分析ページ
│               ├── monthly/
│               │   └── page.tsx # 月間分析ページ
│               └── posts/
│                   └── page.tsx # 投稿分析ページ
├── components/                   # 共通コンポーネント
│   ├── ui/                      # shadcn/ui コンポーネント
│   │   ├── button.tsx
│   │   ├── table.tsx
│   │   ├── select.tsx
│   │   ├── calendar.tsx
│   │   ├── loading.tsx
│   │   └── error.tsx
│   ├── layout/
│   │   ├── header.tsx           # ヘッダー
│   │   ├── navigation.tsx       # ナビゲーション
│   │   └── account-selector.tsx # アカウント切り替え
│   ├── analytics/
│   │   ├── yearly-charts.tsx    # 年間分析グラフ
│   │   ├── monthly-charts.tsx   # 月間分析グラフ
│   │   └── posts-table.tsx      # 投稿分析テーブル
│   └── filters/
│       ├── date-filter.tsx      # 日付フィルター
│       └── media-type-filter.tsx # 投稿タイプフィルター
├── lib/
│   ├── api.ts                   # FastAPI クライアント
│   ├── types.ts                 # TypeScript 型定義
│   └── utils.ts                 # ユーティリティ関数
└── hooks/
    ├── use-accounts.ts          # アカウント管理
    ├── use-analytics.ts         # 分析データ
    └── use-auth.ts              # 認証管理
```

## 🎯 ページ構成とルーティング

### URL構造
```
/login                                    # ログイン
/analytics/account/{accountId}/yearly     # 年間分析
/analytics/account/{accountId}/monthly    # 月間分析  
/analytics/account/{accountId}/posts      # 投稿分析
```

### レイアウト階層
```tsx
// app/layout.tsx (Root Layout)
export default function RootLayout() {
  return (
    <html>
      <body>
        <AuthProvider>
          <Header />
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}

// app/analytics/account/[accountId]/layout.tsx
export default function AccountLayout() {
  return (
    <div className="flex">
      <Navigation accountId={accountId} />
      <main className="flex-1 p-6">
        <AccountSelector currentAccountId={accountId} />
        {children}
      </main>
    </div>
  )
}
```

## 🧩 コンポーネント設計

### 1. レイアウトコンポーネント

```tsx
// components/layout/header.tsx
export function Header() {
  return (
    <header className="border-b bg-white">
      <div className="container mx-auto px-6 py-4">
        <h1 className="text-2xl font-bold">Instagram Analytics</h1>
      </div>
    </header>
  )
}

// components/layout/navigation.tsx
interface NavigationProps {
  accountId: string
}

export function Navigation({ accountId }: NavigationProps) {
  return (
    <nav className="w-64 bg-gray-50 border-r">
      <div className="p-4">
        <Button asChild variant={pathname.includes('yearly') ? 'default' : 'ghost'}>
          <Link href={`/analytics/account/${accountId}/yearly`}>年間分析</Link>
        </Button>
        <Button asChild variant={pathname.includes('monthly') ? 'default' : 'ghost'}>
          <Link href={`/analytics/account/${accountId}/monthly`}>月間分析</Link>
        </Button>
        <Button asChild variant={pathname.includes('posts') ? 'default' : 'ghost'}>
          <Link href={`/analytics/account/${accountId}/posts`}>投稿分析</Link>
        </Button>
      </div>
    </nav>
  )
}
```

### 2. 分析コンポーネント

```tsx
// components/analytics/posts-table.tsx
interface PostsTableProps {
  posts: MediaPost[]
  dateFilter: DateRange
  typeFilter: MediaType[]
}

export function PostsTable({ posts, dateFilter, typeFilter }: PostsTableProps) {
  const filteredPosts = useMemo(() => {
    return posts.filter(post => {
      const dateMatch = isDateInRange(post.timestamp, dateFilter)
      const typeMatch = typeFilter.length === 0 || typeFilter.includes(post.media_type)
      return dateMatch && typeMatch
    })
  }, [posts, dateFilter, typeFilter])

  return (
    <div className="space-y-4">
      <div className="flex gap-4">
        <DateFilter onChange={setDateFilter} />
        <MediaTypeFilter onChange={setTypeFilter} />
      </div>
      
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>投稿日</TableHead>
            <TableHead>サムネイル</TableHead>
            <TableHead>タイプ</TableHead>
            <TableHead>リーチ</TableHead>
            <TableHead>いいね</TableHead>
            <TableHead>コメント</TableHead>
            <TableHead>シェア</TableHead>
            <TableHead>保存</TableHead>
            <TableHead>視聴数</TableHead>
            <TableHead>EG率</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filteredPosts.map(post => (
            <TableRow key={post.ig_media_id}>
              <TableCell>{formatDate(post.timestamp)}</TableCell>
              <TableCell>
                <img src={post.thumbnail_url} className="w-12 h-12 object-cover rounded" />
              </TableCell>
              <TableCell>{post.media_type}</TableCell>
              <TableCell>{post.reach?.toLocaleString()}</TableCell>
              <TableCell>{post.like_count?.toLocaleString()}</TableCell>
              <TableCell>{post.comments_count}</TableCell>
              <TableCell>{post.shares}</TableCell>
              <TableCell>{post.saved}</TableCell>
              <TableCell>{post.views?.toLocaleString()}</TableCell>
              <TableCell>{calculateEngagementRate(post)}%</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```

### 3. グラフコンポーネント

```tsx
// components/analytics/yearly-charts.tsx
interface YearlyChartsProps {
  data: YearlyAnalytics
}

export function YearlyCharts({ data }: YearlyChartsProps) {
  return (
    <div className="grid grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>フォロワー推移</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.monthlyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="followers_count" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>エンゲージメント分析</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.monthlyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="likes" stackId="a" fill="#8884d8" />
              <Bar dataKey="comments" stackId="a" fill="#82ca9d" />
              <Bar dataKey="shares" stackId="a" fill="#ffc658" />
              <Bar dataKey="saved" stackId="a" fill="#ff7300" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
```

## 🔧 API クライアント & 型定義

```tsx
// lib/types.ts
export interface MediaPost {
  ig_media_id: string
  ig_user_id: string
  timestamp: string
  media_type: 'IMAGE' | 'VIDEO' | 'CAROUSEL_ALBUM'
  caption?: string
  media_url: string
  thumbnail_url: string
  permalink: string
  like_count: number
  comments_count: number
  reach: number
  views: number
  shares: number
  saved: number
}

export interface InstagramAccount {
  id: string
  name: string
  ig_user_id: string
  username: string
  profile_picture_url: string
}

// lib/api.ts
class ApiClient {
  private baseUrl = process.env.NEXT_PUBLIC_API_URL

  async getAccounts(): Promise<InstagramAccount[]> {
    const response = await fetch(`${this.baseUrl}/accounts`)
    if (!response.ok) throw new Error('Failed to fetch accounts')
    return response.json()
  }

  async getPostsAnalytics(accountId: string): Promise<MediaPost[]> {
    const response = await fetch(`${this.baseUrl}/analytics/posts/${accountId}`)
    if (!response.ok) throw new Error('Failed to fetch posts analytics')
    return response.json()
  }

  async getYearlyAnalytics(accountId: string): Promise<YearlyAnalytics> {
    const response = await fetch(`${this.baseUrl}/analytics/yearly/${accountId}`)
    if (!response.ok) throw new Error('Failed to fetch yearly analytics')
    return response.json()
  }
}

export const apiClient = new ApiClient()
```

## 🎣 カスタムフック

```tsx
// hooks/use-analytics.ts
export function usePostsAnalytics(accountId: string) {
  const [data, setData] = useState<MediaPost[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const posts = await apiClient.getPostsAnalytics(accountId)
        setData(posts)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    if (accountId) {
      fetchData()
    }
  }, [accountId])

  return { data, loading, error, refetch: () => fetchData() }
}
```

## ⚡ 状態管理（シンプル）

```tsx
// PoCレベルなのでuseStateとuseContextで十分
// 複雑になったらZustandやTanStack Queryを検討

// hooks/use-auth.ts
const AuthContext = createContext<AuthContextType | null>(null)

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
```

## 🚀 実装優先度

### Phase 1: 基盤構築 (1-2日)
1. ✅ Next.js セットアップ + shadcn/ui 導入
2. ✅ 基本レイアウト (Header, Navigation)
3. ✅ 認証システム (シンプルログイン)
4. ✅ API クライアント作成

### Phase 2: 投稿分析ページ (2-3日)
1. ✅ テーブルコンポーネント
2. ✅ フィルター機能 (日付・タイプ)
3. ✅ サムネイル表示
4. ✅ エンゲージメント率計算

### Phase 3: グラフページ (2-3日)
1. ✅ Recharts 統合
2. ✅ 年間分析グラフ
3. ✅ 月間分析グラフ

### Phase 4: 統合・テスト (1日)
1. ✅ アカウント切り替え機能
2. ✅ エラーハンドリング
3. ✅ ローディング状態

**総実装期間**: 6-9日