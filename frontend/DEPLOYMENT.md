# Deployment Guide - Fire Command Center

## Production Build & Deployment

---

## 📦 Building for Production

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Optimize Production Build

```bash
npm run build
```

This creates an optimized `dist/` folder ready for deployment.

### Step 3: Verify Build

```bash
npm run preview
```

Opens a local preview of the production build at http://localhost:4173

---

## 🚀 Deployment Options

### Option 1: Static Hosting (Recommended for Hackathon)

#### Vercel (Free, 0-click deployment)
```bash
npm i -g vercel
vercel
```

#### Netlify (Free, 0-click deployment)
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```

#### GitHub Pages
```bash
# Add to package.json:
"homepage": "https://yourusername.github.io/fire-command-center"

npm run build
npm i -g gh-pages
gh-pages -d dist
```

### Option 2: Traditional Server Hosting

#### Using Node.js (Simple HTTP Server)
```bash
npm install -g serve
serve -s dist -l 5173
```

#### Using Python
```bash
# Python 3
python -m http.server 8080 --directory dist

# Python 2
python -m SimpleHTTPServer 8080
```

#### Using nginx
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/fire-command-center/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Option 3: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build and run:
```bash
docker build -t fire-command-center .
docker run -p 80:80 fire-command-center
```

---

## 🔧 Configuration for Production

### Environment Variables

Create `.env.production`:

```
# Backend API (update to your production server)
VITE_APP_API_URL=https://your-backend-domain.com

# Optional WebSocket (for future use)
VITE_APP_WS_URL=wss://your-backend-domain.com/ws

# Feature flags
VITE_APP_ENABLE_WEBSOCKET=false
VITE_APP_POLL_INTERVAL=1000
```

### Backend URL Configuration

For hackathon on same machine:
```javascript
export const API_BASE_URL = 'http://localhost:8000';
```

For remote/cloud deployment:
```javascript
export const API_BASE_URL = 'https://api.your-domain.com';
```

### CORS Configuration (Backend)

Ensure your backend allows CORS:

```python
# FastAPI example
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔐 Security Checklist

- [ ] Remove console.log statements in production
- [ ] Enable HTTPS (use SSL certificate)
- [ ] Configure CORS properly (don't use "*" in production)
- [ ] Add authentication if needed
- [ ] Rate limit API endpoints
- [ ] Use environment variables for sensitive data
- [ ] Enable security headers:
  ```
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  X-XSS-Protection: 1; mode=block
  ```

---

## 📊 Performance Optimization

The build is already optimized with:

- ✅ Code minification
- ✅ Tree shaking (unused code removal)
- ✅ CSS minification
- ✅ Asset compression
- ✅ Chunk splitting (react vendor separated)
- ✅ Source maps disabled for production

### Additional Optimizations

1. **CDN Caching**
   - Cache static assets for 1 year
   - Cache index.html for 1 hour

2. **Gzip Compression**
   - Enable on server
   - Reduces bundle by ~60%

3. **Image Optimization**
   - Currently using SVG (already optimized)
   - No large assets in this build

### Bundle Size

Estimated sizes:
- React + DOM: ~40KB
- CSS: ~30KB
- App code: ~50KB
- **Total: ~120KB gzipped**

---

## 🚦 Deployment Checklist

### Pre-Deployment
- [ ] All tests pass (see TESTING.md)
- [ ] No console errors
- [ ] Backend running and accessible
- [ ] Environment variables configured
- [ ] CORS enabled on backend
- [ ] SSL certificate installed (if using HTTPS)

### During Deployment
- [ ] Run `npm run build` successfully
- [ ] Verify `dist/` folder created
- [ ] Test production build locally
- [ ] Upload to hosting service
- [ ] Configure domain/DNS
- [ ] Test frontend on production URL
- [ ] Verify backend connectivity

### Post-Deployment
- [ ] Test all dashboard features
- [ ] Test data loading
- [ ] Test simulations
- [ ] Monitor error logs
- [ ] Monitor performance
- [ ] Verify mobile responsiveness

---

## 📱 Mobile Deployment

For tablets/phones at hackathon:

### Responsive Design
- ✅ Already responsive (grid adjusts)
- ✅ Touch-friendly buttons
- ✅ Scales from 320px to 4K

### Testing
```bash
# Open DevTools (F12)
# Device toolbar icon (Ctrl+Shift+M)
# Test with:
# - iPhone 12 (390x844)
# - iPad (768x1024)
# - Tablet (1024x768)
```

---

## 🔄 Continuous Deployment

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: 18
      
      - name: Install and Build
        run: |
          npm install
          npm run build
      
      - name: Deploy
        run: |
          # Your deployment command here
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## 🔍 Monitoring & Debugging

### Production Issues

1. **Check Browser Console**
   - F12 → Console tab
   - Look for red errors
   - Check API calls in Network tab

2. **Check Backend Logs**
   ```bash
   # If using Python backend
   tail -f backend.log
   ```

3. **Monitor Performance**
   - Use browser DevTools → Lighthouse
   - Check response times
   - Monitor CPU/memory usage

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| 404 errors | Wrong API URL | Update API_BASE_URL |
| CORS errors | Backend CORS disabled | Enable CORS in backend |
| Data not loading | Backend down | Check backend health |
| Slow performance | Network latency | Check WebSocket, increase poll interval |

---

## 📈 Scaling Considerations

For large deployments:

1. **Load Balancing**
   - Use multiple backend instances
   - Use nginx/HAProxy for load balancing

2. **Caching**
   - Cache dashboard state on server
   - Reduce database queries

3. **WebSocket**
   - Implement for lower latency
   - Use message queues for scalability

4. **Database**
   - Add indexing for quick lookups
   - Archive historical data

---

## 🎉 Go-Live Checklist

Before hackathon presentation:

- [ ] Frontend deployed and accessible
- [ ] Backend configured and running
- [ ] API endpoints verified working
- [ ] Dashboard displays correctly
- [ ] All simulations functional
- [ ] Mobile responsiveness tested
- [ ] Performance acceptable (< 2s load)
- [ ] Error handling working
- [ ] Backup backend instance available
- [ ] Demo script ready

---

## 📞 Deployment Support

### Quick Troubleshooting

**Frontend won't load:**
1. Check browser console (F12 → Console)
2. Verify API_BASE_URL in constants.js
3. Check backend is running
4. Try clearing browser cache

**API calls failing:**
1. Check backend URL is correct
2. Verify backend CORS settings
3. Confirm backend is running
4. Check network tab for error responses

**Performance issues:**
1. Check network latency
2. Verify backend response times
3. Monitor browser memory usage
4. Consider WebSocket implementation

---

## 🚀 Deployment Commands Summary

```bash
# Development
npm run dev              # Start dev server

# Production
npm run build           # Create optimized build
npm run preview         # Test production build

# Deployment
vercel                  # Deploy to Vercel
netlify deploy --prod   # Deploy to Netlify

# Local serving
serve -s dist -l 5173   # Serve with Node
python -m http.server   # Serve with Python
```

---

**Your Fire Command Center is ready for production! 🎉**

For any issues during deployment, refer to the main README.md or TESTING.md files.
