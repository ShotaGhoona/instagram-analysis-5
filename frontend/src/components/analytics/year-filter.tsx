'use client'

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface YearFilterProps {
  selectedYear: number
  onYearChange: (year: number) => void
}

const YEARS = Array.from({ length: 11 }, (_, i) => 2020 + i) // 2020-2030

export function YearFilter({ selectedYear, onYearChange }: YearFilterProps) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm font-medium">年:</span>
      <Select value={selectedYear.toString()} onValueChange={(value) => onYearChange(parseInt(value))}>
        <SelectTrigger className="w-[120px]">
          <SelectValue placeholder="年を選択" />
        </SelectTrigger>
        <SelectContent>
          {YEARS.map(year => (
            <SelectItem key={year} value={year.toString()}>
              {year}年
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}