# Quick Start Guide - Fire Command Center Dashboard

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Configure Backend URL

Edit `src/utils/constants.js` or create `.env.local`:

```javascript
// src/utils/constants.js
export const API_BASE_URL = 'http://localhost:8000';
```

Or create `.env.local`:
```
VITE_APP_API_URL=http://localhost:8000
```

### Step 3: Start Development Server

```bash
npm run dev
```

The dashboard will be available at: `http://localhost:5173`

### Step 4: Verify Backend Connection

Check the header status:
- Connection badge should show "Connected" (green)
- Last update timestamp should refresh every second

---

## 📊 Dashboard Tour

### Left Column: Building Overview
- **Digital Twin Map**: Interactive SVG showing 9 nodes
- **Risk Legend**: Color coding for hazard levels

### Center Column: Analysis & Details
- **Building Overview**: Quick stats (total nodes, critical count, evacuation status)
- **Node Details**: Click a node on the map to see detailed sensor readings
- **Hazard Heat Map**: Visual intensity comparison across building
- **Prediction Timeline**: Projected hazard progression (NOW, 30s, 60s, 90s)

### Right Column: Control & Monitoring
- **Evacuation Control**: Decision status, route info, simulation buttons
- **Sensor Status**: Live readings from REAL nodes
- **Node Status Grid**: Quick view of all nodes

---

## 🎮 Interactive Features

### Click on Map Nodes
- Displays detailed information in center column
- Shows sensor readings and hazard scores
- Enables simulation controls (when selected)

### Simulation Controls
- **Flashover R2**: Triggers emergency fire event
- **Smoldering R3**: Triggers slow fire progression
- **Reset**: Returns to initial state
- Watch route recalculate automatically

### Monitoring Indicators
- **Status Badge**: SAFE / WARNING / CRITICAL
- **Connection Status**: Shows backend connectivity
- **Timestamp**: Last data update time
- **Node Colors**: 
  - Green = Safe
  - Orange = Danger
  - Red = Critical (pulsing)

---

## 📱 Data Structure

The dashboard automatically fetches and displays:

```javascript
{
  nodes: {
    R1, R2, R3, R4, R5,     // Rooms
    C1, C2,                 // Corridors
    E1, E2                  // Exits
  },
  evacuation: {
    decision: { evacuation_required, reason },
    route: { type, path, cost },
    actuator_commands: { led_states }
  }
}
```

Each node shows:
- Temperature (°C)
- Smoke (%)
- Flame detection
- Occupancy count
- Current hazard score (0-100)
- Predicted hazard score

---

## 🔧 Configuration Options

### API Settings
```javascript
// src/utils/constants.js
export const API_BASE_URL = 'http://localhost:8000';
export const API_POLL_INTERVAL = 1000; // milliseconds
```

### Color Customization
```javascript
// src/utils/constants.js
export const STATE_COLORS = {
  SAFE: '#10b981',
  DANGER: '#ea580c',
  CRITICAL: '#dc2626',
  // ...
};
```

### Hazard Thresholds
```javascript
export const HAZARD_THRESHOLDS = {
  SAFE_MAX: 25,
  DANGER_MIN: 26,
  DANGER_MAX: 65,
  CRITICAL_MIN: 66,
};
```

---

## 🐛 Troubleshooting

### Dashboard shows "Connection Error"
1. Verify backend is running: `python run_backend.py`
2. Check backend port in constants.js (default: 8000)
3. Check CORS is enabled in backend
4. Open browser console (F12) for error details

### Data not updating
1. Check network tab (F12 → Network)
2. Should see requests to `/dashboard/state` every 1 second
3. Verify response status is 200
4. Check backend is returning valid JSON

### Map nodes not clickable
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Verify SVG is rendering (check page source)

### Simulation buttons don't work
1. Confirm node selection (should show blue border on map)
2. Check console for error messages
3. Verify backend routes exist: `/simulation/flashover/{id}`, etc.

---

## 🚢 Production Build

Create optimized production bundle:

```bash
npm run build
```

Output in `dist/` directory. Deploy the entire `dist` folder.

For serving:
```bash
npm run preview  # Preview production build locally
```

---

## 📚 File Structure Quick Reference

```
frontend/
├── src/
│   ├── components/      # 8 React components
│   ├── hooks/           # useBuilding, useWebSocket
│   ├── pages/           # Dashboard main layout
│   ├── services/        # API, WebSocket clients
│   ├── utils/           # Constants, helpers
│   ├── App.jsx          # Root component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Build config
└── README.md            # Full documentation
```

---

## 🎯 What to Look For in the Demo

1. **Real-time Data**: Header updates every second
2. **Interactive Map**: Click nodes to see details
3. **Route Animation**: Green dashed line shows evacuation path
4. **Hazard Colors**: Nodes change color based on risk
5. **Simulation**: Click "Flashover R2" to see route recalculate
6. **Professional UI**: Clean, enterprise-style BMS interface

---

## 💡 Pro Tips

- **Full Screen**: Press F11 for presentation mode
- **Refresh Data**: Automatic every 1 second
- **Monitor Performance**: Open DevTools → Performance tab
- **Test Mobile**: DevTools → Device Emulation
- **Debug API**: DevTools → Network tab shows all requests

---

## 🤝 Integration Points

The dashboard integrates with backend via:

1. **Polling** (Primary): Every 1 second
   - GET `/dashboard/state`
   - GET `/health`

2. **Simulation Commands**:
   - POST `/simulation/flashover/{node_id}`
   - POST `/simulation/smoldering/{node_id}`
   - POST `/simulation/reset`

3. **WebSocket** (Optional, for future):
   - Configured but not yet active
   - See `src/services/websocket.js`

---

## 📞 Support Resources

- Check `README.md` for detailed documentation
- See `src/components/` for component implementations
- Review `src/utils/constants.js` for all configuration options
- Check `src/services/api.js` for backend integration

---

**Ready to showcase your system! 🎉**

The dashboard now presents your fire evacuation system as a professional, production-grade emergency management tool.
