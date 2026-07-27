import { useEffect, useCallback, useRef } from 'react';
import * as websocketService from '../services/websocket';

/**
 * Hook for WebSocket connection management
 * Currently prepared for future use - API polling is primary method
 */
export const useWebSocket = (url, onData) => {
  const unsubscribeRef = useRef(null);

  const connect = useCallback(async () => {
    if (!url) {
      console.warn('WebSocket URL not provided');
      return;
    }

    try {
      await websocketService.connect(url);

      // Subscribe to data updates
      unsubscribeRef.current = websocketService.subscribe('data', (data) => {
        if (onData) {
          onData(data);
        }
      });
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
    }
  }, [url, onData]);

  const disconnect = useCallback(() => {
    if (unsubscribeRef.current) {
      unsubscribeRef.current();
    }
    websocketService.disconnect();
  }, []);

  const send = useCallback((message) => {
    return websocketService.send(message);
  }, []);

  const isConnected = useCallback(() => {
    return websocketService.isConnected();
  }, []);

  useEffect(() => {
    // Only attempt connection if URL is provided
    if (url) {
      connect();
    }

    return () => {
      disconnect();
    };
  }, [url, connect, disconnect]);

  return {
    isConnected,
    send,
    disconnect,
  };
};

export default useWebSocket;
