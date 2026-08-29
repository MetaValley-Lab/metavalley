"use client";

import { useEffect, useState, type ReactNode } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

export interface CarouselSlide {
  id: string;
  content: ReactNode;
}

interface CarouselProps {
  slides: CarouselSlide[];
  intervalMs?: number;
}

export default function Carousel({ slides, intervalMs = 6000 }: CarouselProps) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (slides.length <= 1) return;
    const timer = setInterval(() => {
      setIndex((i) => (i + 1) % slides.length);
    }, intervalMs);
    return () => clearInterval(timer);
  }, [slides.length, intervalMs]);

  if (slides.length === 0) {
    return <div className="h-44 w-full rounded-md bg-[#D9D9D9] sm:h-56" />;
  }

  return (
    <div className="group relative h-44 w-full overflow-hidden rounded-md bg-[#D9D9D9] sm:h-56">
      {slides.map((slide, i) => (
        <div
          key={slide.id}
          className={`absolute inset-0 transition-opacity duration-500 ${
            i === index ? "opacity-100" : "pointer-events-none opacity-0"
          }`}
        >
          {slide.content}
        </div>
      ))}

      {slides.length > 1 && (
        <>
          <button
            type="button"
            onClick={() => setIndex((i) => (i - 1 + slides.length) % slides.length)}
            aria-label="Slide anterior"
            className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full bg-white/70 p-1 opacity-0 transition-opacity group-hover:opacity-100"
          >
            <ChevronLeft size={18} />
          </button>
          <button
            type="button"
            onClick={() => setIndex((i) => (i + 1) % slides.length)}
            aria-label="Próximo slide"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-white/70 p-1 opacity-0 transition-opacity group-hover:opacity-100"
          >
            <ChevronRight size={18} />
          </button>

          <div className="absolute bottom-2 left-1/2 flex -translate-x-1/2 gap-1.5">
            {slides.map((slide, i) => (
              <button
                key={slide.id}
                type="button"
                onClick={() => setIndex(i)}
                aria-label={`Ir para slide ${i + 1}`}
                className={`h-1.5 w-1.5 rounded-full ${i === index ? "bg-white" : "bg-white/50"}`}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

