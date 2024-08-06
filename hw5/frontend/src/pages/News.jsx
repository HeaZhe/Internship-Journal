import React, { useState, useEffect } from 'react';
import { Container, List, ListItem, ListItemText, ListItemButton } from '@mui/material';
import { Link } from 'react-router-dom';
import Nav from '../components/Navbar';

function News() {
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/news/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log('Data fetched from API:', data); // 查看數據格式

                // 按日期排序
                const sortedData = data.sort((a, b) => new Date(b.datetime) - new Date(a.datetime));
                setNews(sortedData);
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
            <List>
                {news.map((item) => (
                    <ListItem key={item.id} disablePadding>
                        <ListItemButton component={Link} to={`/news/${item.id}`}>
                            <ListItemText primary={item.title} secondary={new Date(item.datetime).toLocaleString()} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </Container>
    );
}

export default News;
