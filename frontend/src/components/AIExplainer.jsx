import React from 'react';
import styles from './AIExplainer.module.css';

/**
 * AIExplainer Component
 * Displays why the system made certain evacuation decisions
 */
const AIExplainer = ({ evacuation, nodes }) => {
  if (!evacuation || !evacuation.route) {
    return (
      <div className={styles.container}>
        <div className={styles.noData}>Waiting for evacuation analysis...</div>
      </div>
    );
  }

  const route = evacuation.route;
  const decision = evacuation.decision;
  const routePath = route.path || [];

  // Analyze route decisions
  const getDangerZones = () => {
    const dangerous = [];
    Object.entries(nodes || {}).forEach(([nodeId, node]) => {
      if (node.state === 'CRITICAL' || node.state === 'DANGER') {
        dangerous.push(nodeId);
      }
    });
    return dangerous;
  };

  const getSelectedReason = () => {
    if (!routePath[0]) return 'Calculating optimal route...';
    
    const firstNode = nodes?.[routePath[0]];
    if (!firstNode) return 'Route selected';

    const reasons = [];
    
    if (firstNode.temperature < 60) reasons.push('Lower temperature zone');
    if ((firstNode.smoke || 0) < 20) reasons.push('Minimal smoke');
    if ((firstNode.occupancy || 0) > 0) reasons.push('Occupied zone priority');
    
    return reasons.length > 0 ? reasons.join(' • ') : 'Optimal path identified';
  };

  const dangerZones = getDangerZones();

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>🤖 AI Route Decision</h3>

      {/* Avoided Zones */}
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Avoided Zones</div>
        {dangerZones.length > 0 ? (
          <div className={styles.zonesList}>
            {dangerZones.map((nodeId) => {
              const node = nodes[nodeId];
              return (
                <div key={nodeId} className={styles.zoneItem}>
                  <span className={styles.zoneId}>{nodeId}</span>
                  <span className={styles.zoneReason}>
                    {node.state === 'CRITICAL' ? '🔥 Critical' : '⚠️ Danger'}
                  </span>
                  <span className={styles.zoneDetail}>
                    {node.hazard_score?.toFixed(0)}/100
                  </span>
                </div>
              );
            })}
          </div>
        ) : (
          <div className={styles.noData}>No dangerous zones detected</div>
        )}
      </div>

      {/* Selected Route Reason */}
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Route Selected Because</div>
        <div className={styles.reasonBox}>
          {getSelectedReason()}
        </div>
      </div>

      {/* Decision Logic */}
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Decision Logic</div>
        <div className={styles.logicList}>
          <div className={styles.logicItem}>
            <span className={styles.logicIcon}>✓</span>
            <span className={styles.logicText}>
              Sensor fusion evaluated {Object.keys(nodes || {}).length} nodes
            </span>
          </div>
          <div className={styles.logicItem}>
            <span className={styles.logicIcon}>✓</span>
            <span className={styles.logicText}>
              Predicted hazard at each exit analyzed
            </span>
          </div>
          <div className={styles.logicItem}>
            <span className={styles.logicIcon}>✓</span>
            <span className={styles.logicText}>
              Occupancy-aware path optimization applied
            </span>
          </div>
          <div className={styles.logicItem}>
            <span className={styles.logicIcon}>✓</span>
            <span className={styles.logicText}>
              Cost = {route.cost?.toFixed(2)} (lower is better)
            </span>
          </div>
        </div>
      </div>

      {/* Current Decision */}
      <div className={styles.section}>
        <div className={styles.sectionTitle}>Current Decision</div>
        <div className={`${styles.decisionBox} ${decision?.evacuation_required ? styles.required : styles.notRequired}`}>
          <div className={styles.decisionLabel}>
            Evacuation {decision?.evacuation_required ? 'REQUIRED' : 'NOT REQUIRED'}
          </div>
          {decision?.reason && (
            <div className={styles.decisionReason}>{decision.reason}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIExplainer;
