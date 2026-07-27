import { STATE_COLORS, NODE_STATES, HAZARD_THRESHOLDS } from './constants';

/**
 * Determine node state based on hazard score
 */
export const getNodeStateFromHazard = (hazardScore) => {
  if (hazardScore <= HAZARD_THRESHOLDS.SAFE_MAX) return NODE_STATES.SAFE;
  if (hazardScore <= HAZARD_THRESHOLDS.DANGER_MAX) return NODE_STATES.DANGER;
  return NODE_STATES.CRITICAL;
};

/**
 * Get color for a given state
 */
export const getStateColor = (state) => {
  return STATE_COLORS[state] || STATE_COLORS.UNKNOWN;
};

/**
 * Format temperature value
 */
export const formatTemperature = (temp) => {
  if (temp === null || temp === undefined) return '--';
  return `${Math.round(temp)}°C`;
};

/**
 * Format smoke percentage
 */
export const formatSmoke = (smoke) => {
  if (smoke === null || smoke === undefined) return '--';
  return `${Math.round(smoke)}%`;
};

/**
 * Format occupancy count
 */
export const formatOccupancy = (occupancy) => {
  if (occupancy === null || occupancy === undefined) return '--';
  return `${Math.round(occupancy)}`;
};

/**
 * Format hazard score with one decimal
 */
export const formatHazardScore = (score) => {
  if (score === null || score === undefined) return '--';
  return Math.round(score * 10) / 10;
};

/**
 * Determine if node is dangerous
 */
export const isDangerous = (state) => {
  return state === NODE_STATES.DANGER || state === NODE_STATES.CRITICAL;
};

/**
 * Determine if node is critical
 */
export const isCritical = (state) => {
  return state === NODE_STATES.CRITICAL;
};

/**
 * Calculate risk level percentage for visualization
 */
export const getRiskPercentage = (hazardScore) => {
  if (hazardScore <= HAZARD_THRESHOLDS.SAFE_MAX) return 0;
  if (hazardScore >= 100) return 100;
  return Math.round((hazardScore / 100) * 100);
};

/**
 * Format time elapsed
 */
export const formatTimeElapsed = (seconds) => {
  if (seconds < 60) return `${Math.round(seconds)}s`;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.round(seconds % 60);
  return `${minutes}m ${remainingSeconds}s`;
};

/**
 * Get LED status color
 */
export const getLEDColor = (ledState) => {
  if (!ledState) return '#9ca3af';
  const stateColors = {
    OFF: '#9ca3af',
    GREEN: '#10b981',
    AMBER: '#f59e0b',
    RED_PULSE: '#dc2626',
    RED_BLINK: '#dc2626',
  };
  return stateColors[ledState] || '#9ca3af';
};

/**
 * Check if LED is active
 */
export const isLEDActive = (ledState) => {
  return ledState && ledState !== 'OFF';
};

/**
 * Check if LED is pulsing/blinking
 */
export const isLEDAnimating = (ledState) => {
  return ledState === 'RED_PULSE' || ledState === 'RED_BLINK';
};

/**
 * Build route display string
 */
export const formatRoute = (routePath) => {
  if (!routePath || !Array.isArray(routePath)) return '--';
  return routePath.join(' → ');
};

/**
 * Get evacuation status color
 */
export const getEvacuationStatusColor = (required) => {
  return required ? '#dc2626' : '#10b981';
};

/**
 * Get system status badge
 */
export const getSystemStatus = (state) => {
  if (!state) return { label: 'Unknown', color: '#9ca3af' };
  
  const hasEvacuation = state.evacuation?.decision?.evacuation_required;
  const hasCritical = Object.values(state.nodes || {}).some(
    (node) => node.state === NODE_STATES.CRITICAL
  );

  if (hasCritical) {
    return { label: 'CRITICAL', color: '#dc2626' };
  }
  if (hasEvacuation) {
    return { label: 'WARNING', color: '#f59e0b' };
  }
  return { label: 'SAFE', color: '#10b981' };
};

/**
 * Clamp value between min and max
 */
export const clamp = (value, min, max) => {
  return Math.min(Math.max(value, min), max);
};

/**
 * Debounce function
 */
export const debounce = (func, wait) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

/**
 * Throttle function
 */
export const throttle = (func, limit) => {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
};
