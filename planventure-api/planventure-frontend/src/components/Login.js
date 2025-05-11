import React from 'react';

function Login({ email, setEmail, password, setPassword, handleLogin, loading, error }) {
  const styles = {
    input: {
      width: '100%',
      padding: '10px 12px',
      marginBottom: 12,
      borderRadius: 6,
      border: '1px solid #cbd5e1',
      fontSize: 16,
    },
    button: {
      padding: '8px 18px',
      background: 'linear-gradient(90deg,#4299e1,#3182ce)',
      color: '#fff',
      border: 'none',
      borderRadius: 6,
      fontWeight: 600,
      fontSize: 15,
      cursor: 'pointer',
      marginRight: 6,
    },
    error: {
      color: '#e53e3e',
      marginTop: 8,
      textAlign: 'center',
    },
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        style={styles.input}
        type='email'
        placeholder='Email'
        value={email}
        required
        onChange={(e) => setEmail(e.target.value)}
        autoComplete='username'
      />
      <input
        style={styles.input}
        type='password'
        placeholder='Password'
        value={password}
        required
        onChange={(e) => setPassword(e.target.value)}
        autoComplete='current-password'
      />
      <button style={styles.button} type='submit' disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
      {error && <div style={styles.error}>{error}</div>}
    </form>
  );
}

export default Login;
