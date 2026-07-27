import React, { useState, useCallback } from 'react';
import useBuilding from '../hooks/useBuilding';
import BuildingMap from '../components/BuildingMap';
import NodeStatus from '../components/NodeStatus';
import SensorPanel from '../components/SensorPanel';
import HazardLegend from '../components/HazardLegend';
import HeatMap from '../components/HeatMap';
import Timeline from '../components/Timeline';
import RoutePanel from '../components/RoutePanel';
import RoomCard from '../components/RoomCard';
import SystemBanner from '../components/SystemBanner';
import AIExplainer from '../components/AIExplainer';
import EventLog from '../components/EventLog';
import { getSystemStatus, formatRoute } from '../utils/helpers';
import { NODE_TYPES } from '../utils/constants';
import styles from './Dashboard.module.css';

/**
 * Main Dashboard Component
 * Orchestrates all dashboard sections and real-time data updates
 */
const Dashboard = () => {
  const { state, loading, error, isConnected, lastUpdate, refetch } = useBuilding();
  const [selectedNode, setSelectedNode] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showInsights, setShowInsights] = useState(false);

  const handleNodeClick = useCallback((nodeId) => {
    setSelectedNode(selectedNode === nodeId ? null : nodeId);
  }, [selectedNode]);

  const handleRefresh = useCallback(() => {
    refetch();
  }, [refetch]);

  const systemStatus = getSystemStatus(state);
  const nodes = state?.nodes || {};
  const backendConnected = Boolean(isConnected && state);
  const mqttConnected = Object.keys(nodes).length > 0;
  const esp32Online = Object.values(nodes).some((node) => node.node_type === NODE_TYPES.REAL);

  // Note: Dashboard always renders with default empty state
  // Connection status is shown in SystemBanner
  // Loading spinner shown only on initial load with no data
  // Retry happens automatically via useBuilding polling

  const evacuation = state?.evacuation || {};
  const evacuationRoute = evacuation.route?.path || [];
  const selectedNodeData = selectedNode ? nodes[selectedNode] : null;
  const actuatorCommands = evacuation.actuator_commands || {};

  return (
    <div className={styles.dashboard}>
      {/* HEADER */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.titleSection}>
            <h1 className={styles.mainTitle}>🚨 FIRE COMMAND CENTER</h1>
            <p className={styles.subtitle}>
              AI Powered Dynamic Evacuation Intelligence System
            </p>
          </div>

          <div className={styles.statusSection}>
            <div className={styles.statusBadge} style={{ color: systemStatus.color }}>
              {systemStatus.label}
            </div>

            <div className={`${styles.connectionStatus} ${isConnected ? styles.connected : styles.disconnected}`}>
              <span className={styles.dot} />
              {isConnected ? 'Connected' : 'Offline'}
            </div>

            <div className={styles.timestamp}>
              {lastUpdate ? `Updated: ${lastUpdate.toLocaleTimeString()}` : '...'}
            </div>
          </div>
        </div>
      </header>

      {/* SYSTEM BANNER */}
      <SystemBanner isConnected={backendConnected} lastUpdate={lastUpdate} mqttConnected={mqttConnected} esp32Online={esp32Online} />

      {/* MAIN CONTENT */}
      <main className={styles.main}>
        <div className={styles.grid}>
          {/* LEFT COLUMN: Building Map */}
          <section className={styles.leftColumn}>
            <div className={styles.section}>
              <BuildingMap
                nodes={nodes}
                evacuationRoute={evacuationRoute}
                onNodeClick={handleNodeClick}
                selectedNode={selectedNode}
              />
            </div>

            <div className={styles.section}>
              <HazardLegend />
            </div>
          </section>

          {/* CENTER COLUMN: Details & Controls */}
          <section className={styles.centerColumn}>
            {/* Node Details */}
            {selectedNode ? (
              <div className={styles.section}>
                <div className={styles.sectionHeader}>
                  <h3>Node Details: {selectedNode}</h3>
                  <button
                    className={styles.closeButton}
                    onClick={() => setSelectedNode(null)}
                  >
                    ×
                  </button>
                </div>
                <NodeStatus node={selectedNodeData} nodeId={selectedNode} />
              </div>
            ) : (
              <div className={styles.section}>
                <h3 className={styles.sectionTitle}>Building Overview</h3>
                <div className={styles.quickStats}>
                  <div className={styles.statCard}>
                    <div className={styles.statLabel}>Total Nodes</div>
                    <div className={styles.statValue}>{Object.keys(nodes).length}</div>
                  </div>
                  <div className={styles.statCard}>
                    <div className={styles.statLabel}>Critical</div>
                    <div className={styles.statValue} style={{ color: '#dc2626' }}>
                      {Object.values(nodes).filter((n) => n.state === 'CRITICAL').length}
                    </div>
                  </div>
                  <div className={styles.statCard}>
                    <div className={styles.statLabel}>Evacuation</div>
                    <div
                      className={styles.statValue}
                      style={{
                        color: evacuation.decision?.evacuation_required
                          ? '#dc2626'
                          : '#10b981',
                      }}
                    >
                      {evacuation.decision?.evacuation_required ? 'YES' : 'NO'}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Hazard Heat Map */}
            <div className={styles.section}>
              <HeatMap nodes={nodes} />
            </div>

            {/* Prediction Timeline */}
            <div className={styles.section}>
              <Timeline nodes={nodes} />
            </div>
          </section>

          {/* RIGHT COLUMN: Route Panel & Sensors */}
          <section className={styles.rightColumn}>
            {/* Evacuation Route */}
            <div className={styles.section}>
              <RoutePanel evacuation={evacuation} onRefresh={handleRefresh} />
            </div>

            {/* AI Insights Toggle */}
            <div className={styles.section}>
              <button
                className={`${styles.insightToggle} ${showInsights ? styles.active : ''}`}
                onClick={() => setShowInsights(!showInsights)}
              >
                {showInsights ? '✕ Hide AI Insights' : '→ Show AI Insights'}
              </button>
            </div>

            {/* AI Explainer & Event Log (collapsible) */}
            {showInsights && (
              <>
                <div className={styles.section}>
                  <AIExplainer evacuation={evacuation} nodes={nodes} />
                </div>
                <div className={styles.section}>
                  <EventLog nodes={nodes} evacuation={evacuation} />
                </div>
              </>
            )}

            {/* Active Sensors */}
            {!showInsights && (
              <>
                <div className={styles.section}>
                  <h3 className={styles.sectionTitle}>Sensor Status</h3>
                  <div className={styles.sensorsList}>
                    {Object.entries(nodes)
                      .filter(([, node]) => node.node_type === 'REAL')
                      .slice(0, 3)
                      .map(([nodeId, node]) => (
                        <SensorPanel
                          key={nodeId}
                          node={node}
                          nodeId={nodeId}
                          ledState={actuatorCommands[nodeId]?.led}
                        />
                      ))}
                  </div>
                </div>

                {/* Node Quick View */}
                <div className={styles.section}>
                  <h3 className={styles.sectionTitle}>Node Status</h3>
                  <div className={styles.roomGrid}>
                {Object.entries(nodes)
                  .slice(0, 6)
                  .map(([nodeId, node]) => (
                    <RoomCard
                      key={nodeId}
                      node={node}
                      nodeId={nodeId}
                      selected={selectedNode === nodeId}
                      onClick={() => handleNodeClick(nodeId)}
                    />
                  ))}
              </div>
                </div>
              </>
            )}
          </section>
        </div>
      </main>

      {/* FOOTER */}
      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <span>Dynamic Fire Evacuation Router • Real-time Hazard Mapping</span>
          <span>System Status: {isConnected ? '✓ Online' : '✗ Offline'}</span>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
