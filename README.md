# JMP-like Data Processing Application

A modern web application for data processing and visualization, similar to JMP, built with React and FastAPI.

## Quick Start

Simply run one of these commands:
```bash
# First time setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

# Run the application
python run.py
```

This will:
1. Start the FastAPI backend server on port 8000
2. Start the React development server on port 3000

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

To stop the application, press `Ctrl+C` in the terminal.

## Features

- Data import/export (CSV, Excel)
- Interactive data table with sorting and pagination
- Real-time data visualization with multiple chart types:
  - Scatter plots
  - Histograms
  - Box plots
- Modern dark theme UI
- Redux state management for predictable data flow
- TypeScript for better type safety

## Project Structure

```
project_root/
├── backend/          # Python FastAPI backend
│   ├── app.py       # Main FastAPI application
│   └── requirements.txt
├── frontend/        # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── store/      # Redux store and slices
│   │   └── App.tsx     # Main application component
│   ├── package.json
│   └── tsconfig.json
└── run.py          # Application runner script
```

## State Management

The application uses Redux for state management with the following structure:

```typescript
interface DataState {
  data: Record<string, any>[];  // The actual data rows
  columns: {
    id: string;
    type: 'number' | 'string' | 'date';
  }[];
  loading: boolean;
  error: string | null;
}
```

## Development

### Backend API Endpoints

- `POST /upload`: Upload and process data files
- `GET /health`: Health check endpoint

### Frontend Components

- `DataImport`: File upload component with drag-and-drop support
- `DataTable`: Interactive data grid with pagination
- `DataVisualization`: Interactive charts with multiple visualization options

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License
