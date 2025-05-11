import React from 'react';

function TripForm({
  tripForm,
  handleTripFormChange,
  handleTripFormSubmit,
  editingTripId,
  loading,
  setEditingTripId,
  setTripForm,
  styles,
}) {
  return (
    <form onSubmit={handleTripFormSubmit} style={{ marginBottom: 24 }}>
      <div style={styles.formRow}>
        <input
          style={styles.input}
          type='text'
          name='name'
          placeholder='Trip Name'
          value={tripForm.name}
          required
          onChange={handleTripFormChange}
        />
        <input
          style={styles.input}
          type='text'
          name='destination'
          placeholder='Destination'
          value={tripForm.destination}
          required
          onChange={handleTripFormChange}
        />
      </div>
      <div style={styles.formRow}>
        <input
          style={styles.input}
          type='text'
          name='description'
          placeholder='Description'
          value={tripForm.description}
          onChange={handleTripFormChange}
        />
        <input
          style={styles.input}
          type='date'
          name='start_date'
          value={tripForm.start_date}
          required
          onChange={handleTripFormChange}
        />
        <input
          style={styles.input}
          type='date'
          name='end_date'
          value={tripForm.end_date}
          required
          onChange={handleTripFormChange}
        />
      </div>
      <button style={styles.button} type='submit' disabled={loading}>
        {editingTripId
          ? loading
            ? 'Updating...'
            : 'Update Trip'
          : loading
          ? 'Adding...'
          : 'Add Trip'}
      </button>
      {editingTripId && (
        <button
          type='button'
          style={{ ...styles.button, ...styles.dangerButton, width: 120 }}
          onClick={() => {
            setEditingTripId(null);
            setTripForm({
              name: '',
              destination: '',
              description: '',
              start_date: '',
              end_date: '',
            });
          }}
        >
          Cancel Edit
        </button>
      )}
    </form>
  );
}

export default TripForm;
