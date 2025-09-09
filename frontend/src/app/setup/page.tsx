'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/layout/header'
import { useAccount } from '@/contexts/account-context'
import { apiClient } from '@/lib/api'

export default function SetupPage() {
  const { accounts } = useAccount()
  const [credentials, setCredentials] = useState({
    appId: '',
    appSecret: '',
    accessToken: ''
  })
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      const result = await apiClient.refreshTokens({
        app_id: credentials.appId,
        app_secret: credentials.appSecret,
        access_token: credentials.accessToken
      })
      
      if (result.success) {
        alert(`トークン更新成功！\n新規: ${result.new_accounts}件\n更新: ${result.updated_accounts}件\n処理総数: ${result.total_processed}件`)
        // Clear form after success
        setCredentials({ appId: '', appSecret: '', accessToken: '' })
      } else {
        alert(`トークン更新に失敗しました\nエラー: ${result.errors.join(', ')}`)
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      alert(`トークン更新中にエラーが発生しました: ${error}`)
    } finally {
      setIsLoading(false)
    }
  }

  const getTokenStatus = (account: any) => {
    // ダミーロジック - 実際のAPIでは有効期限をチェック
    const statuses = ['valid', 'expired', 'unset']
    const randomStatus = statuses[Math.floor(Math.random() * statuses.length)]
    return randomStatus
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'valid':
        return '✅'
      case 'expired':
        return '⚠️'
      case 'unset':
        return '❌'
      default:
        return '❌'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'valid':
        return '正常'
      case 'expired':
        return '更新が必要'
      case 'unset':
        return '未連携'
      default:
        return '未連携'
    }
  }

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'valid':
        return 'default' as const
      case 'expired':
        return 'secondary' as const
      case 'unset':
        return 'destructive' as const
      default:
        return 'destructive' as const
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Instagram API セットアップ</h1>
          <p className="text-gray-600">Instagram API の設定を行います</p>
        </div>

        <div className="grid gap-8 max-w-4xl">
          {/* API設定フォーム */}
          <Card>
            <CardHeader>
              <CardTitle>API 認証情報</CardTitle>
              <CardDescription>
                Instagram App ID、App Secret、Access Token を入力してください
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="appId">App ID</Label>
                  <Input
                    id="appId"
                    type="text"
                    placeholder="Instagram App ID を入力"
                    value={credentials.appId}
                    onChange={(e) => setCredentials(prev => ({ ...prev, appId: e.target.value }))}
                    className="font-mono text-sm"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="appSecret">App Secret</Label>
                  <Input
                    id="appSecret"
                    type="password"
                    placeholder="Instagram App Secret を入力"
                    value={credentials.appSecret}
                    onChange={(e) => setCredentials(prev => ({ ...prev, appSecret: e.target.value }))}
                    className="font-mono text-sm"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="accessToken">Access Token</Label>
                  <Input
                    id="accessToken"
                    type="text"
                    placeholder="Instagram Access Token を入力"
                    value={credentials.accessToken}
                    onChange={(e) => setCredentials(prev => ({ ...prev, accessToken: e.target.value }))}
                    className="font-mono text-sm"
                  />
                </div>

                <Button 
                  type="submit" 
                  disabled={isLoading || !credentials.appId || !credentials.appSecret || !credentials.accessToken}
                  className="w-full"
                >
                  {isLoading ? 'トークン更新中...' : 'トークン更新'}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* アカウント連携状況 */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                ✅ アカウント連携状況
              </CardTitle>
              <CardDescription>
                接続済みの Instagram アカウント一覧
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {accounts.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">アカウントが登録されていません</p>
                ) : (
                  accounts.map((account) => {
                    const tokenStatus = getTokenStatus(account)
                    return (
                      <div key={account.ig_user_id} className="border rounded-lg p-4 space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className="text-2xl">📱</span>
                            <div>
                              <h3 className="font-medium text-gray-900">
                                {account.name} (@{account.username})
                              </h3>
                            </div>
                          </div>
                          <Badge variant={getStatusBadgeVariant(tokenStatus)}>
                            {getStatusIcon(tokenStatus)} {getStatusText(tokenStatus)}
                          </Badge>
                        </div>
                        
                        <div className="ml-11 space-y-1 text-sm text-gray-600">
                          <div className="flex justify-between">
                            <span>├ トークン:</span>
                            <span>
                              {tokenStatus === 'valid' ? '有効 (有効期限: 2025-09-15)' : 
                               tokenStatus === 'expired' ? '期限切れ (有効期限: 2025-08-10)' : 
                               '未設定'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>├ 最終更新:</span>
                            <span>
                              {tokenStatus === 'valid' ? '2025-08-15 14:30' : 
                               tokenStatus === 'expired' ? '2025-07-10 09:15' : 
                               '---'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>└ ステータス:</span>
                            <span>{getStatusIcon(tokenStatus)} {getStatusText(tokenStatus)}</span>
                          </div>
                        </div>
                      </div>
                    )
                  })
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}