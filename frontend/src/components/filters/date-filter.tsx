'use client'

import { useState } from 'react'
import { CalendarIcon } from 'lucide-react'
import { format } from 'date-fns'
import { ja } from 'date-fns/locale'
import { DateRange } from 'react-day-picker'

import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { cn } from '@/lib/utils'

interface DateFilterProps {
  value: DateRange | undefined
  onChange: (dateRange: DateRange | undefined) => void
}

export function DateFilter({ value, onChange }: DateFilterProps) {
  const [isOpen, setIsOpen] = useState(false)

  const formatDateRange = (dateRange: DateRange | undefined): string => {
    if (!dateRange) return '期間を選択'
    
    if (dateRange.from) {
      if (dateRange.to) {
        return `${format(dateRange.from, 'yyyy/MM/dd', { locale: ja })} - ${format(dateRange.to, 'yyyy/MM/dd', { locale: ja })}`
      } else {
        return format(dateRange.from, 'yyyy/MM/dd', { locale: ja })
      }
    }
    
    return '期間を選択'
  }

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className={cn(
            'justify-start text-left font-normal',
            !value && 'text-muted-foreground'
          )}
        >
          <CalendarIcon className="mr-2 h-4 w-4" />
          📅 {formatDateRange(value)}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        <Calendar
          initialFocus
          mode="range"
          defaultMonth={value?.from}
          selected={value}
          onSelect={(range) => {
            onChange(range)
            if (range?.from && range?.to) {
              setIsOpen(false)
            }
          }}
          numberOfMonths={2}
          locale={ja}
        />
      </PopoverContent>
    </Popover>
  )
}