import { YearlyAnalytics, MonthlyStats } from './types'

// ASCIIデザイン（docs/requirement-definition/03-page-design.md）の数値を完全再現
export const mockYearlyData: YearlyAnalytics = {
  account_id: 'mock_account_1',
  total_posts: 36, // 全期間の投稿数推定
  avg_engagement_rate: 10.5, // 平均エンゲージメント率
  monthly_stats: [
    {
      month: '2023-04',
      followers_count: 728,
      follows_count: 2, // フォロー数は推定値
      media_count: 5, // 投稿数推定
      profile_views: 17,
      website_clicks: 0,
      total_likes: 14,
      total_comments: 0,
      total_shares: 0,
      total_saved: 0
    },
    {
      month: '2024-03', 
      followers_count: 743,
      follows_count: -14, // 新規フォロワー数（負の値は減少）
      media_count: 12, // 投稿数推定
      profile_views: 6,
      website_clicks: 0,
      total_likes: 105,
      total_comments: 0,
      total_shares: 0,
      total_saved: 0
    },
    {
      month: '2024-02',
      followers_count: 740,
      follows_count: 740, // 新規フォロワー（大きな増加）
      media_count: 3, // 投稿数推定
      profile_views: 1,
      website_clicks: 0,
      total_likes: 0,
      total_comments: 0,
      total_shares: 0,
      total_saved: 0
    }
  ]
}

// グラフ用の追加データ（フォロワー推移を滑らかに表示するため）
export const mockFollowerData = [
  { month: '2023-04', followers: 728, following: 2 },
  { month: '2024-02', followers: 740, following: 740 },
  { month: '2024-03', followers: 743, following: 726 } // followingは調整値
]

// エンゲージメント分析用データ（積み上げグラフ用）
export const mockEngagementData = [
  { 
    month: '2023-04', 
    いいね: 14, 
    コメント: 0, 
    シェア: 0, 
    保存: 0 
  },
  { 
    month: '2024-02', 
    いいね: 0, 
    コメント: 0, 
    シェア: 0, 
    保存: 0 
  },
  { 
    month: '2024-03', 
    いいね: 105, 
    コメント: 0, 
    シェア: 0, 
    保存: 0 
  }
]