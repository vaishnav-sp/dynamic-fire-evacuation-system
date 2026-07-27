import React, { useState, useEffect } from 'react';
import styles from './EventLog.module.css';

/**
 * EventLog Component
 * Displays time-stamped events like smoke detection, route changes, etc.
 */
const EventLog = ({ nodes, evacuation }) => {
  const [events, setEvents] = useState([]);
  const [expandedEvent, setExpandedEvent] = useState(null);

  useEffect(() => {
    const now = new Date();
    const newEvents = [];

    // Check for critical nodes
    Object.entries(nodes || {}).forEach(([nodeId, node]) => {
      if (node.state === 'CRITICAL') {
        newEvents.push({
          id: `critical-${nodeId}`,
          timestamp: now,
          type: 'CRITICAL_ALERT',
          title: '🔥 Critical Hazard Detected',
          description: `Node ${nodeId} reached critical hazard level (${node.hazard_score?.toFixed(0)}/100)`,
          severity: 'critical',
        });
      }
    });

    // Check for evacuation decision
    if (evacuation?.decision?.evacuation_required) {
      newEvents.push({
        id: 'evac-decision',
        timestamp: new Date(now.getTime() - 2000),
        type: 'EVACUATION_DECISION',
        title: '⚠️ Evacuation Decision Made',
        description: evacuation.decision.reason || 'High hazard level detected',
        severity: 'warning',
      });
    }

    // Check for route optimization
    if (evacuation?.route?.path) {
      newEvents.push({
        id: 'route-optimized',
        timestamp: new Date(now.getTime() - 5000),
        type: 'ROUTE_OPTIMIZED',
        title: '📍 Route Optimized',
        description: `Evacuation path set to: ${evacuation.route.path.join(' → ')}`,
        severity: 'info',
      });
    }

    // Smoke detection
    const smokyNodes = Object.entries(nodes || {})
      .filter(([, node]) => (node.smoke || 0) > 30)
      .slice(0, 2);

    smokyNodes.forEach(([nodeId, node], idx) => {
      newEvents.push({
        id: `smoke-${nodeId}`,
        timestamp: new Date(now.getTime() - 10000 - idx * 2000),
        type: 'SMOKE_DETECTED',
        title: '💨 Smoke Detected',
        description: `Smoke level at ${nodeId}: ${node.smoke?.toFixed(0)}%`,
        severity: 'warning',
      });
    });

    // Temperature spike
    const hotNodes = Object.entries(nodes || {})
      .filter(([, node]) => (node.temperature || 0) > 50)
      .slice(0, 1);

    hotNodes.forEach(([nodeId, node]) => {
      newEvents.push({
        id: `temp-${nodeId}`,
        timestamp: new Date(now.getTime() - 15000),
        type: 'TEMPERATURE_SPIKE',
        title: '🌡️ Temperature Spike',
        description: `Temperature at ${nodeId}: ${node.temperature?.toFixed(0)}°C`,
        severity: 'warning',
      });
    });

    // System online
    newEvents.push({
      id: 'system-online',
      timestamp: new Date(now.getTime() - 60000),
      type: 'SYSTEM_ONLINE',
      title: '✓ System Online',
      description: 'Fire Command Center initialized',
      severity: 'info',
    });

    // Sort by timestamp (newest first)
    newEvents.sort((a, b) => b.timestamp - a.timestamp);
    setEvents(newEvents.slice(0, 8)); // Keep last 8 events
  }, [nodes, evacuation]);

  const getSeverityColor = (severity) => {
    const colors = {
      critical: '#dc2626',
      warning: '#f59e0b',
      info: '#3b82f6',
    };
    return colors[severity] || '#6b7280';
  };

  const formatTime = (timestamp) => {
    const diff = new Date() - timestamp;
    if (diff < 60000) return 'just now';
    if (diff < 3600000) {
      const mins = Math.floor(diff / 60000);
      return `${mins}m ago`;
    }
    return timestamp.toLocaleTimeString();
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>📋 Event Log</h3>
      {events.length === 0 ? (
        <div className={styles.noEvents}>No events recorded</div>
      ) : (
        <div className={styles.eventsList}>
          {events.map((event) => (
            <div
              key={event.id}
              className={styles.eventItem}
              style={{ borderLeftColor: getSeverityColor(event.severity) }}
              onClick={() => setExpandedEvent(expandedEvent === event.id ? null : event.id)}
            >
              <div className={styles.eventHeader}>
                <div className={styles.eventTitleRow}>
                  <span className={styles.eventTitle}>{event.title}</span>
                  <span className={styles.eventTime}>{formatTime(event.timestamp)}</span>
                </div>
                <div className={styles.eventDescription}>{event.description}</div>
              </div>

              {expandedEvent === event.id && (
                <div className={styles.eventDetails}>
                  <div className={styles.detailRow}>
                    <span className={styles.label}>Type:</span>
                    <span className={styles.value}>{event.type}</span>
                  </div>
                  <div className={styles.detailRow}>
                    <span className={styles.label}>Time:</span>
                    <span className={styles.value}>{event.timestamp.toLocaleTimeString()}</span>
                  </div>
                  <div className={styles.detailRow}>
                    <span className={styles.label}>Severity:</span>
                    <span className={styles.value}>{event.severity.toUpperCase()}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EventLog;
