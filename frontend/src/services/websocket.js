/**
 * WebSocket Service for real-time data updates
 * Currently prepared for future use - API polling is primary method
 */

let websocket = null;
let listeners = {};

/**
 * Subscribe to a WebSocket event
 */
export const subscribe = (event, callback) => {
  if (!listeners[event]) {
    listeners[event] = [];
  }
  listeners[event].push(callback);

  // Return unsubscribe function
  return () => {
    listeners[event] = listeners[event].filter((cb) => cb !== callback);
  };
};

/**
 * Publish event to listeners
 */
const publish = (event, data) => {
  if (listeners[event]) {
    listeners[event].forEach((callback) => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error in listener for ${event}:`, error);
      }
    });
  }
};

/**
 * Connect to WebSocket
 */
export const connect = (url) => {
  return new Promise((resolve, reject) => {
    try {
      websocket = new WebSocket(url);

      websocket.onopen = () => {
        console.log('WebSocket connected');
        publish('connected', true);
        resolve(websocket);
      };

      websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          publish('data', data);
          publish(data.type, data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        publish('error', error);
        reject(error);
      };

      websocket.onclose = () => {
        console.log('WebSocket disconnected');
        publish('connected', false);
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
      reject(error);
    }
  });
};

/**
 * Disconnect from WebSocket
 */
export const disconnect = () => {
  if (websocket) {
    websocket.close();
    websocket = null;
  }
};

/**
 * Send message through WebSocket
 */
export const send = (message) => {
  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify(message));
    return true;
  }
  console.warn('WebSocket is not open');
  return false;
};

/**
 * Check if connected
 */
export const isConnected = () => {
  return websocket && websocket.readyState === WebSocket.OPEN;
};

/**
 * Get WebSocket ready state
 */
export const getReadyState = () => {
  return websocket?.readyState ?? WebSocket.CLOSED;
};

export default {
  connect,
  disconnect,
  send,
  subscribe,
  isConnected,
  getReadyState,
};
