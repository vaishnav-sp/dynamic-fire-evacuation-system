import React from 'react';
import styles from './SystemBanner.module.css';

/**
 * SystemBanner Component
 * Displays backend, MQTT, and ESP32 connection status
 */
const SystemBanner = ({ isConnected, lastUpdate, mqttConnected, esp32Online }) => {
  const backendConnected = Boolean(isConnected);
  const mqttOnline = Boolean(mqttConnected);
  const esp32Active = Boolean(esp32Online);

  return (
    <div className={`${styles.banner} ${isConnected ? styles.healthy : styles.unhealthy}`}>
      <div className={styles.statusItem}>
        <div className={styles.indicator} style={{ backgroundColor: backendConnected ? '#10b981' : '#dc2626' }} />
        <div className={styles.info}>
          <div className={styles.label}>Backend API</div>
          <div className={styles.status}>{backendConnected ? 'CONNECTED' : 'DISCONNECTED'}</div>
        </div>
      </div>

      <div className={styles.divider} />

      <div className={styles.statusItem}>
        <div className={styles.indicator} style={{ backgroundColor: mqttOnline ? '#10b981' : '#f59e0b' }} />
        <div className={styles.info}>
          <div className={styles.label}>MQTT Broker</div>
          <div className={styles.status}>{mqttOnline ? 'ACTIVE' : 'OFFLINE'}</div>
        </div>
      </div>

      <div className={styles.divider} />

      <div className={styles.statusItem}>
        <div className={styles.indicator} style={{ backgroundColor: esp32Active ? '#10b981' : '#f59e0b' }} />
        <div className={styles.info}>
          <div className={styles.label}>ESP32 Sensor Node</div>
          <div className={styles.status}>{esp32Active ? 'ONLINE' : 'OFFLINE'}</div>
        </div>
      </div>

      {lastUpdate && (
        <>
          <div className={styles.divider} />
          <div className={styles.lastUpdate}>
            Last sync: {lastUpdate?.toLocaleTimeString?.() || 'n/a'}
          </div>
        </>
      )}
    </div>
  );
};

export default SystemBanner;
