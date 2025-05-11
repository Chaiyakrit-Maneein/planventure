import React from 'react';

function TripActions({ onLogout, onRefresh, error }) {
  return (
    <div>
      <button onClick={onLogout}>Logout</button>
      <h3>Your Trips</h3>
      <button onClick={onRefresh}>Refresh</button>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
    </div>
  );
}

export default TripActions;
