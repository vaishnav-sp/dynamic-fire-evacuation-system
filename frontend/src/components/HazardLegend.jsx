import React from 'react';
import { STATE_COLORS, STATE_LABELS, NODE_STATES } from '../utils/constants';
import styles from './HazardLegend.module.css';

/**
 * Hazard Legend Component
 * Displays color-coded risk levels
 */
const HazardLegend = ({ compact = false }) => {
  const states = [NODE_STATES.SAFE, NODE_STATES.DANGER, NODE_STATES.CRITICAL];

  return (
    <div className={`${styles.legend} ${compact ? styles.compact : ''}`}>
      <h3 className={styles.title}>Risk Levels</h3>
      <div className={styles.items}>
        {states.map((state) => (
          <div key={state} className={styles.item}>
            <div
              className={styles.indicator}
              style={{ backgroundColor: STATE_COLORS[state] }}
            />
            <span className={styles.label}>{STATE_LABELS[state]}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HazardLegend;
