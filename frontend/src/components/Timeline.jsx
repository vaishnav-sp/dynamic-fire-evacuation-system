import React from 'react';
import { PREDICTION_INTERVALS } from '../utils/constants';
import { getStateColor } from '../utils/helpers';
import styles from './Timeline.module.css';

/**
 * Timeline Component
 * Displays prediction timeline and hazard progression
 */
const Timeline = ({ nodes, events = [] }) => {
  if (!nodes || Object.keys(nodes).length === 0) {
    return (
      <div className={styles.container}>
        <h3>Prediction Timeline</h3>
        <div className={styles.noData}>No data available</div>
      </div>
    );
  }

  // Get the node with highest current hazard for main timeline display
  const maxNode = Object.entries(nodes).reduce((max, [id, node]) => {
    return (node.hazard_score || 0) > (max.hazard || 0)
      ? { id, hazard: node.hazard_score, predicted: node.predicted_hazard }
      : max;
  }, {});

  // Simulate prediction progression (in real app, this would come from backend)
  const getProgressionValue = (baseHazard, predictedHazard, index) => {
    const trend = (predictedHazard - baseHazard) / 3;
    return Math.max(
      0,
      Math.min(100, baseHazard + trend * (index + 1))
    );
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Hazard Progression</h3>

      {maxNode.id && (
        <div className={styles.timelineSection}>
          <div className={styles.timelineNode}>
            <div className={styles.nodeLabel}>{maxNode.id}</div>
            <div className={styles.timelineGraph}>
              {PREDICTION_INTERVALS.map((interval, index) => {
                const value = getProgressionValue(
                  maxNode.hazard,
                  maxNode.predicted,
                  index
                );
                const state =
                  value <= 25 ? 'SAFE' : value <= 65 ? 'DANGER' : 'CRITICAL';
                const color = getStateColor(state);

                return (
                  <div key={interval.label} className={styles.timePoint}>
                    <div className={styles.timeLabel}>{interval.label}</div>
                    <div className={styles.timeBar}>
                      <div
                        className={styles.timeBarFill}
                        style={{
                          height: `${value}%`,
                          backgroundColor: color,
                        }}
                      />
                    </div>
                    <div className={styles.timeValue}>{Math.round(value)}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {events.length > 0 && (
        <div className={styles.eventsSection}>
          <h4 className={styles.eventsTitle}>Recent Events</h4>
          <div className={styles.eventsList}>
            {events.slice(-5).map((event, index) => (
              <div key={index} className={styles.eventItem}>
                <div className={styles.eventTime}>{event.time}</div>
                <div className={styles.eventDescription}>{event.description}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Timeline;
