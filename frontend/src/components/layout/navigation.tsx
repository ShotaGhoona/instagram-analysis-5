'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'

interface NavigationProps {
  accountId: string
}

export function Navigation({ accountId }: NavigationProps) {
  const pathname = usePathname()

  return (
    <nav className="w-64 bg-gray-50 border-r">
      <div className="p-4 space-y-2">
        <Button 
          asChild 
          variant={pathname.includes('yearly') ? 'default' : 'ghost'}
          className="w-full justify-start"
        >
          <Link href={`/analytics/account/${accountId}/yearly`}>
            年間分析
          </Link>
        </Button>
        <Button 
          asChild 
          variant={pathname.includes('monthly') ? 'default' : 'ghost'}
          className="w-full justify-start"
        >
          <Link href={`/analytics/account/${accountId}/monthly`}>
            月間分析
          </Link>
        </Button>
        <Button 
          asChild 
          variant={pathname.includes('posts') ? 'default' : 'ghost'}
          className="w-full justify-start"
        >
          <Link href={`/analytics/account/${accountId}/posts`}>
            投稿分析
          </Link>
        </Button>
      </div>
    </nav>
  )
}