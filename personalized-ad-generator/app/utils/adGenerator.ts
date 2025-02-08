export async function generateAd(interests: string, product: string): Promise<string> {
  // Simulate API call delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  const interestList = interests.split(",").map((i) => i.trim().toLowerCase())

  // Mock ad generation logic
  let adContent = `Experience the ultimate ${product} that's perfect for `

  if (interestList.includes("football") || interestList.includes("sports")) {
    adContent += `sports enthusiasts! Whether you're on the field or hitting the gym, our ${product} will keep you at the top of your game. `
  }

  if (interestList.includes("music") || interestList.includes("ed sheeran")) {
    adContent += `music lovers! Inspired by the rhythm and style of artists like Ed Sheeran, our ${product} will hit all the right notes in your daily life. `
  }

  if (interestList.includes("cooking") || interestList.includes("healthy lifestyle")) {
    adContent += `health-conscious individuals! Perfect for preparing delicious and nutritious meals, our ${product} will revolutionize your cooking experience. `
  }

  adContent += `Elevate your ${interestList.join(" and ")} experience with our cutting-edge ${product}! Limited time offer - don't miss out!`

  return adContent
}

