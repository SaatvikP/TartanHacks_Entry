export async function generateAd(artist: string, product: string, brand: string): Promise<string | null> {
  const API_URL = "http://127.0.0.1:8000/generate_ad"; // Replace with your backend's URL if deployed

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ artist, product, brand }),
    });

    if (response.ok) {
      const data = await response.json();
      return data.video_url; // This assumes the backend returns a video URL
    } else {
      console.error("Error:", response.statusText);
      return null;
    }
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}
