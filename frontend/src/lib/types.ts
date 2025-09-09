// User and Authentication
export interface User {
  id: number
  username: string
  created_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

// Instagram Account
export interface InstagramAccount {
  id: number
  name: string
  ig_user_id: string
  username: string
  profile_picture_url?: string
}

// Media Post
export interface MediaPost {
  ig_media_id: string
  ig_user_id: string
  timestamp: string
  media_type: 'IMAGE' | 'VIDEO' | 'CAROUSEL_ALBUM'
  caption?: string
  media_url: string
  thumbnail_url?: string
  permalink: string
  like_count: number
  comments_count: number
  reach?: number
  views?: number
  shares?: number
  saved?: number
}

// Analytics Data
export interface PostAnalytics extends MediaPost {
  engagement_rate?: number
}

export interface MonthlyStats {
  month: string
  followers_count: number
  follows_count: number
  media_count: number
  profile_views: number
  website_clicks: number
  total_likes: number
  total_comments: number
  total_shares: number
  total_saved: number
}

export interface YearlyAnalytics {
  account_id: string
  monthly_stats: MonthlyStats[]
  total_posts: number
  avg_engagement_rate: number
}

export interface DailyStats {
  date: string
  posts_count: number
  new_followers: number
  reach: number
  profile_views: number
  website_clicks: number
}

export interface MonthlyAnalytics {
  account_id: string
  month: string
  daily_stats: DailyStats[]
}

// Filter Types
export interface DateRange {
  from: Date
  to: Date
}

export type MediaType = 'IMAGE' | 'VIDEO' | 'CAROUSEL_ALBUM'

// API Response Types
export interface ApiResponse<T> {
  data: T
  message?: string
}

export interface ApiError {
  detail: string
  status_code: number
}