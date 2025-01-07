import pandas as pd
from typing import Dict, Any
from fastapi import UploadFile
import io

class DataImportService:
    @staticmethod
    async def import_csv(file: UploadFile) -> Dict[str, Any]:
        try:
            contents = await file.read()
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
            return {
                "success": True,
                "data": df.to_dict('records'),
                "columns": df.columns.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def import_excel(file: UploadFile) -> Dict[str, Any]:
        try:
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            return {
                "success": True,
                "data": df.to_dict('records'),
                "columns": df.columns.tolist()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    async def export_data(data: Dict[str, Any], format: str) -> bytes:
        df = pd.DataFrame(data["data"])
        buffer = io.BytesIO()
        
        if format.lower() == 'csv':
            df.to_csv(buffer, index=False)
        elif format.lower() == 'excel':
            df.to_excel(buffer, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        buffer.seek(0)
        return buffer.getvalue()
