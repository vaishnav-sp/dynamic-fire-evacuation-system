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

    // ---------- TOP ----------
    R1: { x: 40,  y: 40,  width: 90, height: 60 },
    R2: { x: 170, y: 40,  width: 90, height: 60 },
    R3: { x: 300, y: 40,  width: 90, height: 60 },
    R4: { x: 430, y: 40,  width: 90, height: 60 },

    // ---------- UPPER CORRIDORS ----------
    C1: { x: 40,  y: 140, width: 90, height: 45 },
    C2: { x: 235, y: 140, width: 90, height: 45 },
    C3: { x: 430, y: 140, width: 90, height: 45 },

    // ---------- LOBBY ----------
    L1: { x: 235, y: 210, width: 90, height: 45 },

    // ---------- MIDDLE ----------
    C4: { x: 80,  y: 280, width: 70, height: 40 },
    H1: { x: 235, y: 280, width: 90, height: 45 },
    C5: { x: 410, y: 280, width: 70, height: 40 },

    // ---------- LOWER ROOMS ----------
    R5: { x: 40,  y: 360, width: 90, height: 60 },
    R6: { x: 170, y: 360, width: 90, height: 60 },
    R7: { x: 300, y: 360, width: 90, height: 60 },
    R8: { x: 430, y: 360, width: 90, height: 60 },

    // ---------- LOWER CORRIDORS ----------
    C6: { x: 105, y: 455, width: 90, height: 45 },
    C7: { x: 365, y: 455, width: 90, height: 45 },

    // ---------- LOWER LOBBY ----------
    L2: { x: 235, y: 525, width: 90, height: 45 },

    // ---------- EXITS ----------
    E1: { x: 235, y: 120, width: 90, height: 40 },
    E2: { x: 235, y: 610, width: 90, height: 40 },
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
          viewBox="0 0 1000 800"
          className={styles.map}
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Background */}
          <rect width="560" height="680" fill="#fafbfc" stroke="#e5e7eb" strokeWidth="2" />

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

          <rect width="560" height="680" fill="url(#grid)" />

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
                onClick={async () => {
                  onNodeClick?.(nodeId);

                  if (nodeId.startsWith("R")) {
                    await fetch(`http://localhost:8000/dashboard/start/${nodeId}`, {
                      method: "POST",
                    });

                    window.dispatchEvent(new Event("refresh-dashboard"));
                  }
                }}


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

                const startX = from.x + from.width / 2;
                const startY = from.y + from.height / 2;

                const endX = to.x + to.width / 2;
                const endY = to.y + to.height / 2;

                // L-shaped routing
                const midX = startX;
                const midY = endY;

                return (
                  <g key={index}>
                    {/* Glow */}
                    <polyline
                      points={`${startX},${startY} ${midX},${midY} ${endX},${endY}`}
                      fill="none"
                      stroke="#10b981"
                      strokeWidth="8"
                      opacity="0.25"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />

                    {/* Main route */}
                    <polyline
                      points={`${startX},${startY} ${midX},${midY} ${endX},${endY}`}
                      fill="none"
                      stroke="#10b981"
                      strokeWidth="4"
                      strokeDasharray="10 6"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className={styles.animatedPath}
                    />

                    {/* Direction marker */}
                    <circle
                      cx={midX}
                      cy={midY}
                      r="5"
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
