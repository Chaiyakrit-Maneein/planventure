import React, { useState } from 'react';
import axios from 'axios';
import Login from './components/Login';
import TripForm from './components/TripForm';
import TripTable from './components/TripTable';
import TripDetailModal from './components/TripDetailModal';

const API_URL = 'http://localhost:5000';

const styles = {
  container: {
    maxWidth: 900,
    margin: '2rem auto',
    fontFamily: 'Segoe UI, Arial, sans-serif',
    background: '#f9fafb',
    borderRadius: 12,
    boxShadow: '0 2px 16px #0001',
    padding: 32,
  },
  title: {
    textAlign: 'center',
    marginBottom: 24,
    color: '#2d3748',
  },
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
  dangerButton: {
    background: 'linear-gradient(90deg,#e53e3e,#c53030)',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginBottom: 24,
    background: '#fff',
    borderRadius: 8,
    overflow: 'hidden',
    boxShadow: '0 1px 4px #0001',
  },
  th: {
    background: '#edf2f7',
    color: '#2d3748',
    fontWeight: 700,
    padding: '12px 8px',
    borderBottom: '1px solid #e2e8f0',
    textAlign: 'left',
  },
  td: {
    padding: '10px 8px',
    borderBottom: '1px solid #f1f1f1',
    fontSize: 15,
    color: '#4a5568',
  },
  actionsTd: {
    minWidth: 180,
    display: 'flex',
    gap: 6,
  },
  formRow: {
    display: 'flex',
    gap: 12,
    marginBottom: 12,
  },
  error: {
    color: '#e53e3e',
    marginTop: 8,
    textAlign: 'center',
  },
  detailModal: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0,0,0,0.25)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  },
  detailContent: {
    background: '#fff',
    borderRadius: 10,
    padding: 28,
    minWidth: 320,
    maxWidth: 400,
    boxShadow: '0 4px 32px #0002',
    position: 'relative',
  },
  closeBtn: {
    position: 'absolute',
    top: 10,
    right: 14,
    background: 'none',
    border: 'none',
    fontSize: 22,
    color: '#888',
    cursor: 'pointer',
  },
};

function App() {
  const [token, setToken] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [trips, setTrips] = useState([]);
  const [error, setError] = useState('');
  const [selectedTrip, setSelectedTrip] = useState(null);
  const [tripDetail, setTripDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tripForm, setTripForm] = useState({
    name: '',
    destination: '',
    description: '',
    start_date: '',
    end_date: '',
  });
  const [editingTripId, setEditingTripId] = useState(null);

  // Login handler
  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/auth/login`, { email, password });
      setToken(res.data.token);
      setEmail('');
      setPassword('');
      fetchTrips(res.data.token);
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    }
    setLoading(false);
  };

  // Fetch all trips
  const fetchTrips = async (jwt) => {
    setError('');
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/api/trips`, {
        headers: { Authorization: `Bearer ${jwt || token}` },
      });
      setTrips(res.data.trips);
    } catch (err) {
      setError('Failed to fetch trips');
    }
    setLoading(false);
  };

  // Fetch trip detail
  const fetchTripDetail = async (tripId) => {
    setError('');
    setTripDetail(null);
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/api/trips/${tripId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTripDetail(res.data.trip);
    } catch (err) {
      setError('Failed to fetch trip details');
    }
    setLoading(false);
  };

  // Add or update trip
  const handleTripFormSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (editingTripId) {
        // Update
        await axios.put(`${API_URL}/api/trips/${editingTripId}`, tripForm, {
          headers: { Authorization: `Bearer ${token}` },
        });
      } else {
        // Add
        await axios.post(`${API_URL}/api/trips`, tripForm, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      setTripForm({
        name: '',
        destination: '',
        description: '',
        start_date: '',
        end_date: '',
      });
      setEditingTripId(null);
      fetchTrips();
    } catch (err) {
      setError(
        err.response?.data?.error?.message ||
          err.response?.data?.message ||
          'Failed to save trip'
      );
    }
    setLoading(false);
  };

  // Edit trip
  const handleEditTrip = (trip) => {
    setEditingTripId(trip.id);
    setTripForm({
      name: trip.name || '',
      destination: trip.destination || '',
      description: trip.description || '',
      start_date: trip.start_date || '',
      end_date: trip.end_date || '',
    });
  };

  // Delete trip
  const handleDeleteTrip = async (tripId) => {
    if (!window.confirm('Are you sure you want to delete this trip?')) return;
    setError('');
    setLoading(true);
    try {
      await axios.delete(`${API_URL}/api/trips/${tripId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchTrips();
    } catch (err) {
      setError('Failed to delete trip');
    }
    setLoading(false);
  };

  // Show trip detail modal
  const handleViewDetails = (trip) => {
    setSelectedTrip(trip);
    fetchTripDetail(trip.id);
  };

  // Hide trip detail modal
  const handleCloseDetail = () => {
    setSelectedTrip(null);
    setTripDetail(null);
  };

  // Logout
  const handleLogout = () => {
    setToken('');
    setTrips([]);
    setSelectedTrip(null);
    setTripDetail(null);
    setError('');
  };

  // Handle trip form input
  const handleTripFormChange = (e) => {
    setTripForm({ ...tripForm, [e.target.name]: e.target.value });
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Planventure</h2>
      {!token ? (
        <Login
          email={email}
          setEmail={setEmail}
          password={password}
          setPassword={setPassword}
          handleLogin={handleLogin}
          loading={loading}
          error={error}
        />
      ) : (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
            <button
              style={{ ...styles.button, width: 100, marginBottom: 0, background: '#e53e3e' }}
              onClick={handleLogout}
            >
              Logout
            </button>
            <button
              style={{ ...styles.button, width: 100, marginBottom: 0, background: '#38b2ac' }}
              onClick={() => fetchTrips()}
            >
              {loading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
          <h3 style={{ color: '#2d3748', marginBottom: 18 }}>Your Trips</h3>
          <TripForm
            tripForm={tripForm}
            handleTripFormChange={handleTripFormChange}
            handleTripFormSubmit={handleTripFormSubmit}
            editingTripId={editingTripId}
            loading={loading}
            setEditingTripId={setEditingTripId}
            setTripForm={setTripForm}
            styles={styles}
          />
          <div style={{ overflowX: 'auto' }}>
            <TripTable
              trips={trips}
              handleViewDetails={handleViewDetails}
              handleEditTrip={handleEditTrip}
              handleDeleteTrip={handleDeleteTrip}
              styles={styles}
            />
          </div>
          {error && <div style={styles.error}>{error}</div>}
        </div>
      )}

      {/* Trip Detail Modal */}
      {selectedTrip && (
        <TripDetailModal
          selectedTrip={selectedTrip}
          tripDetail={tripDetail}
          handleCloseDetail={handleCloseDetail}
          styles={styles}
        />
      )}
    </div>
  );
}

export default App;
