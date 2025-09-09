'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, Info, CheckCircle, AlertTriangle, XCircle } from 'lucide-react'
import { Header } from '@/components/layout/header'
import { useAccount } from '@/contexts/account-context'
import { apiClient } from '@/lib/api'

export default function SetupPage() {
  const { accounts, loading: accountsLoading } = useAccount()
  const [credentials, setCredentials] = useState({
    appId: '',
    appSecret: '',
    accessToken: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setResult(null)
    
    try {
      const response = await apiClient.refreshTokens({
        app_id: credentials.appId,
        app_secret: credentials.appSecret,
        access_token: credentials.accessToken
      })
      
      setResult(response)
      
      if (response.success) {
        // Clear form after success
        setCredentials({ appId: '', appSecret: '', accessToken: '' })
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      setResult({
        success: false,
        message: `通信エラーが発生しました: ${error}`,
        errors: [String(error)]
      })
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
        return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'expired':
        return <AlertTriangle className="h-4 w-4 text-yellow-600" />
      case 'unset':
        return <XCircle className="h-4 w-4 text-red-600" />
      default:
        return <XCircle className="h-4 w-4 text-red-600" />
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

  const isFormValid = credentials.appId.trim() && credentials.appSecret.trim() && credentials.accessToken.trim()

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Instagram API セットアップ</h1>
          <p className="text-gray-600">Instagram API の認証情報を設定してアカウントトークンを更新します</p>
        </div>

        <div className="grid gap-8 max-w-4xl">
          {/* 結果表示 */}
          {result && (
            <Alert className={result.success ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}>
              <div className="flex items-start gap-3">
                {result.success ? (
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-600 mt-0.5" />
                )}
                <div className="flex-1">
                  <AlertDescription className="text-sm">
                    <div className="font-medium mb-2">{result.message}</div>
                    {result.success && (
                      <div className="space-y-1 text-xs text-gray-700">
                        <div>新規アカウント: {result.new_accounts}件</div>
                        <div>更新アカウント: {result.updated_accounts}件</div>
                        <div>処理総数: {result.total_processed}件</div>
                      </div>
                    )}
                    {!result.success && result.errors && result.errors.length > 0 && (
                      <div className="mt-2">
                        <div className="text-xs font-medium mb-1">エラー詳細:</div>
                        <ul className="text-xs space-y-1">
                          {result.errors.map((error: string, index: number) => (
                            <li key={index} className="text-red-700">• {error}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </AlertDescription>
                </div>
              </div>
            </Alert>
          )}

          {/* API設定フォーム */}
          <Card>
            <CardHeader>
              <CardTitle>API 認証情報</CardTitle>
              <CardDescription>
                Instagram App ID、App Secret、Access Token を入力してトークンを更新してください
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="appId">
                    App ID <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="appId"
                    type="text"
                    placeholder="例: 1234567890123456"
                    value={credentials.appId}
                    onChange={(e) => setCredentials(prev => ({ ...prev, appId: e.target.value }))}
                    className="font-mono text-sm"
                    required
                  />
                  <p className="text-xs text-gray-500">
                    Facebook Developer App の App ID を入力してください
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="appSecret">
                    App Secret <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="appSecret"
                    type="password"
                    placeholder="例: a1b2c3d4e5f6g7h8i9j0..."
                    value={credentials.appSecret}
                    onChange={(e) => setCredentials(prev => ({ ...prev, appSecret: e.target.value }))}
                    className="font-mono text-sm"
                    required
                  />
                  <p className="text-xs text-gray-500">
                    Facebook Developer App の App Secret を入力してください
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="accessToken">
                    Access Token <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="accessToken"
                    type="text"
                    placeholder="例: EAARrfZCwPTGUBP..."
                    value={credentials.accessToken}
                    onChange={(e) => setCredentials(prev => ({ ...prev, accessToken: e.target.value }))}
                    className="font-mono text-sm"
                    required
                  />
                  <p className="text-xs text-gray-500">
                    Instagram Graph API の User Access Token を入力してください
                  </p>
                </div>

                <Button 
                  type="submit" 
                  disabled={isLoading || !isFormValid}
                  className="w-full"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      トークン更新中...
                    </>
                  ) : (
                    'トークン更新'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* アカウント連携状況 */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                アカウント連携状況
              </CardTitle>
              <CardDescription>
                現在接続済みの Instagram アカウント一覧
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {accountsLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <Loader2 className="h-6 w-6 animate-spin mr-2" />
                    <span className="text-gray-500">アカウント情報を読み込み中...</span>
                  </div>
                ) : accounts.length === 0 ? (
                  <div className="text-center py-8">
                    <Info className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">アカウントが登録されていません</p>
                    <p className="text-xs text-gray-400 mt-1">
                      上記フォームでトークン更新を実行するとアカウントが追加されます
                    </p>
                  </div>
                ) : (
                  accounts.map((account) => {
                    const tokenStatus = getTokenStatus(account)
                    return (
                      <div key={account.ig_user_id} className="border rounded-lg p-4 space-y-3 hover:shadow-sm transition-shadow">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className="text-2xl">📱</span>
                            <div>
                              <h3 className="font-medium text-gray-900">
                                {account.name} (@{account.username})
                              </h3>
                              <p className="text-xs text-gray-500">ID: {account.ig_user_id}</p>
                            </div>
                          </div>
                          <Badge variant={getStatusBadgeVariant(tokenStatus)} className="flex items-center gap-1">
                            {getStatusIcon(tokenStatus)}
                            {getStatusText(tokenStatus)}
                          </Badge>
                        </div>
                        
                        <div className="ml-11 space-y-1 text-sm text-gray-600 bg-gray-50 rounded p-3">
                          <div className="flex justify-between">
                            <span>├ トークン:</span>
                            <span className="font-mono text-xs">
                              {tokenStatus === 'valid' ? '有効 (有効期限: 2025-09-15)' : 
                               tokenStatus === 'expired' ? '期限切れ (有効期限: 2025-08-10)' : 
                               '未設定'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>├ 最終更新:</span>
                            <span className="font-mono text-xs">
                              {tokenStatus === 'valid' ? '2025-08-15 14:30' : 
                               tokenStatus === 'expired' ? '2025-07-10 09:15' : 
                               '---'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>└ ステータス:</span>
                            <span className="flex items-center gap-1">
                              {getStatusIcon(tokenStatus)}
                              <span>{getStatusText(tokenStatus)}</span>
                            </span>
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