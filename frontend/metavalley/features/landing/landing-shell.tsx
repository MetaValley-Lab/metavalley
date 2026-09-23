"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { agents } from "./landing-data";
import { icons } from "./landing-icons";

export function LandingEffects() {
  useEffect(() => {
    const onScroll = () => document.querySelector("header")?.classList.toggle("is-scrolled", window.scrollY > 20);
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => entry.isIntersecting && entry.target.classList.add("is-visible")), { threshold: 0.08, rootMargin: "0px 0px -50px 0px" });
    const cursor = document.querySelector<HTMLElement>(".custom-cursor");
    const moveCursor = (event: MouseEvent) => { if (cursor) cursor.style.transform = `translate3d(${event.clientX}px, ${event.clientY}px, 0)`; };
    window.addEventListener("scroll", onScroll);
    document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
    window.addEventListener("mousemove", moveCursor);
    return () => { window.removeEventListener("scroll", onScroll); window.removeEventListener("mousemove", moveCursor); observer.disconnect(); };
  }, []);
  return <div className="custom-cursor pointer-events-none fixed left-0 top-0 z-[100] hidden h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#7F77DD] opacity-70 md:block" />;
}

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const links = [["Como funciona", "#como-funciona"], ["Funcionalidades", "#funcionalidades"], ["Preços", "#precos"]];
  return (
    <header className="landing-header fixed left-0 top-0 z-50 w-full border-b border-transparent bg-transparent transition-all duration-300">
      <div className="mx-auto flex h-[76px] max-w-[1240px] items-center justify-between px-5 lg:px-8">
        <a href="#" className="group flex items-center gap-1.5">
          <span className="font-display text-xl font-extrabold tracking-[-0.04em] text-[#A39DF0]">MetaValley</span>
          <span className="relative h-2 w-2"><span className="absolute inset-0 animate-ping rounded-full bg-[#22C55E] opacity-50" /><span className="relative block h-2 w-2 rounded-full bg-[#22C55E]" /></span>
        </a>
        <nav className="hidden items-center gap-8 md:flex">{links.map(([label, href]) => <a key={href} href={href} className="nav-link">{label}</a>)}</nav>
        <div className="hidden items-center gap-3 md:flex"><Link href="/auth/login" className="ghost-button">Entrar</Link><Link href="/auth/register" className="primary-button">Começar grátis</Link></div>
        <button className="cursor-pointer rounded-lg border border-white/10 p-2 md:hidden" onClick={() => setMobileOpen((open) => !open)} aria-label={mobileOpen ? "Fechar menu" : "Abrir menu"}>{mobileOpen ? icons.close({}) : icons.menu({})}</button>
      </div>
      {mobileOpen && <div className="border-t border-white/[0.06] bg-[#08080A]/95 px-5 py-6 backdrop-blur-xl md:hidden"><div className="flex flex-col gap-5">{links.map(([label, href]) => <a key={href} onClick={() => setMobileOpen(false)} href={href} className="nav-link">{label}</a>)}<div className="mt-2 flex gap-3"><Link href="/auth/login" className="ghost-button flex-1">Entrar</Link><Link href="/auth/register" className="primary-button flex-1">Começar grátis</Link></div></div></div>}
    </header>
  );
}

export function Hero() {
  return <section className="relative isolate flex min-h-screen items-center pt-24"><div className="mesh-bg absolute inset-0 -z-10" /><div className="hero-grid absolute inset-0 -z-10 opacity-30" />{[1, 2, 3, 4].map((number) => <div key={number} className={`particle particle-${number}`} />)}<div className="mx-auto grid w-full max-w-[1240px] gap-16 px-5 py-20 lg:grid-cols-[0.95fr_1.05fr] lg:items-center lg:px-8 lg:py-28"><div><div className="reveal mb-7 inline-flex items-center gap-2 rounded-full border border-[#7F77DD]/20 bg-[#7F77DD]/[0.06] px-3 py-1.5"><span className="h-1.5 w-1.5 rounded-full bg-[#22C55E]" /><span className="font-mono text-[10px] uppercase tracking-[0.18em] text-[#A9A5D9]">Executive Intelligence Platform</span></div><h1 className="reveal hero-title max-w-[850px] font-display text-[48px] font-black leading-[0.98] tracking-[-0.055em] md:text-[68px] lg:text-[86px]">Valide sua ideia<br /><span className="gradient-text">antes de construí-la.</span></h1><p className="reveal delay-100 mt-7 max-w-[650px] text-[16px] leading-7 text-[#888892] md:text-[18px]">Um board executivo de IA com CEO, CTO, CFO e CMO debate sua ideia com você — e entrega dados de mercado antes de você gastar R$1 construindo algo que ninguém quer.</p><div className="reveal delay-200 mt-9 flex flex-col gap-3 sm:flex-row"><Link href="/auth/register" className="primary-button large-button group">Acessar o beta gratuito <span className="transition-transform group-hover:translate-x-1">{icons.arrow({})}</span></Link><a href="#como-funciona" className="secondary-button large-button"><span className="flex h-7 w-7 items-center justify-center rounded-full bg-white/[0.08]">{icons.play({ size: 13 })}</span>Ver como funciona</a></div><p className="reveal delay-300 mt-8 text-xs text-[#555560]">Fundadores de São Paulo, Recife, Aracaju e mais 12 estados já estão usando ↗</p></div><ChatPreview /></div></section>;
}

function ChatPreview() {
  return <div className="reveal delay-200 relative mx-auto w-full max-w-[600px] lg:ml-auto"><div className="board-badge absolute -top-5 left-1/2 z-20 -translate-x-1/2 whitespace-nowrap"><span className="h-2 w-2 animate-pulse rounded-full bg-[#22C55E]" />Board ativo: CEO • CFO • CTO • CMO</div><div className="chat-glow absolute -inset-10 -z-10" /><div className="chat-window"><div className="flex items-center justify-between border-b border-white/[0.06] px-5 py-4"><div className="flex items-center gap-3"><div className="flex -space-x-2">{agents.map((agent) => <div key={agent.name} className="agent-avatar" style={{ borderColor: agent.color, color: agent.color }}>{agent.name[0]}</div>)}</div><div><div className="text-xs font-semibold">Board Executivo</div><div className="mt-0.5 text-[10px] text-[#555560]">4 agentes online</div></div></div><span className="font-mono text-[9px] uppercase tracking-wider text-[#555560]">LIVE</span></div><div className="space-y-4 p-5"><div className="flex justify-end"><div className="max-w-[85%] rounded-2xl rounded-br-md border border-white/[0.06] bg-white/[0.045] px-4 py-3 text-[13px] leading-5 text-[#C6C6CC]">Minha ideia é uma plataforma que valida startups com IA.</div></div><div className="flex items-start gap-3"><div className="agent-small bg-[#7F77DD]/10 text-[#9B94F2]">C</div><div className="max-w-[85%]"><div className="mb-1.5 flex items-center gap-2"><span className="text-[11px] font-semibold text-[#9B94F2]">CEO Agent</span><span className="text-[9px] text-[#444450]">agora</span></div><div className="rounded-2xl rounded-tl-md border border-[#7F77DD]/10 bg-[#7F77DD]/[0.055] px-4 py-3 text-[13px] leading-5 text-[#B9B8C3]">Boa pergunta de entrada. Qual o CAC estimado no seu modelo?<span className="typing-cursor ml-1" /></div></div></div><div className="flex items-start gap-3 opacity-50"><div className="agent-small bg-[#0891B2]/10 text-[#0891B2]">T</div><div className="flex items-center gap-2 rounded-2xl rounded-tl-md border border-[#0891B2]/10 bg-[#0891B2]/[0.04] px-4 py-3"><span className="thinking-dot" /><span className="thinking-dot animation-delay-100" /><span className="thinking-dot animation-delay-200" /></div></div></div><div className="border-t border-white/[0.06] p-4"><div className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-[#0D0D10] px-4 py-3"><span className="text-[11px] text-[#444450]">Converse com seu board...</span><span className="text-[#555560]">{icons.arrow({ size: 15 })}</span></div></div></div></div>;
}
