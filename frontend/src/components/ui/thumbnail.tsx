import Image from 'next/image'
import { useState } from 'react'

interface ThumbnailProps {
  src?: string
  alt: string
  size?: number
}

export function Thumbnail({ src, alt, size = 48 }: ThumbnailProps) {
  const [hasError, setHasError] = useState(false)
  
  const fallbackSrc = 'https://picsum.photos/400/400?random=999'
  return (
    <div className="relative">
      <Image
        src={hasError ? fallbackSrc : (src || fallbackSrc)}
        alt={alt}
        width={size}
        height={size}
        className="rounded-md object-cover"
        onError={() => setHasError(true)}
      />
    </div>
  )
}