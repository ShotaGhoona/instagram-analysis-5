'use client'

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
  const handleFromDateChange = (date: Date | undefined) => {
    onChange({
      from: date,
      to: value?.to
    })
  }

  const handleToDateChange = (date: Date | undefined) => {
    onChange({
      from: value?.from,
      to: date
    })
  }

  return (
    <div className="flex items-center gap-2">
      {/* 開始日 */}
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            className={cn(
              "w-[140px] justify-start text-left font-normal",
              !value?.from && "text-muted-foreground"
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {value?.from ? (
              format(value.from, "MM/dd", { locale: ja })
            ) : (
              <span>開始日</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={value?.from}
            onSelect={handleFromDateChange}
            locale={ja}
          />
        </PopoverContent>
      </Popover>

      <span className="text-gray-500">-</span>

      {/* 終了日 */}
      <Popover>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            className={cn(
              "w-[140px] justify-start text-left font-normal",
              !value?.to && "text-muted-foreground"
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {value?.to ? (
              format(value.to, "MM/dd", { locale: ja })
            ) : (
              <span>終了日</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={value?.to}
            onSelect={handleToDateChange}
            locale={ja}
          />
        </PopoverContent>
      </Popover>
    </div>
  )
}