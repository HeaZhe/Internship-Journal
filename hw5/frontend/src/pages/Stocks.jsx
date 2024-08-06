import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Container, Button, CircularProgress } from '@mui/material';
import { format } from 'date-fns';
import '../styles/Stocks.css';
import Nav from '../components/Navbar';

function Stocks() {
    const [latest_rows, setLatestRows] = useState([]);
    const [history_rows, setHistoryRows] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showLatest, setShowLatest] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/stocks_latest/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log('從 API 獲取的數據:', data);

                const processedData = data.map(item => ({
                    ...item,
                    change: item.change !== null ? item.change : '-',
                    change_percent: item.change_percent !== null ? item.change_percent : '-',
                    price: item.price !== null ? item.price : '-',
                }));

                setLatestRows(processedData);
            } catch (error) {
                console.error('獲取數據時出錯:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        if (!showLatest) {
            const fetchHistoryData = async () => {
                setLoading(true);
                try {
                    const response = await fetch('http://127.0.0.1:8000/api/stocks_history/');
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    const data = await response.json();
                    console.log('從 API 獲取的歷史數據:', data);

                    const processedData = data.map(item => ({
                        ...item,
                        change: item.change !== null ? item.change : '-',
                        change_percent: item.change_percent !== null ? item.change_percent : '-',
                        price: item.price !== null ? item.price : '-',
                        fetch_at: item.fetch_at ? format(new Date(item.fetch_at), 'yyyy-MM-dd HH:mm') : '-'
                    }));

                    // 按照 fetch_at 進行排序
                    processedData.sort((a, b) => new Date(b.fetch_at) - new Date(a.fetch_at));

                    setHistoryRows(processedData);
                } catch (error) {
                    console.error('獲取歷史數據時出錯:', error);
                } finally {
                    setLoading(false);
                }
            };

            fetchHistoryData();
        }
    }, [showLatest]);

    const handleToggle = () => {
        setShowLatest(!showLatest);
    };

    const updateData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/start_scraper/', {
                method: 'POST',
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log('爬蟲成功啟動');
            // 可以在這裡添加更強大的數據獲取或輪詢方法
            setShowLatest(!showLatest); // 重新載入數據
        } catch (error) {
            console.error('啟動爬蟲時出錯:', error);
        }
    };

    const columns = [
        { field: 'name', headerName: 'Name', width: 80, cellClassName: 'left-align', headerAlign: 'left' },
        { field: 'code', headerName: 'Code', width: 300, headerAlign: 'left' },
        { field: 'price', headerName: 'Price', width: 100, renderCell: (params) => <div className="center-align">{params.value}</div>, headerAlign: 'center' },
        { field: 'change', headerName: 'Change', width: 100, renderCell: (params) => <div className="center-align">{params.value}</div>, headerAlign: 'center' },
        { field: 'change_percent', headerName: 'Change Percent', width: 150, renderCell: (params) => <div className="center-align">{params.value}</div>, headerAlign: 'center' },
        ...(showLatest ? [] : [{ field: 'fetch_at', headerName: 'Fetch at', width: 200, renderCell: (params) => <div className="center-align">{params.value}</div>, headerAlign: 'center' }]),
    ];

    return (
        <Container>
            <Nav />
            <h1>股票數據表格範例</h1>
            <Button variant="contained" onClick={handleToggle} style={{ marginBottom: 20 }}>
                {showLatest ? '顯示歷史' : '顯示最新'}
            </Button>
            <Button variant="contained" onClick={updateData} style={{ marginBottom: 20, marginLeft: 10 }}>
                更新數據
            </Button>
            {loading ? (
                <CircularProgress />
            ) : (
                <div style={{ height: 600, width: '100%' }}>
                    <DataGrid
                        rows={showLatest ? latest_rows : history_rows}
                        columns={columns}
                        getRowId={(row) => row.id}
                        pageSize={5}
                        onRowClick={(row) => console.log('點擊的行:', row)}
                    />
                </div>
            )}
        </Container>
    );
}

export default Stocks;
