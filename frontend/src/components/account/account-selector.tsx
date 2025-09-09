'use client'

import * as React from 'react'
import { Check, ChevronsUpDown } from 'lucide-react'

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

export function AccountSelector() {
  const { currentAccount, accounts, loading, switchAccount } = useAccount()
  const [open, setOpen] = React.useState(false)

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg">
        <span>👤</span>
        <span className="text-sm">読み込み中...</span>
      </div>
    )
  }

  if (!currentAccount) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 rounded-lg">
        <span>👤</span>
        <span className="text-sm">アカウントなし</span>
      </div>
    )
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-auto justify-between gap-2"
        >
          <span>👤</span>
          <span className="text-sm">
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
                    <span>👤</span>
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