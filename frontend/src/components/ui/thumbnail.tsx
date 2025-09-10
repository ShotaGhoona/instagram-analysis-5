import Image from 'next/image'
import { useState } from 'react'

interface ThumbnailProps {
  src?: string
  alt: string
  size?: number
}

export function Thumbnail({ src, alt, size = 48 }: ThumbnailProps) {
  const [hasError, setHasError] = useState(false)
  
  // フォールバック用のプレースホルダー画像
  const fallbackSrc = `https://via.placeholder.com/400x400/e5e7eb/9ca3af?text=No+Image`
  
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <Image
        src={hasError ? fallbackSrc : (src || fallbackSrc)}
        alt={alt}
        fill
        className="rounded-md object-cover"
        sizes={`${size}px`}
        onError={() => setHasError(true)}
      />
    </div>
  )
}