# Dynamic Fire Evacuation System
## System Architecture, API Documentation & Communication Protocol

---

# 1. System Architecture

## 1.1 Overview

The Dynamic Fire Evacuation System is a hybrid digital twin-based intelligent fire monitoring and evacuation platform that combines:

- Real-time sensor acquisition
- Virtual fire simulation
- Sensor fusion-based hazard estimation
- Predictive fire progression analysis
- Dynamic evacuation route generation
- Real-time visualization dashboard

The system follows a layered architecture where physical sensor nodes, simulation nodes, backend intelligence, and frontend visualization work together to create a real-time emergency response system.

---

# 1.2 High-Level Architecture

```
                 ┌─────────────────────┐
                 │     ESP32 Node      │
                 │ Temperature Sensor  │
                 │ Smoke Sensor        │
                 │ Flame Sensor        │
                 │ Occupancy Input     │
                 └──────────┬──────────┘
                            │
                            │ MQTT Communication
                            │
                            ▼

                 ┌─────────────────────┐
                 │    MQTT Broker      │
                 │  Message Transport  │
                 └──────────┬──────────┘
                            │

                            ▼

        ┌──────────────────────────────────┐
        │          Backend System          │
        │                                  │
        │  MQTT Subscriber                 │
        │        │                         │
        │        ▼                         │
        │  Sensor Data Processor           │
        │        │                         │
        │        ▼                         │
        │  Hazard Assessment Engine        │
        │        │                         │
        │        ▼                         │
        │  Fire Prediction Module          │
        │        │                         │
        │        ▼                         │
        │  Evacuation Route Optimizer      │
        │                                  │
        └──────────────┬───────────────────┘
                       │

                       ▼

        ┌──────────────────────────────────┐
        │        FastAPI Backend           │
        │                                  │
        │ REST APIs                        │
        │ Dashboard State                  │
        │ Simulation Control               │
        │ Route Information                │
        └──────────────┬───────────────────┘
                       │

                       ▼

        ┌──────────────────────────────────┐
        │       React Dashboard            │
        │                                  │
        │ Digital Twin Floor Map           │
        │ Hazard Visualization             │
        │ Evacuation Route Display         │
        │ Sensor Monitoring                │
        │ Fire Prediction Timeline         │
        └──────────────────────────────────┘
```

---

# 1.3 System Components

## 1.3.1 Sensor Layer

The sensor layer consists of ESP32-based monitoring nodes.

### Hardware Node Features

- Temperature monitoring
- Smoke detection
- Flame detection
- Occupancy estimation
- Wireless communication through MQTT


The collected information represents the physical state of a building zone.

Example sensor payload:

```json
{
 "node_id":"R2",
 "node_type":"ESP32",
 "temperature":34.2,
 "smoke":0,
 "flame":true,
 "occupancy":1
}
```

---

# 1.3.2 Digital Twin Layer

The digital twin represents the physical building digitally.

Each room/corridor is represented as a virtual node.

Each node maintains:

- Current hazard level
- Temperature
- Smoke concentration
- Flame status
- Occupancy
- Predicted future hazard


Example:

```json
{
 "node":"R4",
 "temperature":87.5,
 "smoke":48.8,
 "hazard_score":73.8,
 "state":"CRITICAL"
}
```

---

# 1.3.3 Hazard Intelligence Layer

The hazard engine combines multiple parameters to calculate fire risk.

Inputs:

- Temperature
- Smoke intensity
- Flame detection
- Occupancy


Output:

- Hazard score
- Fire severity state
- Future hazard prediction


Risk Classification:

| Hazard Score | State |
|-------------|-------|
| 0-25 | SAFE |
| 26-65 | DANGER |
| >65 | CRITICAL |

---

# 1.3.4 Prediction Module

The system predicts future fire conditions.

Prediction intervals:

- Current state
- 30 seconds
- 60 seconds
- 90 seconds


Example:

```json
{
 "prediction":
 {
    "30s":65,
    "60s":90,
    "90s":100
 }
}
```

This enables proactive evacuation instead of reaction-based evacuation.

---

# 1.3.5 Evacuation Routing Engine

The building is represented as a graph.

Each location becomes a graph node.

Edges represent possible movement paths.


The routing engine considers:

- Fire blocked areas
- Hazard severity
- Distance
- Safety score


The safest route is dynamically calculated.

Example:

```
START

C2

 |

R5

 |

E2

EXIT
```

---

# 1.3.6 Dashboard Layer

The React-based Fire Command Center provides:

## Features

- Interactive building floor map
- Real-time node status
- Hazard heat visualization
- Fire prediction timeline
- Evacuation route animation
- Simulation controls
- Sensor monitoring
- System status monitoring


---

# 2. API Documentation

Base URL:

```
http://localhost:8000
```

---

# 2.1 Health Check API

## GET /health

Checks backend availability.

### Request

```
GET /health
```

### Response

```json
{
 "status":"ONLINE",
 "service":"Dynamic Fire Evacuation System"
}
```

---

# 2.2 Root API

## GET /

Returns system information.

### Response

```json
{
 "system":"Dynamic Fire Evacuation System",
 "status":"running"
}
```

---

# 2.3 Dashboard State API

## GET /dashboard/state

Returns complete digital twin state.

### Response

```json
{
 "nodes":
 {
   "R2":
   {
    "temperature":84.8,
    "smoke":32,
    "flame":true,
    "hazard_score":65,
    "state":"CRITICAL"
   }
 },

 "evacuation":
 {
   "route":
   {
    "path":
    [
     "C2",
     "R5",
     "E2"
    ]
   }
 }
}
```

---

# 2.4 Simulation APIs

## Trigger Flashover

### POST

```
/simulation/flashover/{node_id}
```

Example:

```
POST /simulation/flashover/R2
```

Purpose:

Simulates a rapidly developing fire condition.


Response:

```json
{
 "scenario":"FLASHOVER",
 "node":"R2",
 "status":"APPLIED"
}
```

---

# Trigger Smoldering

### POST

```
/simulation/smoldering/{node_id}
```


Example:

```
POST /simulation/smoldering/R4
```


Response:

```json
{
 "scenario":"SMOLDERING",
 "node":"R4",
 "status":"APPLIED"
}
```

---

# Reset Simulation

### POST

```
/simulation/reset
```


Response:

```json
{
 "scenario":"RESET",
 "status":"APPLIED"
}
```

---

# 2.5 Route Comparison API

## GET /route/comparison

Returns safest and shortest evacuation information.


Response:

```json
{
 "status":"ACTIVE",

 "safest_route":
 {
   "path":
   [
    "C2",
    "R5",
    "E2"
   ],

   "risk":"LOW"
 }
}
```

---

# 3. Communication Protocol Documentation

---

# 3.1 Communication Overview

The system uses MQTT as the communication protocol between ESP32 sensor nodes and backend processing services.

Architecture:

```
ESP32
 |
 |
MQTT
 |
 |
Backend Subscriber
 |
 |
Hazard Engine
 |
 |
Dashboard
```

---

# 3.2 MQTT Communication

## Protocol

```
MQTT
```

## Broker

```
localhost:1883
```

---

# 3.3 Topic Structure

Sensor nodes publish data using:

```
fire/sensors/{node_id}
```


Example:

```
fire/sensors/R2
```

---

# 3.4 Sensor Message Format

ESP32 publishes JSON messages.


Example:

```json
{
 "node_id":"R2",
 "node_type":"ESP32",
 "temperature":34.2,
 "smoke":0,
 "flame":true,
 "occupancy":1
}
```


---

# 3.5 Backend Processing Flow


1. ESP32 collects sensor information.

2. Data is published through MQTT.

3. Backend MQTT subscriber receives message.

4. Sensor data is normalized.

5. Hazard score is calculated.

6. Digital twin state is updated.

7. Evacuation route is recalculated.

8. Dashboard receives updated information.


---

# 3.6 Hardware Communication

## ESP32 Node

Responsibilities:

- Sensor acquisition
- Data formatting
- MQTT publishing
- Local LED indication


## Backend

Responsibilities:

- Data processing
- Fire intelligence
- Routing decisions
- Dashboard synchronization


---

# 3.7 Real and Virtual Node Communication

The system supports hybrid deployment:

## Real Nodes

Physical ESP32 sensor nodes.

Example:

```
R1
```

## Virtual Nodes

Simulation-based nodes used for:

- Digital twin testing
- Fire spread simulation
- Scenario demonstration


Example:

```
R2,R3,R4,R5,C2
```


This hybrid approach allows testing large buildings with limited hardware.

---

# 4. System Innovation Summary

The proposed system introduces:

## Hybrid Digital Twin

Combines real sensor data with simulated building zones.

## Predictive Fire Intelligence

Predicts future fire conditions before complete hazard development.

## Dynamic Risk-Aware Routing

Routes are continuously updated based on changing fire conditions.

## Sensor Fusion

Multiple parameters are combined to estimate accurate hazard levels.

## Command Center Visualization

Provides emergency operators with complete building awareness.

---

# 5. Future Enhancements

Possible improvements:

- Multiple ESP32 deployment
- AI-based fire progression prediction
- Computer vision based occupancy detection
- Cloud deployment
- Mobile emergency responder application
- Integration with building management systems


---

# End of Documentation