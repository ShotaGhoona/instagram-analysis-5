'use client'

import { useState } from 'react'
import { Check, ChevronDown } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'
import { MediaType } from '@/lib/types'

interface MediaTypeFilterProps {
  value: MediaType[]
  onChange: (mediaTypes: MediaType[]) => void
}

const MEDIA_TYPE_OPTIONS = [
  { value: 'IMAGE' as MediaType, label: 'IMAGE' },
  { value: 'VIDEO' as MediaType, label: 'VIDEO' },
  { value: 'CAROUSEL_ALBUM' as MediaType, label: 'CAROUSEL' },
  // TODO: { value: 'STORY' as MediaType, label: 'STORY' } 将来実装
]

export function MediaTypeFilter({ value, onChange }: MediaTypeFilterProps) {
  const [isOpen, setIsOpen] = useState(false)

  const toggleMediaType = (mediaType: MediaType) => {
    const newValue = value.includes(mediaType)
      ? value.filter(type => type !== mediaType)
      : [...value, mediaType]
    onChange(newValue)
  }

  const getDisplayText = (): string => {
    if (value.length === 0) {
      return 'All'
    }
    if (value.length === MEDIA_TYPE_OPTIONS.length) {
      return 'All'
    }
    if (value.length === 1) {
      const option = MEDIA_TYPE_OPTIONS.find(opt => opt.value === value[0])
      return option?.label || 'All'
    }
    return `${value.length}種類選択中`
  }

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={isOpen}
          className="justify-between"
        >
          タイプ: [{getDisplayText()}]
          <ChevronDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <div className="p-2">
          <div className="space-y-1">
            {/* All選択オプション */}
            <div
              className={cn(
                'flex items-center space-x-2 rounded-sm px-2 py-1.5 text-sm cursor-pointer hover:bg-accent',
                value.length === 0 && 'bg-accent'
              )}
              onClick={() => onChange([])}
            >
              <div className={cn(
                'h-4 w-4 border border-primary rounded-sm flex items-center justify-center',
                value.length === 0 && 'bg-primary'
              )}>
                {value.length === 0 && <Check className="h-3 w-3 text-primary-foreground" />}
              </div>
              <span>All</span>
            </div>
            
            {/* 個別タイプ選択オプション */}
            {MEDIA_TYPE_OPTIONS.map((option) => {
              const isSelected = value.includes(option.value)
              return (
                <div
                  key={option.value}
                  className={cn(
                    'flex items-center space-x-2 rounded-sm px-2 py-1.5 text-sm cursor-pointer hover:bg-accent',
                    isSelected && 'bg-accent'
                  )}
                  onClick={() => toggleMediaType(option.value)}
                >
                  <div className={cn(
                    'h-4 w-4 border border-primary rounded-sm flex items-center justify-center',
                    isSelected && 'bg-primary'
                  )}>
                    {isSelected && <Check className="h-3 w-3 text-primary-foreground" />}
                  </div>
                  <span>{option.label}</span>
                </div>
              )
            })}
          </div>
        </div>
      </PopoverContent>
    </Popover>
  )
}