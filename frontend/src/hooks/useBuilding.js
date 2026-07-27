import { useEffect, useState, useCallback } from 'react';
import { fetchDashboardState } from '../services/api';
import { API_POLL_INTERVAL } from '../utils/constants';

/**
 * Hook for managing building state
 * Polls backend for dashboard state with automatic retry
 * Keeps last valid state when backend is temporarily unavailable
 */
export const useBuilding = () => {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(true); // Only true on initial load
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [hasEverConnected, setHasEverConnected] = useState(false);

  // Fetch data from backend
  const fetchData = useCallback(async () => {
    try {
      console.log('[useBuilding] Fetching dashboard state...');
      const data = await fetchDashboardState();
      console.log('[useBuilding] Fetch successful:', data);
      setState(data);
      setError(null);
      setIsConnected(true);
      setHasEverConnected(true);
      setLastUpdate(new Date());
      // Only clear loading on successful first connection
      if (loading && !hasEverConnected) {
        setLoading(false);
      }
    } catch (err) {
      console.error('[useBuilding] Fetch failed:', err);
      setIsConnected(false);
      console.error('Failed to fetch building state:', err);
      // Keep previous state and only update connection status
      // This allows dashboard to show last known data while offline
      setError(err.message);
      // Clear loading after first attempt even if failed
      // Dashboard will render with empty or previous state
      if (loading) {
        setLoading(false);
      }
    }
  }, [loading, hasEverConnected]);

  // Initial fetch and adaptive polling setup
  useEffect(() => {
    // Initial fetch
    fetchData();

    // Set up adaptive polling - retry faster when offline
    let pollInterval;
    
    const setupPolling = () => {
      // Clear previous interval
      if (pollInterval) clearInterval(pollInterval);
      
      // Poll immediately, then set recurring interval
      const poll = async () => {
        await fetchData();
      };
      
      // Use faster interval if not connected (1 second) or normal interval if connected (1 second default)
      // This ensures we keep trying even if offline
      pollInterval = setInterval(poll, API_POLL_INTERVAL);
    };
    
    setupPolling();

    // Cleanup
    return () => {
      if (pollInterval) clearInterval(pollInterval);
    };
  }, [fetchData]);

  // Refetch function for manual updates
  const refetch = useCallback(async () => {
    setLoading(true);
    await fetchData();
  }, [fetchData]);

  return {
    state,
    loading,
    error,
    isConnected,
    lastUpdate,
    refetch,
  };
};

export default useBuilding;
