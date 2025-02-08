"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { useRouter } from "next/navigation"  // Import Next.js router

const goals = [
  {
    title: "Personalized Experiences",
    shortDescription: "Tailoring ads to individual interests and preferences.",
    fullDescription:
      "We're revolutionizing digital advertising by creating highly personalized experiences. Our AI-powered platform analyzes user interests and preferences to deliver ads that resonate on a personal level, transforming how users interact with promotional content.",
    color: "bg-blue-100 text-blue-800",
  },
  {
    title: "Enhanced Engagement",
    shortDescription: "Boosting user interaction through relevance.",
    fullDescription:
      "By crafting ads that align with users' passions, we significantly increase engagement rates. Whether it's sports, music, or lifestyle, our platform ensures that each ad speaks directly to the user's interests, leading to higher click-through rates and more meaningful interactions.",
    color: "bg-green-100 text-green-800",
  },
  {
    title: "Improved Conversion",
    shortDescription: "Turning interest into action more effectively.",
    fullDescription:
      "Our personalized approach doesn't just catch attention—it drives action. By presenting products and services in contexts that matter to individual users, we dramatically improve conversion rates, helping businesses achieve better ROI on their advertising spend.",
    color: "bg-yellow-100 text-yellow-800",
  },
  {
    title: "User-Centric Advertising",
    shortDescription: "Making ads a welcome part of the user experience.",
    fullDescription:
      "We believe ads should enhance, not interrupt. By aligning promotional content with user interests, we're transforming advertising from an unwelcome distraction into valuable, relevant information that users appreciate and engage with willingly.",
    color: "bg-red-100 text-red-800",
  },
]

export default function Home() {
  const [expandedCard, setExpandedCard] = useState<number | null>(null)
  const router = useRouter() // ✅ Add router to navigate

  return (
    <div className="px-4 py-8 sm:px-6 lg:px-8">
      <h1 className="text-4xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-8">
        Revolutionizing Digital Advertising
      </h1>

      <p className="text-center text-xl text-gray-700 mb-12 max-w-3xl mx-auto">
        At AdPersona, we're on a mission to transform advertising into personalized, engaging experiences that resonate
        with each individual user.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
        {goals.map((goal, index) => (
          <motion.div
            key={index}
            className={`rounded-lg shadow-lg overflow-hidden cursor-pointer ${goal.color}`}
            layout
            onClick={() => setExpandedCard(expandedCard === index ? null : index)}
          >
            <div className="p-6">
              <h2 className="text-2xl font-bold mb-2">{goal.title}</h2>
              <p>{goal.shortDescription}</p>
              <AnimatePresence>
                {expandedCard === index && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <p className="mt-4">{goal.fullDescription}</p>
                  </motion.div>
                )}
              </AnimatePresence>
              <p className="text-sm mt-4 font-semibold">
                {expandedCard === index ? "Click to collapse" : "Click to learn more"}
              </p>
            </div>
          </motion.div>
        ))}
      </div>

      {/* ✅ "Let's Try" Button - Navigates to /generate */}
      <div className="flex justify-center mt-10">
        <button
          onClick={() => router.push("/generate")}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-lg hover:bg-blue-700"
        >
          Let's Try!
        </button>
      </div>
    </div>
  )
}
