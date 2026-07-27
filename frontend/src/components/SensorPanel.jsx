import React, { useState } from 'react';
import {
  formatTemperature,
  formatSmoke,
  formatOccupancy,
  getLEDColor,
  isLEDAnimating,
} from '../utils/helpers';
import { NODE_TYPES } from '../utils/constants';
import styles from './SensorPanel.module.css';

/**
 * Sensor Panel Component
 * Displays live sensor readings from a node
 */
const SensorPanel = ({ node, nodeId, ledState }) => {
  const [expanded, setExpanded] = useState(false);

  if (!node) {
    return <div className={styles.container}>No sensor data</div>;
  }

  const isReal = node.node_type === NODE_TYPES.REAL;
  const ledColor = getLEDColor(ledState);
  const isAnimating = isLEDAnimating(ledState);

  return (
    <div className={`${styles.container}`}>
      <button
        className={styles.header}
        onClick={() => setExpanded(!expanded)}
        aria-expanded={expanded}
      >
        <div className={styles.nodeInfo}>
          <span className={styles.nodeId}>{nodeId}</span>
          <span className={styles.type}>{isReal ? 'REAL' : 'VIRTUAL'}</span>
        </div>
        <span className={styles.toggle}>{expanded ? '−' : '+'}</span>
      </button>

      {expanded && (
        <div className={styles.content}>
          <div className={styles.sensorGrid}>
            <div className={styles.sensorItem}>
              <span className={styles.icon}>🌡️</span>
              <div className={styles.sensorInfo}>
                <div className={styles.label}>Temperature</div>
                <div className={styles.value}>{formatTemperature(node.temperature)}</div>
              </div>
            </div>

            <div className={styles.sensorItem}>
              <span className={styles.icon}>💨</span>
              <div className={styles.sensorInfo}>
                <div className={styles.label}>Smoke</div>
                <div className={styles.value}>{formatSmoke(node.smoke)}</div>
              </div>
            </div>

            <div className={styles.sensorItem}>
              <span className={styles.icon}>🔥</span>
              <div className={styles.sensorInfo}>
                <div className={styles.label}>Flame</div>
                <div className={styles.value}>{node.flame ? 'Detected' : 'No'}</div>
              </div>
            </div>

            <div className={styles.sensorItem}>
              <span className={styles.icon}>👥</span>
              <div className={styles.sensorInfo}>
                <div className={styles.label}>Occupancy</div>
                <div className={styles.value}>{formatOccupancy(node.occupancy)}</div>
              </div>
            </div>
          </div>

          {isReal && ledState && (
            <div className={styles.ledSection}>
              <div className={styles.ledLabel}>LED Status</div>
              <div className={styles.ledDisplay}>
                <div
                  className={`${styles.ledIndicator} ${isAnimating ? styles.pulse : ''}`}
                  style={{ backgroundColor: ledColor }}
                />
                <span className={styles.ledState}>{ledState}</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SensorPanel;
