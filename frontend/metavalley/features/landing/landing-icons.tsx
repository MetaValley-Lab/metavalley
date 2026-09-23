import type { ReactNode } from "react";

type IconProps = { size?: number; strokeWidth?: number };

type Icon = (props: IconProps) => ReactNode;

const stroke = (path: ReactNode, size: number) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true">
    {path}
  </svg>
);

const line = (d: string, strokeWidth = 1.6) => <path d={d} stroke="currentColor" strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" />;

export const icons: Record<string, Icon> = {
  arrow: ({ size = 18, strokeWidth = 1.8 }) => stroke(<>{line("M5 12h14M13 6l6 6-6 6", strokeWidth)}</>, size),
  play: ({ size = 18 }) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 5.5v13l10-6.5L8 5.5Z" fill="currentColor" /></svg>,
  clock: ({ size = 22 }) => stroke(<><circle cx="12" cy="12" r="8.5" stroke="currentColor" strokeWidth="1.6" />{line("M12 7v5l3.5 2")}</>, size),
  chartDown: ({ size = 22 }) => stroke(<>{line("M4 6v13h16")}{line("m7 9 3 3 3-4 4 3")}{line("m14 15 3 3 3-3")}</>, size),
  bulb: ({ size = 22 }) => stroke(<>{line("M9 18h6M10 21h4")}{line("M8.2 15.5C6.8 14.3 6 12.6 6 10.7a6 6 0 0 1 12 0c0 1.9-.8 3.6-2.2 4.8-.7.6-1.1 1.2-1.1 1.9h-5.4c0-.7-.4-1.3-1.1-1.9Z")}</>, size),
  message: ({ size = 22 }) => stroke(<>{line("M5 5.5h14v10H9l-4 3v-13Z")}{line("M8 9h8M8 12h5", 1.5)}</>, size),
  users: ({ size = 22 }) => stroke(<><circle cx="9" cy="8" r="3" stroke="currentColor" strokeWidth="1.6" />{line("M3.5 19c.5-3 2.3-4.5 5.5-4.5s5 1.5 5.5 4.5")}{line("M15 6.5a2.5 2.5 0 0 1 0 5M16 14.5c2.6.4 4 1.9 4.5 4.5")}</>, size),
  rocket: ({ size = 22 }) => stroke(<>{line("M14 4c3.8-.8 6 .2 6 .2s1 2.2.2 6c-.8 3.8-4.3 6.3-7.1 7.1l-4.2-4.2C9.7 10.3 12.2 4.8 14 4Z")}{line("m9 15-3 3M7 12l-3 1 1 3")}</>, size),
  grid: ({ size = 22 }) => stroke(<>{["4,4", "14,4", "4,14", "14,14"].map((point) => { const [x, y] = point.split(","); return <rect key={point} x={x} y={y} width="6" height="6" rx="1" stroke="currentColor" strokeWidth="1.5" />; })}</>, size),
  brain: ({ size = 22 }) => stroke(<>{line("M9 5.5a3 3 0 0 0-5 2.2A3.2 3.2 0 0 0 5.5 13 3.3 3.3 0 0 0 9 18.5M15 5.5a3 3 0 0 1 5 2.2 3.2 3.2 0 0 1-1.5 5.3 3.3 3.3 0 0 1-3.5 5.5")}{line("M9 5.5v13M15 5.5v13M9 10h6M9 14h6", 1.5)}</>, size),
  menu: ({ size = 24 }) => stroke(<>{line("M4 7h16M4 12h16M4 17h16", 1.7)}</>, size),
  close: ({ size = 24 }) => stroke(<>{line("m6 6 12 12M18 6 6 18", 1.7)}</>, size),
};
