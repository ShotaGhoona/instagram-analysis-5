import { InstagramAccount } from './types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private baseUrl: string
  private token: string | null = null

  constructor() {
    this.baseUrl = API_BASE_URL
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token')
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { Authorization: `Bearer ${this.token}` }),
        ...options.headers,
      },
      ...options,
    }

    const response = await fetch(url, config)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  setToken(token: string) {
    this.token = token
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token)
    }
  }

  clearToken() {
    this.token = null
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
    }
  }

  // Auth endpoints
  async login(username: string, password: string): Promise<{ access_token: string; token_type: string }> {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
  }

  async register(username: string, password: string) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
  }

  // Account endpoints
  async getAccounts(): Promise<InstagramAccount[]> {
    return this.request('/accounts/')
  }

  async getAccount(igUserId: string): Promise<InstagramAccount> {
    return this.request(`/accounts/${igUserId}`)
  }

  // Analytics endpoints
  async getYearlyAnalytics(accountId: string) {
    return this.request(`/analytics/yearly/${accountId}`)
  }

  async getMonthlyAnalytics(accountId: string, year: number, month: number) {
    return this.request(`/analytics/monthly/${accountId}?year=${year}&month=${month}`)
  }

  async getPostsAnalytics(accountId: string, params?: {
    start_date?: string
    end_date?: string
    media_type?: string
  }) {
    const searchParams = new URLSearchParams(params as Record<string, string>)
    return this.request(`/analytics/posts/${accountId}?${searchParams}`)
  }

  // Setup endpoints
  async refreshTokens(credentials: {
    app_id: string
    app_secret: string
    access_token: string
  }): Promise<{
    success: boolean
    message: string
    updated_accounts: number
    new_accounts: number
    total_processed: number
    errors: string[]
  }> {
    return this.request('/setup/refresh-tokens', {
      method: 'POST',
      body: JSON.stringify({
        app_id: credentials.app_id,
        app_secret: credentials.app_secret,
        access_token: credentials.access_token
      }),
    })
  }
}

export const apiClient = new ApiClient()