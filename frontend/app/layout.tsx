import './globals.css'

export const metadata = {
  title: 'AI Risk Intelligence Platform',
  description: 'Human-in-the-loop Trust & Safety risk intelligence prototype',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
