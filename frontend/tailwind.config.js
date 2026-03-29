/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#f2c062',
          container: '#d4a54a',
          'fixed-dim': '#dec396',
        },
        on: {
          primary: '#412d00',
          surface: '#e5e2e1',
        },
        surface: {
          DEFAULT: '#131313',
          dim: '#131313',
          lowest: '#0e0e0e',
          low: '#1c1b1b',
          high: '#2a2a29',
          highest: '#353534',
          bright: 'rgba(255, 255, 255, 0.1)', // semi-transparent
        },
        outline: {
          variant: 'rgba(255, 255, 255, 0.2)', // 20% opacity
          ghost: 'rgba(255, 255, 255, 0.15)', // 15% opacity
        }
      },
      fontFamily: {
        serif: ['"Playfair Display"', '"Noto Serif"', 'serif'],
        sans: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 24px 0 rgba(242, 192, 98, 0.08)',
      },
      letterSpacing: {
        tightest: '-.02em',
        widest: '.1em', // 10%
      }
    },
  },
  plugins: [],
}
