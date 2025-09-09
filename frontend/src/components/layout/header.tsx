'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { AccountSelector } from '@/components/account/account-selector'

interface HeaderProps {
  accountId?: string
}

export function Header({ accountId = "1" }: HeaderProps) {
  const pathname = usePathname()

  return (
    <header className="border-b bg-white shadow-sm">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Instagram Analytics</h1>
          
          <div className="flex items-center gap-4">
            {/* ナビゲーションボタン */}
            <div className="flex gap-2">
              <Button 
                asChild 
                variant={pathname.includes('yearly') ? 'default' : 'outline'}
                size="sm"
              >
                <Link href={`/analytics/account/${accountId}/yearly`}>
                  年間分析
                </Link>
              </Button>
              <Button 
                asChild 
                variant={pathname.includes('monthly') ? 'default' : 'outline'}
                size="sm"
              >
                <Link href={`/analytics/account/${accountId}/monthly`}>
                  月間分析
                </Link>
              </Button>
              <Button 
                asChild 
                variant={pathname.includes('posts') ? 'default' : 'outline'}
                size="sm"
              >
                <Link href={`/analytics/account/${accountId}/posts`}>
                  投稿分析
                </Link>
              </Button>
            </div>
            
            {/* アカウント切り替え */}
            <AccountSelector />
          </div>
        </div>
      </div>
    </header>
  )
}