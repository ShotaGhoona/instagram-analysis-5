'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { InstagramAccount } from '@/lib/types'
import { apiClient } from '@/lib/api'

interface AccountContextType {
  currentAccount: InstagramAccount | null
  accounts: InstagramAccount[]
  loading: boolean
  error: string | null
  switchAccount: (igUserId: string) => void
  refreshAccounts: () => Promise<void>
}

const AccountContext = createContext<AccountContextType | null>(null)

export function AccountProvider({ children }: { children: React.ReactNode }) {
  const [accounts, setAccounts] = useState<InstagramAccount[]>([])
  const [currentAccount, setCurrentAccount] = useState<InstagramAccount | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const params = useParams()
  const router = useRouter()

  // アカウント一覧取得
  const fetchAccounts = async () => {
    try {
      setLoading(true)
      setError(null)
      const fetchedAccounts = await apiClient.getAccounts()
      setAccounts(fetchedAccounts)
      
      // 現在のアカウントを設定
      if (params.accountId && fetchedAccounts.length > 0) {
        const account = fetchedAccounts.find(acc => acc.ig_user_id === params.accountId)
        setCurrentAccount(account || fetchedAccounts[0])
      } else if (fetchedAccounts.length > 0) {
        setCurrentAccount(fetchedAccounts[0])
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch accounts')
    } finally {
      setLoading(false)
    }
  }

  // 初回アカウント一覧取得
  useEffect(() => {
    fetchAccounts()
  }, [])

  // URL変更時の現在アカウント更新
  useEffect(() => {
    if (params.accountId && accounts.length > 0) {
      const account = accounts.find(acc => acc.ig_user_id === params.accountId)
      if (account && account.ig_user_id !== currentAccount?.ig_user_id) {
        setCurrentAccount(account)
      }
    }
  }, [params.accountId, accounts, currentAccount])

  // アカウント切り替え関数
  const switchAccount = (igUserId: string) => {
    const account = accounts.find(acc => acc.ig_user_id === igUserId)
    if (!account) return

    // 現在のパスからアカウントIDを新しいものに置き換え
    const currentPath = window.location.pathname
    const newPath = currentPath.replace(
      /\/account\/[^\/]+/,
      `/account/${igUserId}`
    )
    
    router.push(newPath)
  }

  // アカウント一覧再取得
  const refreshAccounts = async () => {
    await fetchAccounts()
  }

  const value: AccountContextType = {
    currentAccount,
    accounts,
    loading,
    error,
    switchAccount,
    refreshAccounts
  }

  return (
    <AccountContext.Provider value={value}>
      {children}
    </AccountContext.Provider>
  )
}

export function useAccount() {
  const context = useContext(AccountContext)
  if (!context) {
    throw new Error('useAccount must be used within AccountProvider')
  }
  return context
}