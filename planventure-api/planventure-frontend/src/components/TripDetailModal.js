import React from 'react';

function TripDetailModal({ selectedTrip, tripDetail, handleCloseDetail, styles }) {
  return (
    <div style={styles.detailModal} onClick={handleCloseDetail}>
      <div style={styles.detailContent} onClick={(e) => e.stopPropagation()}>
        <button style={styles.closeBtn} onClick={handleCloseDetail} title='Close'>
          &times;
        </button>
        <h3 style={{ color: '#2b6cb0', marginBottom: 10 }}>Trip Details</h3>
        {!tripDetail ? (
          <div style={{ color: '#718096' }}>Loading...</div>
        ) : (
          <div>
            <div>
              <b>Name:</b>{' '}
              {tripDetail.name !== undefined && tripDetail.name !== null
                ? tripDetail.name
                : '-'}
            </div>
            <div>
              <b>Description:</b>{' '}
              {tripDetail.description !== undefined && tripDetail.description !== null
                ? tripDetail.description
                : '-'}
            </div>
            <div>
              <b>Destination:</b>{' '}
              {tripDetail.destination !== undefined && tripDetail.destination !== null
                ? tripDetail.destination
                : '-'}
            </div>
            <div>
              <b>Start Date:</b>{' '}
              {tripDetail.start_date !== undefined && tripDetail.start_date !== null
                ? tripDetail.start_date
                : '-'}
            </div>
            <div>
              <b>End Date:</b>{' '}
              {tripDetail.end_date !== undefined && tripDetail.end_date !== null
                ? tripDetail.end_date
                : '-'}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default TripDetailModal;
