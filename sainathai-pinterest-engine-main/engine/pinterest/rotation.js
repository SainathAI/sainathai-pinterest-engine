const niches = [
  "Mindset & Motivation",
  "Business & Entrepreneurship",
  "AI Tools & Automation",
  "Health & Fitness Tips"
];

let index = 0;

export function getNextNiche() {
  const niche = niches[index];
  index = (index + 1) % niches.length;
  return niche;
}
