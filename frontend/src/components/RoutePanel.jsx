import React, { useState } from 'react';
import {
  formatRoute,
  getEvacuationStatusColor,
} from '../utils/helpers';
import {
  triggerFlashover,
  triggerSmoldering,
  resetSimulation,
} from '../services/api';
import styles from './RoutePanel.module.css';

/**
 * Route Panel Component
 * Displays evacuation route information and simulation controls
 */
const RoutePanel = ({ evacuation, onRefresh }) => {
  const [loading, setLoading] = useState(false);
  const [lastAction, setLastAction] = useState(null);

  if (!evacuation) {
    return (
      <div className={styles.container}>
        <div className={styles.noData}>No evacuation data</div>
      </div>
    );
  }

  const decision = evacuation.decision || {};
  const route = evacuation.route || {};
  const statusColor = getEvacuationStatusColor(decision.evacuation_required);

  const handleSimulation = async (action, nodeId = null) => {
    setLoading(true);
    try {
      if (action === 'reset') {
        await resetSimulation();
      } else if (nodeId) {
        if (action === 'flashover') {
          await triggerFlashover(nodeId);
        } else if (action === 'smoldering') {
          await triggerSmoldering(nodeId);
        }
      }
      setLastAction(`${action} triggered`);
      setTimeout(() => onRefresh?.(), 500);
    } catch (error) {
      console.error('Simulation error:', error);
      setLastAction(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Evacuation Control</h3>

      {/* Decision Status */}
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Decision Status</div>
        <div
          className={styles.statusCard}
          style={{ borderLeftColor: statusColor }}
        >
          <div className={styles.statusLabel}>Evacuation Required:</div>
          <div className={styles.statusValue} style={{ color: statusColor }}>
            {decision.evacuation_required ? '⚠️ YES' : '✓ NO'}
          </div>
          {decision.reason && (
            <div className={styles.reason}>{decision.reason}</div>
          )}
        </div>
      </div>

      {/* Route Information */}
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Current Route</div>
        <div className={styles.routeCard}>
          <div className={styles.routeRow}>
            <span className={styles.label}>Route Type:</span>
            <span className={styles.value}>{route.type || '--'}</span>
          </div>
          <div className={styles.routeRow}>
            <span className={styles.label}>Path:</span>
            <span className={styles.value}>{formatRoute(route.path)}</span>
          </div>
          <div className={styles.routeRow}>
            <span className={styles.label}>Cost:</span>
            <span className={styles.value}>{route.cost?.toFixed(2) || '--'}</span>
          </div>
        </div>
      </div>

      {/* Simulation Controls */}
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Simulation Control</div>
        <div className={styles.controls}>
          <button
            className={styles.button}
            onClick={() => handleSimulation('flashover', 'R2')}
            disabled={loading}
            title="Trigger flashover in R2"
          >
            🔥 Flashover R2
          </button>
          <button
            className={styles.button}
            onClick={() => handleSimulation('smoldering', 'R3')}
            disabled={loading}
            title="Trigger smoldering in R3"
          >
            💨 Smoldering R3
          </button>
          <button
            className={`${styles.button} ${styles.danger}`}
            onClick={() => handleSimulation('reset')}
            disabled={loading}
            title="Reset simulation to initial state"
          >
            ↻ Reset
          </button>
        </div>
        {lastAction && (
          <div className={styles.lastAction}>{lastAction}</div>
        )}
      </div>
    </div>
  );
};

export default RoutePanel;
