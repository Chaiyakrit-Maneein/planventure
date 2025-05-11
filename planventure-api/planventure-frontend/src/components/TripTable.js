import React from 'react';
import DataTable from 'react-data-table-component';

function TripTable({ trips, handleViewDetails, handleEditTrip, handleDeleteTrip, styles }) {
  const columns = [
    {
      name: 'Name',
      selector: (row) => row.name ?? '-',
      sortable: true,
    },
    {
      name: 'Destination',
      selector: (row) => row.destination ?? '-',
      sortable: true,
    },
    {
      name: 'Description',
      selector: (row) => row.description ?? '-',
      sortable: false,
      grow: 2,
    },
    {
      name: 'Start Date',
      selector: (row) => row.start_date ?? '-',
      sortable: true,
    },
    {
      name: 'End Date',
      selector: (row) => row.end_date ?? '-',
      sortable: true,
    },
    {
      name: 'Actions',
      cell: (row) => (
        <div style={{ display: 'flex', gap: 6, whiteSpace: 'nowrap' }}>
          <button style={styles.button} onClick={() => handleViewDetails(row)}>
            View
          </button>
          <button style={styles.button} onClick={() => handleEditTrip(row)}>
            Edit
          </button>
          <button
            style={{ ...styles.button, ...styles.dangerButton }}
            onClick={() => handleDeleteTrip(row.id)}
          >
            Delete
          </button>
        </div>
      ),
      ignoreRowClick: true,
      allowOverflow: true,
      button: true,
      width: '220px',
    },
  ];

  return (
    <DataTable
      columns={columns}
      data={trips}
      noDataComponent='No trips yet. Add your first trip!'
      pagination
      highlightOnHover
      dense
      responsive
      style={{ background: '#fff', borderRadius: 8, boxShadow: '0 1px 4px #0001' }}
    />
  );
}

export default TripTable;
