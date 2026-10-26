# Frontend

This is the Next.js frontend for PromptOS. It provides the workspace-style UI for entering prompts, viewing optimization progress, and reviewing optimized outputs.

## Features

- Prompt input and formatting controls
- Real-time processing state and progress updates
- Pipeline visualization for each optimization step
- Prompt scoring and token usage feedback
- Prompt history view

## Tech Stack

- Next.js
- React
- Tailwind CSS
- Zustand for state management
- Framer Motion for UI transitions

## Setup

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## Available Scripts

- npm run dev — start the development server
- npm run build — create a production build
- npm run start — run the production build
- npm run lint — run ESLint

## Notes

The frontend expects the backend API to be running on http://localhost:8000.

