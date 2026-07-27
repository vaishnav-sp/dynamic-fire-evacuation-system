# Fire Command Center Frontend

A production-grade emergency response dashboard built with React for the Dynamic Fire Evacuation Router system.

## Features

✓ Real-time hazard visualization with interactive floor map
✓ Dynamic evacuation route calculation and display
✓ Live sensor data dashboard
✓ Predictive hazard timeline
✓ Simulation controls for testing
✓ Professional light-theme BMS-style UI
✓ Responsive design
✓ Real-time API polling with WebSocket support ready

## Project Structure

```
src/
├── components/          # React components
│   ├── BuildingMap.jsx         # SVG interactive floor map
│   ├── HazardLegend.jsx        # Risk level legend
│   ├── HeatMap.jsx             # Hazard intensity visualization
│   ├── NodeStatus.jsx          # Detailed node information
│   ├── RoomCard.jsx            # Node status cards
│   ├── RoutePanel.jsx          # Evacuation route control
│   ├── SensorPanel.jsx         # Live sensor readings
│   └── Timeline.jsx            # Prediction timeline
├── hooks/              # Custom React hooks
│   ├── useBuilding.js          # Building state management
│   └── useWebSocket.js         # WebSocket connection
├── pages/              # Page components
│   └── Dashboard.jsx           # Main dashboard layout
├── services/           # API & data services
│   ├── api.js                  # Backend API calls
│   └── websocket.js            # WebSocket handler
├── utils/              # Utilities and helpers
│   ├── constants.js            # System constants
│   └── helpers.js              # Helper functions
├── App.jsx             # Root component
├── main.jsx            # Entry point
└── index.css           # Global styles
```

## Setup

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Configuration

Set the backend API URL via environment variables:

```bash
# .env or terminal
VITE_APP_API_URL=http://localhost:8000
```

Or modify `src/utils/constants.js`:
```javascript
export const API_BASE_URL = 'http://localhost:8000';
```

## Development

Start the development server:

```bash
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## Production Build

```bash
npm run build
```

Output files will be in the `dist/` directory.

## Architecture

### Data Flow

1. **useBuilding Hook**: Polls `/dashboard/state` endpoint every second
2. **API Service**: Handles HTTP requests with error handling
3. **Components**: Display data and respond to user interactions
4. **WebSocket Service**: Prepared for real-time updates (optional)

### Key Technologies

- **React 18**: UI framework with hooks
- **CSS Modules**: Component-scoped styling
- **SVG**: Interactive floor map visualization
- **Fetch API**: HTTP client for backend communication

## API Integration

The dashboard expects the backend to expose:

### GET `/dashboard/state`

Returns the current building state:

```json
{
  "nodes": {
    "R1": {
      "node_type": "REAL|VIRTUAL",
      "temperature": 25,
      "smoke": 0,
      "flame": false,
      "occupancy": 0,
      "hazard_score": 6.25,
      "predicted_hazard": 6.25,
      "state": "SAFE|DANGER|CRITICAL"
    }
  },
  "evacuation": {
    "decision": {
      "evacuation_required": true,
      "reason": "Critical fire hazard detected"
    },
    "route": {
      "type": "SAFEST",
      "path": ["C2", "R5", "E2"],
      "cost": 14.63
    },
    "actuator_commands": {
      "R2": {
        "led": "RED_PULSE"
      }
    }
  }
}
```

### POST `/simulation/flashover/{node_id}`
Trigger flashover simulation at a node

### POST `/simulation/smoldering/{node_id}`
Trigger smoldering simulation at a node

### POST `/simulation/reset`
Reset simulation to initial state

## Styling

The dashboard uses a professional light theme with:

- **Color Palette**:
  - Safe: Green (#10b981)
  - Warning: Amber (#f59e0b)
  - Danger: Orange (#ea580c)
  - Critical: Red (#dc2626)
  - Primary: Navy Blue (#1e3a8a)

- **Design System**:
  - Rounded corners (6px-12px)
  - Soft shadows
  - Clear typography hierarchy
  - Smooth transitions (150ms-350ms)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- Real-time polling with 1-second interval
- Efficient component updates with React hooks
- Memoized callbacks to prevent unnecessary re-renders
- SVG optimization for floor map

## Future Enhancements

- WebSocket integration for lower latency
- Historical data charts
- Advanced filtering and search
- Mobile-responsive optimization
- Dark mode support
- Data export functionality
- User authentication
- Event logging and audit trails

## Troubleshooting

### Dashboard shows "Connection Error"

1. Verify backend is running on the correct port
2. Check CORS settings in backend
3. Inspect browser console for API errors
4. Ensure API_BASE_URL is correctly configured

### Nodes not showing updated data

1. Confirm backend is sending valid state JSON
2. Check browser network tab for API responses
3. Verify hazard_score and predicted_hazard values are numbers

### Map visualization issues

1. Clear browser cache
2. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
3. Check SVG rendering in browser DevTools

## License

See LICENSE file in project root.

## Support

For issues or questions, refer to the main project documentation.
