import { API_BASE_URL, ENDPOINTS } from '../utils/constants';

/**
 * Fetch dashboard state from backend
 * Retries once on network failure
 */
export const fetchDashboardState = async (retry = true) => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
    
    const response = await fetch(`${API_BASE_URL}${ENDPOINTS.DASHBOARD_STATE}`, {
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching dashboard state:', error);
    
    // Retry once on network errors
    if (retry && (error.name === 'AbortError' || error instanceof TypeError)) {
      console.warn('Network error, retrying once...');
      try {
        return await fetchDashboardState(false);
      } catch (retryError) {
        console.error('Retry failed:', retryError);
        throw new Error('Backend unavailable - check if server is running on ' + API_BASE_URL);
      }
    }
    
    throw error;
  }
};

/**
 * Check backend health
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}${ENDPOINTS.HEALTH}`);
    return response.ok;
  } catch (error) {
    console.error('Error checking backend health:', error);
    return false;
  }
};

/**
 * Trigger flashover simulation at a node
 */
export const triggerFlashover = async (nodeId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}${ENDPOINTS.SIMULATION_FLASHOVER}/${nodeId}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error triggering flashover:', error);
    throw error;
  }
};

/**
 * Trigger smoldering simulation at a node
 */
export const triggerSmoldering = async (nodeId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}${ENDPOINTS.SIMULATION_SMOLDERING}/${nodeId}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error triggering smoldering:', error);
    throw error;
  }
};

/**
 * Reset simulation
 */
export const resetSimulation = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}${ENDPOINTS.SIMULATION_RESET}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error resetting simulation:', error);
    throw error;
  }
};

export default {
  fetchDashboardState,
  checkHealth,
  triggerFlashover,
  triggerSmoldering,
  resetSimulation,
};
