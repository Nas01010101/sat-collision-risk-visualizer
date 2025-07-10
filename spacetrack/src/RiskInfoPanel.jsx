import React from 'react';

export default function RiskInfoPanel({ info, onClose }) {
  if (!info) return null;
  return (
    <div className="absolute top-4 right-4 bg-white p-4 rounded-lg shadow-lg z-10">
      <button className="float-right" onClick={onClose}>✕</button>
      <h2 className="text-xl font-bold">Object {info.id}</h2>
      <p>Risk score: {(info.risk*100).toFixed(1)}%</p>
      <p>Time to collision: {info.timeToCollision ?? 'N/A'}</p>
    </div>
  );
}
