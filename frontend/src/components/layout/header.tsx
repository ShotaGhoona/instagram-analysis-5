'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { AccountSelector } from '@/components/account/account-selector'
import { BarChartIcon, LogOut } from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'

interface HeaderProps {
  accountId?: string
}

export function Header({ accountId = "1" }: HeaderProps) {
  const pathname = usePathname()
  const router = useRouter()
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <header className="border-b bg-white shadow-sm">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/">
            <h1 className="text-2xl font-bold text-gray-900 cursor-pointer hover:text-gray-700 transition-colors">
              Shintairiki Instagram Analytics
            </h1>
          </Link>
          
          <div className="flex items-center gap-4">
            {/* ナビゲーションボタン - ログイン時のみ表示 */}
            {user && (
              <div className="flex gap-2">
                <Button 
                  asChild 
                  variant={pathname.includes('yearly') ? 'default' : 'outline'}
                >
                  <Link href={`/analytics/account/${accountId}/yearly`}>
                    <BarChartIcon className="w-4 h-4" />
                    年間分析
                  </Link>
                </Button>
                <Button 
                  asChild 
                  variant={pathname.includes('monthly') ? 'default' : 'outline'}
                >
                  <Link href={`/analytics/account/${accountId}/monthly`}>
                    <BarChartIcon className="w-4 h-4" />
                    月間分析
                  </Link>
                </Button>
                <Button 
                  asChild 
                  variant={pathname.includes('posts') ? 'default' : 'outline'}
                >
                  <Link href={`/analytics/account/${accountId}/posts`}>
                    <BarChartIcon className="w-4 h-4" />
                    投稿分析
                  </Link>
                </Button>
              </div>
            )}
            
            <div className="flex items-center gap-2">
              {/* アカウント切り替え - ログイン時のみ表示 */}
              {user && <AccountSelector />}
              
              {/* ログアウトボタン - ログイン時のみ表示 */}
              {user && (
                <Button 
                  variant="outline" 
                  onClick={handleLogout}
                  className="text-gray-600 hover:text-red-600 hover:border-red-300"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  ログアウト
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}