import React from 'react';

function TripList({ trips }) {
  return (
    <ul>
      {trips.map((trip) => (
        <li key={trip.id}>
          <b>{trip.name}</b> - {trip.description}
        </li>
      ))}
    </ul>
  );
}

export default TripList;
