'use client'

import { AuthProvider } from '@/hooks/use-auth'
import { AccountProvider } from '@/contexts/account-context'
import { ReactNode } from 'react'

interface ProvidersProps {
  children: ReactNode
}

export function Providers({ children }: ProvidersProps) {
  return (
    <AuthProvider>
      <AccountProvider>
        {children}
      </AccountProvider>
    </AuthProvider>
  )
}