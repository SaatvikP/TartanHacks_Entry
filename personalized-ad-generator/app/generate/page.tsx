"use client";

import { useState } from "react";
import { generateAd } from "../utils/adGenerator";

const ARTISTS = [
  "Ed Sheeran",
  "Lebron James",
  "Tom Brady",
  "Sachin Tendulkar",
  "Virat Kohli",
  "Stephan Curry",
  "Ronaldo",
  "Tom Holland",
];

const BRANDS = [
  "Adidas",
  "AppLoving",
  "Benetton",
  "Chanel",
  "LV",
  "MRF",
  "Oracle",
  "Redbull",
];

export default function GenerateAdPage() {
  const [artist, setArtist] = useState("");
  const [product, setProduct] = useState("");
  const [brand, setBrand] = useState("");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    const url = await generateAd(artist, product, brand); // Call the backend
    setVideoUrl(url); // Update state with the video URL
    setIsLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Generate Your Personalized Ad</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-semibold">Select Artist:</label>
          <select
            value={artist}
            onChange={(e) => setArtist(e.target.value)}
            className="border p-2 w-full"
            required
          >
            <option value="" disabled>
              Choose an artist
            </option>
            {ARTISTS.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block font-semibold">Product Name:</label>
          <input
            type="text"
            value={product}
            onChange={(e) => setProduct(e.target.value)}
            className="border p-2 w-full"
            placeholder="Enter product name"
            required
          />
        </div>

        <div>
          <label className="block font-semibold">Select Brand:</label>
          <select
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
            className="border p-2 w-full"
            required
          >
            <option value="" disabled>
              Choose a brand
            </option>
            {BRANDS.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white p-2 rounded w-full"
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate Ad"}
        </button>
      </form>

      {videoUrl && (
        <div className="mt-8">
          <h2 className="text-lg font-medium">Your AI-Generated Ad:</h2>
          <video controls className="mt-4 w-full">
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}
