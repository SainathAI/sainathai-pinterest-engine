const niches = [
  "Motivation",
  "Health Tips",
  "Technology",
  "Business Quotes",
  "Mindset",
  "Fitness",
  "AI Tools"
];

let index = 0;

export function getNextNiche() {
  const niche = niches[index];
  index = (index + 1) % niches.length;
  return niche;
}
