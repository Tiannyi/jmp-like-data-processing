import React from 'react';
import { Box, Container, CssBaseline, AppBar, Toolbar, Typography, Grid, Paper } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import DataImport from './components/DataImport';
import DataTable from './components/DataTable';
import DataVisualization from './components/DataVisualization';
import { Provider } from 'react-redux';
import { store } from './store/store';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                JMP-like Data Processing
              </Typography>
            </Toolbar>
          </AppBar>
          
          <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper sx={{ p: 2 }}>
                  <Grid container spacing={3}>
                    <Grid item xs={12}>
                      <DataImport />
                    </Grid>
                    
                    <Grid item xs={12}>
                      <DataTable />
                    </Grid>
                    
                    <Grid item xs={12} md={6}>
                      <DataVisualization />
                    </Grid>
                    
                    <Grid item xs={12} md={6}>
                      <DataVisualization />
                    </Grid>
                  </Grid>
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </ThemeProvider>
    </Provider>
  );
};

export default App;
