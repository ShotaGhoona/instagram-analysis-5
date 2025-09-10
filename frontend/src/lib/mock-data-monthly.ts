import { MonthlyAnalytics, DailyStats } from './types'

// ASCIIデザイン（docs/requirement-definition/03-page-design.md）の月間分析データを完全再現
export const mockMonthlyData: MonthlyAnalytics = {
  account_id: 'mock_account_1',
  month: '2025-03',
  daily_stats: [
    { date: '2025-03-01', posts_count: 0, new_followers: 2, reach: 158, profile_views: 10, website_clicks: 0 },
    { date: '2025-03-02', posts_count: 2, new_followers: 0, reach: 84, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-03', posts_count: 1, new_followers: 0, reach: 61, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-04', posts_count: 2, new_followers: 0, reach: 72, profile_views: 5, website_clicks: 0 },
    { date: '2025-03-05', posts_count: 3, new_followers: 0, reach: 65, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-06', posts_count: 2, new_followers: 0, reach: 80, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-07', posts_count: 1, new_followers: 0, reach: 72, profile_views: 8, website_clicks: 0 },
    { date: '2025-03-08', posts_count: 1, new_followers: 0, reach: 64, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-09', posts_count: 1, new_followers: 0, reach: 53, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-10', posts_count: 0, new_followers: 0, reach: 53, profile_views: 5, website_clicks: 1 },
    { date: '2025-03-11', posts_count: 0, new_followers: 0, reach: 72, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-12', posts_count: 5, new_followers: 0, reach: 64, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-13', posts_count: 0, new_followers: 0, reach: 91, profile_views: 15, website_clicks: 0 },
    { date: '2025-03-14', posts_count: 0, new_followers: 0, reach: 103, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-15', posts_count: 0, new_followers: 0, reach: 59, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-16', posts_count: 0, new_followers: 0, reach: 38, profile_views: 5, website_clicks: 0 },
    { date: '2025-03-17', posts_count: 2, new_followers: 0, reach: 65, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-18', posts_count: 2, new_followers: 0, reach: 70, profile_views: 18, website_clicks: 0 },
    { date: '2025-03-19', posts_count: 0, new_followers: 0, reach: 116, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-20', posts_count: 0, new_followers: 0, reach: 37, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-21', posts_count: 5, new_followers: 0, reach: 103, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-22', posts_count: 1, new_followers: 0, reach: 90, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-23', posts_count: 0, new_followers: 0, reach: 25, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-24', posts_count: 0, new_followers: 0, reach: 57, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-25', posts_count: 19, new_followers: 0, reach: 73, profile_views: 15, website_clicks: 1 },
    { date: '2025-03-26', posts_count: 17, new_followers: 0, reach: 108, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-27', posts_count: 0, new_followers: 0, reach: 73, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-28', posts_count: 1, new_followers: 0, reach: 67, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-29', posts_count: 0, new_followers: 0, reach: 104, profile_views: 0, website_clicks: 0 },
    { date: '2025-03-30', posts_count: 1, new_followers: 0, reach: 36, profile_views: 0, website_clicks: 0 }
  ]
}

// グラフ用データ（簡素化）
export const mockMonthlyChartData = mockMonthlyData.daily_stats.map(stat => ({
  day: parseInt(stat.date.split('-')[2]), // "2025-03-01" -> 1
  date: stat.date,
  新規フォロワー: stat.new_followers,
  リーチ: stat.reach,
  プロフィールアクセス: stat.profile_views,
  ウェブサイトタップ: stat.website_clicks
}))