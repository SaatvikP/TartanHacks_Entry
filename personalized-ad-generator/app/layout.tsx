import "./globals.css"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import Link from "next/link"
import type React from "react"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "AdPersona - Personalized Ad Platform",
  description: "Revolutionizing digital advertising with AI-powered personalization",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gradient-to-br from-gray-100 to-gray-200`}>
        <div className="flex flex-col min-h-screen">
          <nav className="bg-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex">
                  <div className="flex-shrink-0 flex items-center">
                    <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
                      AdPersona
                    </span>
                  </div>
                  <div className="ml-6 flex space-x-8">
                    <Link
                      href="/"
                      className="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium border-transparent hover:border-gray-300 text-gray-500 hover:text-gray-700"
                    >
                      Goals
                    </Link>
                    <Link
                      href="/demo"
                      className="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium border-transparent hover:border-gray-300 text-gray-500 hover:text-gray-700"
                    >
                      Demo
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </nav>
          <main className="flex-grow">{children}</main>
          <footer className="bg-white shadow-lg mt-12">
            <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
              <p className="text-center text-gray-500 text-sm">© 2023 AdPersona. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}

