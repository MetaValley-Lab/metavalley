import type { Metadata } from "next";
import { PrimeReactProvider } from 'primereact/api';
import { Google_Sans_Flex } from "next/font/google";
import "./globals.css";


export const metadata: Metadata = {
  title: "MetaValley — Valide sua ideia antes de construí-la",
  description: "Um board executivo de IA com CEO, CTO, CFO e CMO para validar sua startup antes de gastar tempo e dinheiro construindo.",
  keywords: ["startup", "validação", "IA", "inteligência artificial", "founders", "business model", "MetaValley",],
  openGraph: {
    title: "MetaValley — Valide antes de construir",
    description:
      "Seu board executivo de IA para validar ideias de startup antes de construir.",
    type: "website",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "MetaValley",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "MetaValley — Valide antes de construir",
    description:
      "Seu board executivo de IA para validar ideias de startup antes de construir.",
    images: ["/og-image.png"],
  },
};

const googleSansFlex = Google_Sans_Flex({
  variable: "--font-google-sans-flex",
  subsets: ["latin", "latin-ext"],
  weight: "variable",
});


export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR" className={`${googleSansFlex.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">
        <PrimeReactProvider>
            {children}
        </PrimeReactProvider>
      </body>
    </html>
  );
}
