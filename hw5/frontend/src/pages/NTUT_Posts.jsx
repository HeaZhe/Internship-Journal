import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, CircularProgress } from '@mui/material';
import Nav from '../components/Navbar';

function NTUT_Posts() {
    const [NTUT_PostsItem, setNTUT_Posts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/ntut_posts/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log('Data fetched from API:', data); // 查看數據格式

                setNTUT_Posts(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);
    return (
        <Container>
            <Nav />
            <Typography variant="h3" gutterBottom>NTUT Posts</Typography>
            {NTUT_PostsItem.map((post) => (
                <Box key={post.id} mb={2} p={2} border={1} borderColor="grey.300" borderRadius={4}>
                    <Typography variant="body1">
                        {post.context.split('\n').map((line, index) => (
                            <React.Fragment key={index}>
                                {line}
                                <br />
                            </React.Fragment>
                        ))}
                    </Typography>
                </Box>
            ))}
        </Container>
    );
}

export default NTUT_Posts;
