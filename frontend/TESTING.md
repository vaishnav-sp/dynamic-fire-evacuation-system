# Fire Command Center - Testing Checklist

## Pre-Deployment Verification

Use this checklist to ensure the dashboard works correctly with your backend before the hackathon demo.

---

## 🔧 Setup Verification

- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Frontend dependencies installed (`npm install` completed)
- [ ] Backend running on http://localhost:8000
- [ ] Backend API accessible (`curl http://localhost:8000/health`)
- [ ] Frontend dev server running (`npm run dev`)
- [ ] Dashboard accessible at http://localhost:5173

---

## 📡 Backend Integration

### API Endpoint Testing

- [ ] `/dashboard/state` returns valid JSON
  - Check response has `nodes` object
  - Check response has `evacuation` object
  - Check each node has: temperature, smoke, flame, occupancy, hazard_score, predicted_hazard, state

- [ ] `/health` endpoint returns 200 status
- [ ] `/simulation/flashover/{node_id}` accepts POST requests
- [ ] `/simulation/smoldering/{node_id}` accepts POST requests
- [ ] `/simulation/reset` accepts POST requests

**Verification Command:**
```bash
# Check dashboard state
curl http://localhost:8000/dashboard/state | jq .

# Check health
curl http://localhost:8000/health
```

---

## 🖥️ Dashboard Display

### Header Rendering
- [ ] Title "FIRE COMMAND CENTER" visible
- [ ] Subtitle "AI Powered Dynamic Evacuation Intelligence System" visible
- [ ] Status badge shows current system state
- [ ] Connection status shows "Connected" (green dot)
- [ ] Timestamp shows current time and updates every second

### Building Map
- [ ] SVG renders without errors
- [ ] 5 rooms visible (R1, R2, R3, R4, R5)
- [ ] 2 corridors visible (C1, C2)
- [ ] 2 exits visible (E1, E2)
- [ ] All nodes have state labels (SAFE, DANGER, CRITICAL)
- [ ] Nodes are color-coded correctly:
  - [ ] Safe nodes are green
  - [ ] Danger nodes are orange
  - [ ] Critical nodes are red and pulsing
- [ ] Hazard scores displayed inside each node

### Layout
- [ ] Three-column layout renders correctly
- [ ] Left column: Building map + legend
- [ ] Center column: Details + visualization
- [ ] Right column: Controls + status
- [ ] All sections scrollable
- [ ] No overlapping content

### Overview Stats (when no node selected)
- [ ] Total nodes count correct
- [ ] Critical count accurate
- [ ] Evacuation status shows YES or NO

---

## 🎯 Interactive Features

### Node Selection
- [ ] Click on node R1 → highlights with blue border
- [ ] Node details panel appears in center
- [ ] Shows temperature, smoke, flame, occupancy
- [ ] Shows hazard scores
- [ ] Click same node again → deselects (blue border removed)

### Hazard Visualization
- [ ] Heat map displays all nodes
- [ ] Bars show correct proportional hazard levels
- [ ] Colors match node states
- [ ] Predicted values shown

### Prediction Timeline
- [ ] Timeline graph shows 4 time points (NOW, 30s, 60s, 90s)
- [ ] Bars show progression of hazard
- [ ] Colors transition from green to red based on values

### Route Display
- [ ] Evacuation route shows in format: "N1 → N2 → N3"
- [ ] Green dashed line drawn on map between route nodes
- [ ] Route updates when simulating events

---

## 🎮 Simulation Controls

### Before Simulation
- [ ] Select a node (e.g., R2)
- [ ] Note current hazard scores
- [ ] Note current evacuation status

### Trigger Flashover
- [ ] Click "Flashover R2" button
- [ ] Route should recalculate
- [ ] R2 hazard score increases significantly
- [ ] R2 state changes to DANGER or CRITICAL
- [ ] Evacuation status updates if needed

### Trigger Smoldering
- [ ] Click "Smoldering R3" button
- [ ] R3 hazard increases gradually
- [ ] System responds appropriately

### Reset Simulation
- [ ] Click "Reset" button
- [ ] All nodes return to safe state
- [ ] Hazard scores reset to 0-25 range
- [ ] Evacuation status returns to NO
- [ ] Map colors return to green

---

## 📊 Data Verification

### Node Status Cards
- [ ] All node cards visible in bottom-right grid
- [ ] Each shows: Node ID, State, Temp, Smoke, Hazard
- [ ] Values match the main display data
- [ ] Clicking card selects node

### Sensor Panel (REAL nodes only)
- [ ] Expandable/collapsible
- [ ] Shows 4 sensors: Temperature, Smoke, Flame, Occupancy
- [ ] Values update every second
- [ ] LED status shows for REAL nodes

---

## 🔄 Real-time Updates

### Automatic Polling
- [ ] Data updates every ~1 second
- [ ] Timestamp in header increments
- [ ] No manual refresh needed
- [ ] Check network tab shows requests to `/dashboard/state`

### Connection Handling
- [ ] Stop backend temporarily
- [ ] Dashboard shows "Offline" status
- [ ] Connection badge turns red
- [ ] Error message appears
- [ ] Restart backend
- [ ] Dashboard reconnects automatically

---

## 🎨 Visual Quality

### Light Theme
- [ ] No dark backgrounds (light/white preferred)
- [ ] Professional color scheme
- [ ] Navy blue headers/primary elements
- [ ] Proper contrast for readability
- [ ] Icons/emojis render correctly

### Responsive Design
- [ ] All sections fit on 1920x1080 screen
- [ ] No content cut off or overflowing
- [ ] Resize window → layout adapts
- [ ] Works on 1280x720 screens (laptop)

### Animations
- [ ] Critical nodes pulse smoothly
- [ ] Route path animates
- [ ] Buttons have hover effects
- [ ] Transitions are smooth (not jumpy)

---

## ⚡ Performance

### Load Time
- [ ] Dashboard loads in < 3 seconds
- [ ] No console errors
- [ ] No console warnings
- [ ] Network tab shows < 500ms for API calls

### Updates
- [ ] No lag when clicking nodes
- [ ] Route updates instantly on simulation
- [ ] Smooth 60fps animations
- [ ] CPU usage < 20% idle

**Check with DevTools:**
1. Open DevTools (F12)
2. Performance tab → Record
3. Interact with dashboard
4. Check framerate (should be 60fps)

---

## 🔐 Data Integrity

### Number Validation
- [ ] Hazard scores: 0-100 range
- [ ] Temperature: positive numbers, reasonable range
- [ ] Smoke: 0-100 percentage
- [ ] Occupancy: non-negative integers

### State Validation
- [ ] Nodes only show: SAFE, DANGER, CRITICAL
- [ ] Evacuation decision: true or false
- [ ] Route costs: positive numbers
- [ ] Node types: REAL or VIRTUAL

---

## 🎤 Demo Readiness

### Presentation Flow
- [ ] Start with clean dashboard (no nodes selected)
- [ ] Explain real vs virtual nodes
- [ ] Show heat map visualization
- [ ] Demonstrate node selection
- [ ] Trigger flashover event
- [ ] Show route recalculation
- [ ] Trigger smoldering at different node
- [ ] Show prediction timeline
- [ ] Reset and return to safe state

### Demo Scripts

**Opening:**
"This is the Fire Command Center - an AI-powered emergency management system with real-time hazard mapping and dynamic evacuation routing."

**Features to Highlight:**
1. "See real-time sensor data from both physical ESP32 nodes (green) and virtual digital twin nodes (blue)"
2. "The system automatically calculates the safest evacuation route (shown in green)"
3. "When hazards change, routes recalculate in real-time - watch..." (trigger flashover)
4. "The prediction timeline shows projected hazard progression"
5. "The system integrates sensor fusion, fire propagation simulation, and explainable AI decisions"

---

## 🐛 Known Issues & Workarounds

### Issue: Connection Error
**Solution:**
- Ensure backend is running
- Check API_BASE_URL in constants.js
- Verify backend CORS settings

### Issue: Data not updating
**Solution:**
- Check browser console (F12)
- Check network tab for failed requests
- Restart both frontend and backend

### Issue: Map not rendering
**Solution:**
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Check SVG support in browser

### Issue: Simulation doesn't work
**Solution:**
- Select a node first (blue border should show)
- Check backend simulation endpoints exist
- Look for error in browser console

---

## ✅ Final Checklist

Before presenting:

- [ ] All tests above pass
- [ ] No console errors or warnings
- [ ] Backend and frontend both running
- [ ] Data loading from backend successfully
- [ ] Simulations trigger correctly
- [ ] Dashboard looks professional
- [ ] Dashboard responds smoothly
- [ ] All visualizations render correctly
- [ ] Demo script rehearsed
- [ ] Backup browser tab open (just in case)

---

## 📝 Judges' Impressions

Checklist for "wow" moments:

- [ ] Real-time data updates (show timestamp)
- [ ] Interactive map visualization (click nodes)
- [ ] Route recalculation (trigger event)
- [ ] Hazard prediction (show timeline)
- [ ] Professional UI (production quality)
- [ ] Seamless integration (real + virtual nodes)
- [ ] Simulation capabilities (test scenarios)
- [ ] Real hardware integration (mention ESP32)

---

**You're ready to showcase! 🚀**

Remember: The judges want to see how well the system handles emergency scenarios, how quickly it reacts, and how clearly it communicates critical information.
