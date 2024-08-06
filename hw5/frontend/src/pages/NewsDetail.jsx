import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Typography, Box } from '@mui/material';
import Nav from '../components/Navbar';

function NewsDetail() {
    const { id } = useParams();
    const [newsItem, setNewsItem] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchNewsDetail = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/news/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                const item = data.find(news => news.id.toString() === id);
                setNewsItem(item);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching news detail:', error);
                setLoading(false);
            }
        };

        fetchNewsDetail();
    }, [id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!newsItem) {
        return <div>News not found</div>;
    }

    return (
        <Container>
            <Nav />
            <Box m={10}>
                <Typography variant="h4" gutterBottom>{newsItem.title}</Typography>
            </Box>
            <Box m={10}>
                <Typography variant="body1" gutterBottom>
                    {newsItem.content.split('\n').map((line, index) => (
                            <React.Fragment key={index}>
                                {line}
                                <br />
                            </React.Fragment>
                ))}</Typography>
            </Box>
            <Box m={10}>
                <Typography variant="body2" color="textSecondary">{new Date(newsItem.datetime).toLocaleString()}</Typography>
            </Box>
        </Container>
    );
}

export default NewsDetail;
