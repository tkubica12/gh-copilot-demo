# Toy Service Web Application

Modern React frontend for the Toy Service application.

## Features

- Browse toy catalog with grid layout
- View toy details
- Edit toy information (name, description)
- Upload/delete toy avatars
- Responsive design with Tailwind CSS
- TypeScript for type safety

## Prerequisites

- Node.js 18+ and npm
- Toy Service backend running on http://localhost:8001

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. (Optional) Create `.env` file for custom configuration:
```bash
VITE_TOY_SERVICE_URL=http://localhost:8001
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
src/
├── config/          # Configuration files (API)
├── components/      # Reusable components
├── pages/           # Page components
├── routes/          # Route configuration
├── services/        # API clients
├── types/           # TypeScript type definitions
└── main.tsx         # Application entry point
```

## Environment Variables

- `VITE_TOY_SERVICE_URL` - Backend API base URL (default: http://localhost:8001)
