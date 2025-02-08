"use client"

import { useState, useEffect, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { generateAd } from "../utils/adGenerator"

function VideoResult() {
  const searchParams = useSearchParams()
  const artist = searchParams.get("artist") || ""
  const product = searchParams.get("product") || ""
  const brand = searchParams.get("brand") || ""

  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchVideo = async () => {
      setIsLoading(true)
      try {
        const url = await generateAd(artist, product, brand)
        if (url) {
          setVideoUrl(url)
        } else {
          setError("Failed to generate ad.")
        }
      } catch {
        setError("An error occurred.")
      } finally {
        setIsLoading(false)
      }
    }

    fetchVideo()
  }, [artist, product, brand])

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Your AI-Generated Ad</h1>

      {isLoading && <p className="text-gray-700">Generating ad... Please wait.</p>}
      {error && <p className="text-red-500">{error}</p>}

      {videoUrl && (
        <div className="mt-6">
          <video controls className="mt-4 w-full">
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  )
}

export default function VideoResultPage() {
  return (
    <Suspense fallback={<p className="text-gray-700 text-center">Loading...</p>}>
      <VideoResult />
    </Suspense>
  )
}
