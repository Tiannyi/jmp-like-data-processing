import React from 'react';
import { Button, Box } from '@mui/material';
import { useDispatch } from 'react-redux';
import { setData, setColumns } from '../store/store';

interface DataImportProps {
  onDataImported: (data: any) => void;
}

const DataImport: React.FC<DataImportProps> = () => {
  const dispatch = useDispatch();
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const result = await response.json();
      
      // Convert data to array of objects with column IDs as keys
      const data = result.data.map((row: any[]) => {
        const rowObj: Record<string, any> = {};
        result.columns.forEach((col: string, index: number) => {
          rowObj[col] = row[index];
        });
        return rowObj;
      });

      // Create column objects with id and type
      const columns = result.columns.map((col: string) => ({
        id: col,
        type: 'number' // You might want to infer this from the data
      }));

      dispatch(setData(data));
      dispatch(setColumns(columns));
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <Box sx={{ p: 2 }}>
      <input
        type="file"
        accept=".csv,.xlsx,.xls"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        ref={fileInputRef}
      />
      <Button
        variant="contained"
        onClick={handleClick}
        sx={{ mt: 2 }}
      >
        Import Data
      </Button>
    </Box>
  );
};

export default DataImport;
