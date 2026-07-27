import React from 'react';
import {
  formatTemperature,
  formatSmoke,
  formatHazardScore,
  getStateColor,
  isCritical,
} from '../utils/helpers';
import { NODE_TYPES } from '../utils/constants';
import styles from './RoomCard.module.css';

/**
 * Room Card Component
 * Displays a room/node card with key information
 */
const RoomCard = ({ node, nodeId, onClick, selected = false, onSimulate }) => {
  if (!node) {
    return (
      <div className={`${styles.card} ${styles.empty}`} onClick={onClick}>
        <div className={styles.noData}>--</div>
      </div>
    );
  }

  const color = getStateColor(node.state);
  const critical = isCritical(node.state);
  const isReal = node.node_type === NODE_TYPES.REAL;

  return (
    <div
      className={`${styles.card} ${critical ? styles.critical : ''} ${
        selected ? styles.selected : ''
      }`}
      onClick={onClick}
      style={{ borderColor: color }}
    >
      <div className={styles.header}>
        <h3 className={styles.id}>{nodeId}</h3>
        <span className={styles.type}>{isReal ? '🟢' : '🔵'}</span>
      </div>

      <div className={styles.state} style={{ color }}>
        {node.state}
      </div>

      <div className={styles.content}>
        <div className={styles.sensor}>
          <span className={styles.label}>Temp:</span>
          <span className={styles.value}>{formatTemperature(node.temperature)}</span>
        </div>
        <div className={styles.sensor}>
          <span className={styles.label}>Smoke:</span>
          <span className={styles.value}>{formatSmoke(node.smoke)}</span>
        </div>
        <div className={styles.sensor}>
          <span className={styles.label}>Hazard:</span>
          <span className={styles.value} style={{ color }}>
            {formatHazardScore(node.hazard_score)}
          </span>
        </div>
      </div>

      {selected && onSimulate && (
        <div className={styles.simulationButtons}>
          <button
            className={styles.simButton}
            onClick={(e) => {
              e.stopPropagation();
              onSimulate('flashover');
            }}
          >
            Flashover
          </button>
          <button
            className={styles.simButton}
            onClick={(e) => {
              e.stopPropagation();
              onSimulate('smoldering');
            }}
          >
            Smoldering
          </button>
        </div>
      )}
    </div>
  );
};

export default RoomCard;
