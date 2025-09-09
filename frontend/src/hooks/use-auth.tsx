'use client'

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { apiClient } from '@/lib/api'
import type { User } from '@/lib/types'

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }): JSX.Element {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in on app start
    const token = localStorage.getItem('auth_token')
    if (token) {
      apiClient.setToken(token)
      // TODO: Verify token and get user info from backend
      // For now, set a dummy user to indicate authenticated state
      setUser({ id: 1, username: 'user', created_at: new Date().toISOString() })
    }
    setIsLoading(false)
  }, [])

  const login = async (username: string, password: string) => {
    try {
      const response = await apiClient.login(username, password)
      apiClient.setToken(response.access_token)
      // TODO: Get user info after login
      setUser({ id: 1, username, created_at: new Date().toISOString() })
      
      // ログイン成功後は年間分析ページへ（仮のaccountId: 1を使用）
      window.location.href = '/analytics/account/1/yearly'
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    apiClient.clearToken()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}