import { use } from 'react'
import { Header } from '@/components/layout/header'
import { AuthGuard } from '@/components/auth/auth-guard'

interface AnalyticsLayoutProps {
  children: React.ReactNode
  params: Promise<{ accountId: string }>
}

export default function AnalyticsLayout({ children, params }: AnalyticsLayoutProps) {
  const resolvedParams = use(params)
  
  return (
    <AuthGuard requireAuth={true}>
      <div className="min-h-screen bg-gray-50">
        <Header accountId={resolvedParams.accountId} />
        <main className="container mx-auto px-6 py-8">
          {children}
        </main>
      </div>
    </AuthGuard>
  )
}