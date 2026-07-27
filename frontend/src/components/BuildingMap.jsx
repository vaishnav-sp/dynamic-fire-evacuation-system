import React, { useState } from 'react';
import {
  getStateColor,
  isCritical,
} from '../utils/helpers';
import styles from './BuildingMap.module.css';

/**
 * Building Map Component
 * SVG-based interactive floor map with nodes and evacuation routes
 */
const BuildingMap = ({ nodes, evacuationRoute, onNodeClick, selectedNode }) => {
  const [hoveredNode, setHoveredNode] = useState(null);

  if (!nodes) {
    return (
      <div className={styles.container}>
        <div className={styles.noData}>No building data</div>
      </div>
    );
  }

  // SVG coordinate mapping for nodes
  const nodePositions = {
    R1: { x: 50, y: 50, width: 140, height: 110 },
    R2: { x: 220, y: 50, width: 140, height: 110 },
    R3: { x: 390, y: 50, width: 140, height: 110 },
    C1: { x: 50, y: 180, width: 140, height: 80 },
    C2: { x: 220, y: 180, width: 140, height: 80 },
    R4: { x: 390, y: 180, width: 140, height: 110 },
    R5: { x: 220, y: 320, width: 140, height: 110 },
    E1: { x: 50, y: 450, width: 140, height: 60 },
    E2: { x: 390, y: 450, width: 140, height: 60 },
  };

  const isNodeOnRoute = (nodeId) => {
    return evacuationRoute && evacuationRoute.includes(nodeId);
  };

  const getNodeColor = (nodeId) => {
    const node = nodes[nodeId];
    if (!node) return '#e5e7eb';
    return getStateColor(node.state);
  };

  const getNodeLabel = (nodeId) => {
    const node = nodes[nodeId];
    if (!node) return nodeId;
    return `${nodeId}\n${node.state}`;
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Digital Twin Floor Map</h3>
      <div className={styles.mapWrapper}>
        <svg
          viewBox="0 0 600 550"
          className={styles.map}
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Background */}
          <rect width="600" height="550" fill="#fafbfc" stroke="#e5e7eb" strokeWidth="2" />

          {/* Grid background */}
          <defs>
            <pattern
              id="grid"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="#f0f1f5"
                strokeWidth="0.5"
              />
            </pattern>

            {/* Glow filter for critical nodes */}
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>

            {/* Pulse animation */}
            <style>{`
              @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
              }
              .node-pulse {
                animation: pulse 2s ease-in-out infinite;
              }
            `}</style>
          </defs>

          <rect width="600" height="550" fill="url(#grid)" />

          {/* Draw nodes */}
          {Object.entries(nodePositions).map(([nodeId, pos]) => {
            const color = getNodeColor(nodeId);
            const critical = isCritical(nodes[nodeId]?.state);
            const onRoute = isNodeOnRoute(nodeId);
            const selected = selectedNode === nodeId;
            const hovered = hoveredNode === nodeId;

            return (
              <g
                key={nodeId}
                onClick={() => onNodeClick?.(nodeId)}
                className={styles.nodeGroup}
                style={{ cursor: 'pointer' }}
              >
                {/* Route highlight background */}
                {onRoute && (
                  <rect
                    x={pos.x - 5}
                    y={pos.y - 5}
                    width={pos.width + 10}
                    height={pos.height + 10}
                    fill={color}
                    opacity="0.15"
                    rx="8"
                  />
                )}

                {/* Node rectangle */}
                <rect
                  x={pos.x}
                  y={pos.y}
                  width={pos.width}
                  height={pos.height}
                  fill={color}
                  stroke={selected ? '#1e3a8a' : '#9ca3af'}
                  strokeWidth={selected ? 3 : hovered ? 2 : 1.5}
                  rx="6"
                  opacity={onRoute ? 1 : 0.8}
                  className={critical ? 'node-pulse' : ''}
                  filter={critical ? 'url(#glow)' : 'none'}
                />

                {/* Node ID and status */}
                <text
                  x={pos.x + pos.width / 2}
                  y={pos.y + pos.height / 2 - 8}
                  textAnchor="middle"
                  fill="#ffffff"
                  fontSize="16"
                  fontWeight="bold"
                  pointerEvents="none"
                >
                  {nodeId}
                </text>

                <text
                  x={pos.x + pos.width / 2}
                  y={pos.y + pos.height / 2 + 15}
                  textAnchor="middle"
                  fill="#ffffff"
                  fontSize="11"
                  fontWeight="500"
                  pointerEvents="none"
                >
                  {nodes[nodeId]?.state || '---'}
                </text>

                {/* Hazard score indicator */}
                {nodes[nodeId] && (
                  <text
                    x={pos.x + pos.width / 2}
                    y={pos.y + pos.height - 5}
                    textAnchor="middle"
                    fill="#ffffff"
                    fontSize="10"
                    pointerEvents="none"
                  >
                    {Math.round(nodes[nodeId].hazard_score)}/100
                  </text>
                )}

                {/* Selection indicator */}
                {selected && (
                  <rect
                    x={pos.x - 3}
                    y={pos.y - 3}
                    width={pos.width + 6}
                    height={pos.height + 6}
                    fill="none"
                    stroke="#1e3a8a"
                    strokeWidth="3"
                    rx="8"
                    strokeDasharray="5,5"
                  />
                )}
              </g>
            );
          })}

          {/* Draw evacuation route path */}
          {evacuationRoute && evacuationRoute.length > 1 && (
            <g className={styles.routePath}>
              {evacuationRoute.map((nodeId, index) => {
                if (index >= evacuationRoute.length - 1) return null;

                const from = nodePositions[nodeId];
                const to = nodePositions[evacuationRoute[index + 1]];

                if (!from || !to) return null;

                const x1 = from.x + from.width / 2;
                const y1 = from.y + from.height / 2;
                const x2 = to.x + to.width / 2;
                const y2 = to.y + to.height / 2;

                return (
                  <g key={`route-${index}`}>
                    {/* Path line with glow */}
                    <line
                      x1={x1}
                      y1={y1}
                      x2={x2}
                      y2={y2}
                      stroke="#10b981"
                      strokeWidth="5"
                      opacity="0.3"
                      strokeLinecap="round"
                    />

                    {/* Main path line */}
                    <line
                      x1={x1}
                      y1={y1}
                      x2={x2}
                      y2={y2}
                      stroke="#10b981"
                      strokeWidth="2.5"
                      strokeDasharray="5,5"
                      strokeLinecap="round"
                      className={styles.animatedPath}
                    />

                    {/* Arrow indicator */}
                    <circle
                      cx={(x1 + x2) / 2}
                      cy={(y1 + y2) / 2}
                      r="4"
                      fill="#10b981"
                    />
                  </g>
                );
              })}
            </g>
          )}

          {/* Building labels */}
          <text
            x="300"
            y="25"
            textAnchor="middle"
            fill="#1f2937"
            fontSize="14"
            fontWeight="bold"
          >
            FLOOR PLAN
          </text>
        </svg>
      </div>

      {/* Legend */}
      <div className={styles.legend}>
        <div className={styles.legendItem}>
          <div className={styles.legendIcon}>→</div>
          <span>Evacuation Route</span>
        </div>
        <div className={styles.legendItem}>
          <div className={styles.legendIcon}>○</div>
          <span>Click node for details</span>
        </div>
      </div>
    </div>
  );
};

export default BuildingMap;
