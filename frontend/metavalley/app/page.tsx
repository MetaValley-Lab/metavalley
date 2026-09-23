import { Footer, FeaturesSection, FinalCta, HowItWorksSection, Logos, PricingSection, ProblemSection, SolutionSection, TestimonialSection } from "@/features/landing/landing-sections";
import { LandingEffects, Header, Hero } from "@/features/landing/landing-shell";

export default function Home() {
  return <main className="min-h-screen overflow-hidden bg-[#08080A] text-[#F0F0F2]"><LandingEffects /><Header /><Hero /><Logos /><ProblemSection /><SolutionSection /><HowItWorksSection /><FeaturesSection /><TestimonialSection /><PricingSection /><FinalCta /><Footer /></main>;
}
