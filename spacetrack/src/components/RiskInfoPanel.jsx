import React from 'react';

/**
 * A floating panel showing risk & time‐to‐collision for a selected object.
 * Props:
 *   info: { id: string, risk: number, timeToCollision?: number }
 *   onClose: () => void
 */
export default function RiskInfoPanel({ info, onClose }) {
  if (!info) return null;
  return (
    <div
      style={{
        position: 'absolute',
        top: '1rem',
        right: '1rem',
        background: 'white',
        padding: '1rem',
        borderRadius: '0.5rem',
        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
        zIndex: 1000,
      }}
    >
      <button
        onClick={onClose}
        style={{
          position: 'absolute',
          top: '0.5rem',
          right: '0.5rem',
          border: 'none',
          background: 'transparent',
          cursor: 'pointer',
          fontSize: '1rem',
        }}
      >
        ✕
      </button>
      <h2 style={{ margin: '0 0 0.5rem' }}>Object {info.id}</h2>
      <p style={{ margin: '0.25rem 0' }}>
        Risk score: {(info.risk * 100).toFixed(1)}%
      </p>
      {info.timeToCollision != null && (
        <p style={{ margin: '0.25rem 0' }}>
          Time to collision: {(info.timeToCollision / 60).toFixed(1)} min
        </p>
      )}
    </div>
  );
}
