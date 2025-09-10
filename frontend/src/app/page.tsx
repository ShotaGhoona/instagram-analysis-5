'use client'

import { AuthGuard } from '@/components/auth/auth-guard'
import { Header } from '@/components/layout/header'
import { useAccount } from '@/contexts/account-context'
import Link from 'next/link'
import { ArrowRight, BarChart3, Calendar, TrendingUp } from 'lucide-react'

export default function HomePage() {
  const { currentAccount } = useAccount()
  const accountId = currentAccount?.ig_user_id || "1"
  
  const features = [
    {
      icon: <Calendar className="w-8 h-8 text-blue-500" />,
      title: "年間分析",
      description: "年次データの傾向とサマリー",
      href: `/analytics/account/${accountId}/yearly`,
      gradient: "from-blue-500 to-indigo-600",
      bgColor: "bg-blue-50",
    },
    {
      icon: <BarChart3 className="w-8 h-8 text-green-500" />,
      title: "月間分析", 
      description: "月次詳細データとグラフ表示",
      href: `/analytics/account/${accountId}/monthly`,
      gradient: "from-green-500 to-emerald-600",
      bgColor: "bg-green-50",
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-purple-500" />,
      title: "投稿分析",
      description: "個別投稿のパフォーマンス分析",
      href: `/analytics/account/${accountId}/posts`,
      gradient: "from-purple-500 to-violet-600",
      bgColor: "bg-purple-50",
    }
  ]

  return (
    <AuthGuard requireAuth={true}>
      <div className="min-h-screen bg-gray-50">
        <Header />
        
        <div className="min-h-[calc(100vh-80px)] flex flex-col">
          {/* Title Section - 90% */}
          <div className="flex-[0.9] flex items-center justify-center">
            <div className="text-center px-6 pt-20">
              <h1 className="text-6xl text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-violet-500 font-bold text-gray-900 mb-6">
                Shintairiki Instagram Analytics
              </h1>
            </div>
          </div>

          {/* Navigation Section - 10% */}
          <div className="flex-[0.1] grid grid-cols-3">
            {features.map((feature, index) => (
              <Link key={index} href={feature.href} className="block">
                <div className={`h-full ${feature.bgColor} border-r border-gray-200 last:border-r-0 hover:bg-opacity-80 transition-all group cursor-pointer relative overflow-hidden`}>
                  <div className="h-full flex flex-col items-center justify-center p-6 relative z-10">
                    <div className="mb-4 p-4 bg-white rounded-full shadow-md group-hover:shadow-lg transition-shadow">
                      {feature.icon}
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-gray-700">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-gray-600 text-center leading-relaxed group-hover:text-gray-500">
                      {feature.description}
                    </p>
                    <div className="mt-4 flex items-center text-gray-700 group-hover:text-gray-900 transition-colors">
                      <span className="text-sm font-medium">分析を見る</span>
                      <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                  {/* Background gradient on hover */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-10 transition-opacity`}></div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}