import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date) {
  return new Intl.DateTimeFormat('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(date))
}

export function formatDateTime(date: string | Date) {
  return new Intl.DateTimeFormat('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

export function calculateEngagementRate(post: {
  like_count: number
  comments_count: number
  shares?: number
  saved?: number
  reach?: number
}): number {
  const totalEngagements = 
    post.like_count + 
    post.comments_count + 
    (post.shares || 0) + 
    (post.saved || 0)
  
  const reach = post.reach || 1
  return Math.round((totalEngagements / reach) * 100 * 10) / 10
}

export function formatNumber(num: number): string {
  return new Intl.NumberFormat('ja-JP').format(num)
}

export function isDateInRange(date: string | Date, range: { from: Date; to: Date }): boolean {
  const targetDate = new Date(date)
  return targetDate >= range.from && targetDate <= range.to
}
