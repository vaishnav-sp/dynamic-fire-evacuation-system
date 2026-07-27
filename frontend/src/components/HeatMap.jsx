import React from 'react';
import { getStateColor } from '../utils/helpers';
import styles from './HeatMap.module.css';

/**
 * Heat Map Component
 * Visualizes hazard intensity across the building
 */
const HeatMap = ({ nodes }) => {
  if (!nodes || Object.keys(nodes).length === 0) {
    return (
      <div className={styles.container}>
        <h3>Hazard Heat Map</h3>
        <div className={styles.noData}>No data available</div>
      </div>
    );
  }

  // Get sorted nodes by hazard score
  const sortedNodes = Object.entries(nodes)
    .map(([id, node]) => ({
      id,
      hazard: node.hazard_score || 0,
      state: node.state,
      predicted: node.predicted_hazard || 0,
    }))
    .sort((a, b) => b.hazard - a.hazard);

  const maxHazard = Math.max(...sortedNodes.map((n) => n.hazard), 100);

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Hazard Heat Map</h3>
      <div className={styles.heatmapChart}>
        {sortedNodes.map((node) => {
          const intensity = (node.hazard / maxHazard) * 100;
          const color = getStateColor(node.state);

          return (
            <div key={node.id} className={styles.bar}>
              <div className={styles.barLabel}>{node.id}</div>
              <div className={styles.barContainer}>
                <div
                  className={styles.barFill}
                  style={{
                    width: `${intensity}%`,
                    backgroundColor: color,
                    boxShadow: `0 0 10px ${color}40`,
                  }}
                >
                  <span className={styles.barValue}>{Math.round(node.hazard)}</span>
                </div>
              </div>
              <div className={styles.predicted}>
                <small>Pred: {Math.round(node.predicted)}</small>
              </div>
            </div>
          );
        })}
      </div>

      <div className={styles.legend}>
        <div className={styles.legendItem}>
          <span className={styles.legendLabel}>Hazard Score: 0-100</span>
        </div>
      </div>
    </div>
  );
};

export default HeatMap;
