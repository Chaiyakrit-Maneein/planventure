import React, { useState } from 'react';

function LoginForm({ onLogin, error }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <form onSubmit={(e) => onLogin(e, email, password)}>
      <input
        type='email'
        placeholder='Email'
        value={email}
        required
        onChange={(e) => setEmail(e.target.value)}
        style={{ width: '100%', marginBottom: 8 }}
      />
      <input
        type='password'
        placeholder='Password'
        value={password}
        required
        onChange={(e) => setPassword(e.target.value)}
        style={{ width: '100%', marginBottom: 8 }}
      />
      <button type='submit' style={{ width: '100%' }}>
        Login
      </button>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </form>
  );
}

export default LoginForm;
