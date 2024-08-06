import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
return (
    <AppBar position="static">
        <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            MyApp
        </Typography>
        <Button color="inherit" component={RouterLink} to="/stocks">
        Stocks
        </Button>
        <Button color="inherit" component={RouterLink} to="/news">
        News
        </Button>
        <Button color="inherit" component={RouterLink} to="/ntut_posts">
        NTUT Posts
        </Button>
        </Toolbar>
    </AppBar>
);
}

export default Navbar;
