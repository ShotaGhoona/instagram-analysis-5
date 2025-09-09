import { Header } from '@/components/layout/header'
import { AuthGuard } from '@/components/auth/auth-guard'

interface AnalyticsLayoutProps {
  children: React.ReactNode
  params: { accountId: string }
}

export default function AnalyticsLayout({ children, params }: AnalyticsLayoutProps) {
  return (
    <AuthGuard requireAuth={true}>
      <div className="min-h-screen bg-gray-50">
        <Header accountId={params.accountId} />
        <main className="container mx-auto px-6 py-8">
          {children}
        </main>
      </div>
    </AuthGuard>
  )
}