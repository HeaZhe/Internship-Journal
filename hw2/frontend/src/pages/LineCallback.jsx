// LineCallback.js
import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const LineCallback = () => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const accessToken = params.get('access_token');
        const refreshToken = params.get('refresh_token');

        console.log('Access Token:', accessToken);
        console.log('Refresh Token:', refreshToken);

        if (accessToken && refreshToken) {
            // 保存 token 到 local storage 或應用程序狀態
            localStorage.setItem('access', accessToken);
            localStorage.setItem('refresh', refreshToken);
            window.location.href = 'http://localhost:5173/';
        }
    }, [location, navigate]);

    return <div>加載中...</div>;
};

export default LineCallback;