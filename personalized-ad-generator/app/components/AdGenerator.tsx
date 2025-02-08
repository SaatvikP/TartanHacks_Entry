"use client"

import { useState, useEffect } from "react"
import { generateAd } from "../utils/adGenerator"

const DEMO_SCENARIOS = [
  { interests: "football, sports", product: "running shoes" },
  { interests: "music, Ed Sheeran", product: "wireless headphones" },
  { interests: "cooking, healthy lifestyle", product: "air fryer" },
]

export default function AdGenerator() {
  const [currentScenario, setCurrentScenario] = useState(0)
  const [ad, setAd] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    generateAdForCurrentScenario()
  }, [currentScenario])

  const generateAdForCurrentScenario = async () => {
    setIsLoading(true)
    try {
      const scenario = DEMO_SCENARIOS[currentScenario]
      const generatedAd = await generateAd(scenario.interests, scenario.product)
      setAd(generatedAd)
    } catch (err) {
      console.error("Failed to generate ad:", err)
      setAd("Failed to generate ad. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleNextScenario = () => {
    setCurrentScenario((prev) => (prev + 1) % DEMO_SCENARIOS.length)
  }

  const scenario = DEMO_SCENARIOS[currentScenario]

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6 p-4 bg-white shadow rounded-lg">
        <h2 className="text-lg font-medium text-gray-900 mb-2">Current Scenario:</h2>
        <p>
          <strong>Interests:</strong> {scenario.interests}
        </p>
        <p>
          <strong>Product:</strong> {scenario.product}
        </p>
      </div>
      <div className="mb-6">
        <button
          onClick={handleNextScenario}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Next Scenario"}
        </button>
      </div>
      {ad && (
        <div className="mt-8">
          <h2 className="text-lg font-medium text-gray-900">Generated Ad:</h2>
          <div className="mt-2 p-4 bg-white shadow rounded-lg">
            <p className="text-gray-700">{ad}</p>
          </div>
        </div>
      )}
    </div>
  )
}

