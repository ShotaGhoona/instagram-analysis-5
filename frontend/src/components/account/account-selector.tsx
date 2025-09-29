'use client'

import * as React from 'react'
import { Check, ChevronsUpDown, User } from 'lucide-react'
import Image from 'next/image'

import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { useAccount } from '@/contexts/account-context'

// Account avatar component
function AccountAvatar({ account, size = 'sm' }: { account: any; size?: 'sm' | 'md' }) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8'
  }

  if (account?.profile_picture_url) {
    return (
      <Image
        src={account.profile_picture_url}
        alt={`@${account.username}`}
        width={size === 'sm' ? 24 : 32}
        height={size === 'sm' ? 24 : 32}
        className={cn(
          "rounded-full object-cover border",
          sizeClasses[size]
        )}
        unoptimized
      />
    )
  }

  return (
    <div className={cn(
      "rounded-full bg-gray-200 flex items-center justify-center",
      sizeClasses[size]
    )}>
      <User className={size === 'sm' ? 'h-3 w-3' : 'h-4 w-4'} />
    </div>
  )
}

export function AccountSelector() {
  const { currentAccount, accounts, loading, switchAccount } = useAccount()
  const [open, setOpen] = React.useState(false)

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-white/20 rounded-lg">
        <div className="w-6 h-6 rounded-full bg-white/30 animate-pulse" />
        <span className="text-sm text-white/80">読み込み中...</span>
      </div>
    )
  }

  if (!currentAccount) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-white/20 rounded-lg">
        <User className="h-4 w-4 text-white/60" />
        <span className="text-sm text-white/80">アカウントなし</span>
      </div>
    )
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="ghost"
          role="combobox"
          aria-expanded={open}
          className="w-auto max-w-60 justify-between gap-2 bg-white/20 text-white hover:bg-white/30 border border-white/30"
        >
          <AccountAvatar account={currentAccount} size="sm" />
          <span className="text-sm truncate">
            {currentAccount.name} (@{currentAccount.username})
          </span>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-80 p-0">
        <Command>
          <CommandInput placeholder="アカウント検索..." className="h-9" />
          <CommandList>
            <CommandEmpty>アカウントが見つかりません</CommandEmpty>
            <CommandGroup>
              {accounts.map((account) => (
                <CommandItem
                  key={account.ig_user_id}
                  value={`${account.name} ${account.username}`}
                  onSelect={() => {
                    switchAccount(account.ig_user_id)
                    setOpen(false)
                  }}
                >
                  <div className="flex items-center gap-2 w-full">
                    <AccountAvatar account={account} size="md" />
                    <div className="flex flex-col">
                      <span className="font-medium">{account.name}</span>
                      <span className="text-sm text-muted-foreground">
                        @{account.username}
                      </span>
                    </div>
                    <Check
                      className={cn(
                        "ml-auto h-4 w-4",
                        currentAccount.ig_user_id === account.ig_user_id
                          ? "opacity-100"
                          : "opacity-0"
                      )}
                    />
                  </div>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}