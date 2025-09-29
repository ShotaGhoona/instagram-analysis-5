'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuth } from '@/hooks/use-auth'
import { AuthGuard } from '@/components/auth/auth-guard'

interface LoginForm {
  username: string
  password: string
}

export default function LoginPage() {
  const router = useRouter()
  const { login } = useAuth()
  const [form, setForm] = useState<LoginForm>({ username: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Basic validation
    if (!form.username || form.username.length < 3) {
      setError('ユーザー名は3文字以上で入力してください')
      return
    }
    
    if (!form.password || form.password.length < 6) {
      setError('パスワードは6文字以上で入力してください')
      return
    }

    setLoading(true)
    setError(null)

    try {
      await login(form.username, form.password)
      // リダイレクトはuseAuth内で処理
    } catch (error) {
      setError('ログインに失敗しました。ユーザー名とパスワードを確認してください。')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: keyof LoginForm, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }))
    if (error) setError(null) // Clear error when user starts typing
  }

  return (
    <AuthGuard requireAuth={false}>
      <div 
        className="min-h-screen flex items-center justify-center px-4 relative"
        style={{
          backgroundImage: "url('/johannes-plenio-RwHv7LgeC7s-unsplash.jpg')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat'
        }}
      >
        {/* Dark overlay */}
        <div className="absolute inset-0 bg-black/50"></div>
        
        <div className="w-full max-w-md relative z-10">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white">Instagram Analytics</h1>
            <p className="text-white/80 mt-2">アカウントにログインしてください</p>
          </div>
          
          <Card className="backdrop-blur-md bg-white/10 border border-white/20 shadow-2xl">
            <CardHeader>
              <CardTitle className="text-white text-xl font-semibold">ログイン</CardTitle>
              <CardDescription className="text-white/70">
                ユーザー名とパスワードを入力してログインしてください
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="space-y-2">
                  <Label htmlFor="username" className="text-white text-sm font-medium">ユーザー名</Label>
                  <Input
                    id="username"
                    type="text"
                    placeholder="ユーザー名を入力"
                    value={form.username}
                    onChange={(e) => handleInputChange('username', e.target.value)}
                    disabled={loading}
                    className="bg-white/20 backdrop-blur-sm border-white/30 text-white placeholder:text-white/60 focus:border-white/50 focus:ring-white/20"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-white text-sm font-medium">パスワード</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="パスワードを入力"
                    value={form.password}
                    onChange={(e) => handleInputChange('password', e.target.value)}
                    disabled={loading}
                    className="bg-white/20 backdrop-blur-sm border-white/30 text-white placeholder:text-white/60 focus:border-white/50 focus:ring-white/20"
                  />
                </div>

                {error && (
                  <div className="text-sm text-red-200 bg-red-500/20 backdrop-blur-sm p-3 rounded-md border border-red-300/30">
                    {error}
                  </div>
                )}

                <div className="pt-2">
                  <Button 
                    type="submit" 
                    className="w-full bg-white/30 backdrop-blur-sm border-2 border-white/50 text-white hover:bg-white/40 hover:border-white/60 transition-all duration-200 font-medium" 
                    disabled={loading}
                  >
                    {loading ? 'ログイン中...' : 'ログイン'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </AuthGuard>
  )
}