import { configureStore, createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Column {
  id: string;
  type: 'number' | 'string' | 'date';
}

interface DataState {
  data: Record<string, any>[];
  columns: Column[];
  loading: boolean;
  error: string | null;
}

const initialState: DataState = {
  data: [],
  columns: [],
  loading: false,
  error: null,
};

const dataSlice = createSlice({
  name: 'data',
  initialState,
  reducers: {
    setData: (state, action: PayloadAction<Record<string, any>[]>) => {
      state.data = action.payload;
    },
    setColumns: (state, action: PayloadAction<Column[]>) => {
      state.columns = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { setData, setColumns, setLoading, setError } = dataSlice.actions;

export const store = configureStore({
  reducer: {
    data: dataSlice.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
