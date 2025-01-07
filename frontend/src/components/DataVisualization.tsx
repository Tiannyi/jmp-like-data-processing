import React from 'react';
import Plot from 'react-plotly.js';
import { Box, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { Data } from 'plotly.js';

interface DataRow {
  [key: string]: any;
}

interface Column {
  id: string;
  type: 'number' | 'string' | 'date';
}

interface DataState {
  data: DataRow[];
  columns: Column[];
}

const DataVisualization: React.FC = () => {
  const { data, columns }: DataState = useSelector((state: RootState) => state.data);
  const [chartType, setChartType] = React.useState<'scatter'|'histogram'|'box'>('scatter');
  const [xAxis, setXAxis] = React.useState<string>('');
  const [yAxis, setYAxis] = React.useState<string>('');

  React.useEffect(() => {
    if (columns.length > 0) {
      setXAxis(columns[0].id);
      setYAxis(columns[1]?.id || columns[0].id);
    }
  }, [columns]);

  const getPlotData = (): Data[] => {
    if (!data || !xAxis || !yAxis) return [];

    switch (chartType) {
      case 'scatter':
        return [{
          x: data.map((row: DataRow) => row[xAxis]),
          y: data.map((row: DataRow) => row[yAxis]),
          mode: 'markers',
          type: 'scatter' as const,
          marker: { color: '#1976d2' }
        }];
      case 'histogram':
        return [{
          x: data.map((row: DataRow) => row[xAxis]),
          type: 'histogram' as const,
          marker: { color: '#1976d2' }
        }];
      case 'box':
        return [{
          y: data.map((row: DataRow) => row[yAxis]),
          type: 'box' as const,
          name: yAxis,
          boxpoints: 'outliers'
        }];
      default:
        return [];
    }
  };

  return (
    <div>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Chart Type</InputLabel>
          <Select
            value={chartType}
            label="Chart Type"
            onChange={(e) => setChartType(e.target.value as 'scatter'|'histogram'|'box')}
          >
            <MenuItem value="scatter">Scatter</MenuItem>
            <MenuItem value="histogram">Histogram</MenuItem>
            <MenuItem value="box">Box</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>X Axis</InputLabel>
          <Select
            value={xAxis}
            label="X Axis"
            onChange={(e) => setXAxis(e.target.value)}
          >
            {columns.map((col: Column) => (
              <MenuItem key={col.id} value={col.id}>{col.id}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Y Axis</InputLabel>
          <Select
            value={yAxis}
            label="Y Axis"
            onChange={(e) => setYAxis(e.target.value)}
          >
            {columns.map((col: Column) => (
              <MenuItem key={col.id} value={col.id}>{col.id}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      <Box sx={{ width: '100%', height: '400px' }}>
        <Plot
          data={getPlotData()}
          layout={{
            title: `${chartType.charAt(0).toUpperCase() + chartType.slice(1)} Plot`,
            xaxis: { title: xAxis },
            yaxis: { title: yAxis },
            width: undefined,
            height: undefined,
            autosize: true
          }}
          style={{ width: '100%', height: '100%' }}
          useResizeHandler={true}
        />
      </Box>
    </div>
  );
};

export default DataVisualization;
