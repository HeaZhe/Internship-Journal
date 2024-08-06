import React from 'react';

const LineLoginButton = () => {
    const handleLogin = (event) => {
        event.preventDefault(); // 防止表單提交
        window.location.href = 'http://127.0.0.1:8000/api/line/login/';
    };

    return (
        <button type="button" onClick={handleLogin}>使用 Line 登入</button>
    );
};

export default LineLoginButton;
