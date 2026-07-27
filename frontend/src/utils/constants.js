// API Configuration
// Using Vite environment variables (import.meta.env.VITE_*)
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const API_BASE_URL = apiUrl;
export const API_POLL_INTERVAL = 1000; // 1 second polling fallback

// Backend Endpoints
export const ENDPOINTS = {
  DASHBOARD_STATE: '/dashboard/state',
  SIMULATION_FLASHOVER: '/simulation/flashover',
  SIMULATION_SMOLDERING: '/simulation/smoldering',
  SIMULATION_RESET: '/simulation/reset',
  HEALTH: '/health',
};

// Node States & Colors
export const NODE_STATES = {
  SAFE: 'SAFE',
  DANGER: 'DANGER',
  CRITICAL: 'CRITICAL',
  UNKNOWN: 'UNKNOWN',
};

export const STATE_COLORS = {
  SAFE: '#10b981',
  DANGER: '#ea580c',
  CRITICAL: '#dc2626',
  WARNING: '#f59e0b',
  UNKNOWN: '#9ca3af',
};

export const STATE_LABELS = {
  SAFE: 'Safe',
  DANGER: 'Danger',
  CRITICAL: 'Critical',
  WARNING: 'Warning',
  UNKNOWN: 'Unknown',
};

// Node Types
export const NODE_TYPES = {
  REAL: 'REAL',
  VIRTUAL: 'VIRTUAL',
};

// Building Layout
export const BUILDING_NODES = {
  rooms: ['R1', 'R2', 'R3', 'R4', 'R5'],
  corridors: ['C1', 'C2'],
  exits: ['E1', 'E2'],
};

// LED States
export const LED_STATES = {
  OFF: 'OFF',
  GREEN: 'GREEN',
  AMBER: 'AMBER',
  RED_PULSE: 'RED_PULSE',
  RED_BLINK: 'RED_BLINK',
};

// Evacuation Decision Reasons
export const EVACUATION_REASONS = {
  NO_EVACUATION: 'No evacuation required',
  LOW_HAZARD: 'Low hazard detected',
  MEDIUM_HAZARD: 'Medium hazard detected',
  HIGH_HAZARD: 'High hazard detected',
  CRITICAL_FIRE: 'Critical fire hazard detected',
  FIRE_SPREADING: 'Fire spreading detected',
};

// Hazard Score Thresholds
export const HAZARD_THRESHOLDS = {
  SAFE_MAX: 25,
  DANGER_MIN: 26,
  DANGER_MAX: 65,
  CRITICAL_MIN: 66,
};

// Prediction Timeline
export const PREDICTION_INTERVALS = [
  { label: 'NOW', seconds: 0 },
  { label: '30s', seconds: 30 },
  { label: '60s', seconds: 60 },
  { label: '90s', seconds: 90 },
];

// UI Constants
export const ANIMATIONS = {
  PULSE: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  BLINK: 'blink 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  SLIDE_IN: 'slideIn 0.3s ease-out',
};
