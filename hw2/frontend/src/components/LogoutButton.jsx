import React from 'react';

const LineLoginButton = () => {
    const handleLogin = (event) => {
        event.preventDefault(); // 防止表單提交
        window.location.href = 'http://localhost:5173/logout';
    };

    return (
        <button type="button" onClick={handleLogin}>Logout</button>
    );
};

export default LineLoginButton;
