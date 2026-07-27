import React from 'react';
import {
  formatTemperature,
  formatSmoke,
  formatOccupancy,
  formatHazardScore,
  getStateColor,
  isCritical,
} from '../utils/helpers';
import { NODE_TYPES } from '../utils/constants';
import styles from './NodeStatus.module.css';

/**
 * Node Status Component
 * Displays detailed sensor readings for a specific node
 */
const NodeStatus = ({ node, nodeId }) => {
  if (!node) {
    return (
      <div className={styles.container}>
        <div className={styles.noData}>No data available</div>
      </div>
    );
  }

  const color = getStateColor(node.state);
  const isReal = node.node_type === NODE_TYPES.REAL;
  const critical = isCritical(node.state);

  return (
    <div className={`${styles.container} ${critical ? styles.critical : ''}`}>
      <div className={styles.header}>
        <h3 className={styles.nodeId}>{nodeId}</h3>
        <div className={styles.typeAndState}>
          <span className={styles.type}>{isReal ? '🟢 REAL' : '🔵 VIRTUAL'}</span>
          <span className={styles.state} style={{ color }}>
            {node.state}
          </span>
        </div>
      </div>

      <div className={styles.sensors}>
        <div className={styles.sensorRow}>
          <label>Temperature</label>
          <span className={styles.value}>{formatTemperature(node.temperature)}</span>
        </div>
        <div className={styles.sensorRow}>
          <label>Smoke</label>
          <span className={styles.value}>{formatSmoke(node.smoke)}</span>
        </div>
        <div className={styles.sensorRow}>
          <label>Flame</label>
          <span className={styles.value}>{node.flame ? '🔥 Detected' : '✓ No'}</span>
        </div>
        <div className={styles.sensorRow}>
          <label>Occupancy</label>
          <span className={styles.value}>{formatOccupancy(node.occupancy)}</span>
        </div>
      </div>

      <div className={styles.hazard}>
        <div className={styles.hazardRow}>
          <label>Current Hazard</label>
          <span className={styles.hazardValue} style={{ color }}>
            {formatHazardScore(node.hazard_score)}/100
          </span>
        </div>
        <div className={styles.hazardRow}>
          <label>Predicted Hazard</label>
          <span className={styles.hazardValue} style={{ color }}>
            {formatHazardScore(node.predicted_hazard)}/100
          </span>
        </div>
      </div>
    </div>
  );
};

export default NodeStatus;
