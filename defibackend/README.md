# 🛡️ DeFi Attack Early Warning System - Backend

AI-powered early warning system for detecting anomalous DeFi transactions in real-time.

## 🏗️ Architecture

```
API → Inference → Risk Score → Threshold → Alert → DB → Blockchain
```

### Key Design Principles

✅ **Separation of Concerns**: Detection ≠ Decision  
✅ **Offline Training**: Models trained offline, frozen for production  
✅ **Graceful Degradation**: Web3 failures don't break the system  
✅ **Auditability**: Blockchain for immutable records, DB for operations

## 📁 Project Structure

```
defi-risk-backend/
├── main.py                    # Application entry point
├── config/
│   └── settings.py           # Centralized configuration
├── app/
│   ├── api/                  # HTTP endpoints only
│   │   ├── health.py        # Health checks
│   │   ├── predict.py       # Prediction routes
│   │   └── alerts.py        # Alert management
│   ├── services/            # Core business logic 🧠
│   │   ├── inference.py     # ML inference
│   │   └── scoring.py       # Risk scoring & decisions
│   ├── ml/                  # Model handling (read-only)
│   │   └── model_loader.py
│   ├── web3/                # Blockchain logic (isolated)
│   │   ├── client.py
│   │   └── alert_registry.py
│   ├── db/                  # Database operations
│   │   └── database.py
│   └── schemas/             # Pydantic models
│       └── models.py
├── scripts/
│   ├── train_model.py       # Model training pipeline
│   └── demo.py              # Demo script
├── models/                   # Trained models directory
└── requirements.txt
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Train Models

```bash
python scripts/train_model.py
```

This creates:
- `models/isolation_forest.pkl` - Trained anomaly detection model
- `models/scaler.pkl` - Feature scaler

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Start Server

```bash
python main.py
```

Server runs at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### 5. Run Demo

```bash
python scripts/demo.py
```

## 🎯 API Endpoints

### Health Checks
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/ready` - Readiness check (all dependencies)
- `GET /api/v1/health/live` - Liveness check

### Predictions
- `POST /api/v1/predict` - Single transaction prediction
- `POST /api/v1/predict/batch` - Batch predictions
- `GET /api/v1/predict/model-info` - Model information
- `GET /api/v1/predict/threshold` - Get alert threshold
- `POST /api/v1/predict/threshold` - Update alert threshold

### Alerts
- `GET /api/v1/alerts` - List alerts (with filters)
- `GET /api/v1/alerts/{id}` - Get specific alert
- `POST /api/v1/alerts/{id}/verify` - Verify alert
- `GET /api/v1/alerts/stats` - System statistics

## 📊 Example Request

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "amount_usd": 5000000,
    "whale_tx": 1,
    "tx_count_user": 2,
    "rolling_volume_user": 10000000,
    "tx_hash": "0x123...",
    "wallet_address": "0xabc..."
  }'
```

Response:
```json
{
  "risk_score": 0.92,
  "risk_level": "critical",
  "is_alert": true,
  "threshold": 0.70,
  "confidence": 0.96,
  "timestamp": "2024-02-07T12:00:00"
}
```

## 🧠 How It Works

### 1. Feature Engineering
Transactions are converted to behavioral features:
- `amount_usd` - Transaction size
- `whale_tx` - Binary whale flag
- `tx_count_user` - Historical activity
- `rolling_volume_user` - Recent volume surge

### 2. Inference Pipeline
```python
Features → Scaler → Isolation Forest → Risk Score
```

### 3. Scoring Logic
```python
Risk Score → Classification → Alert Decision
```

Thresholds:
- **Critical**: ≥ 0.90
- **High**: ≥ 0.70
- **Medium**: ≥ 0.50
- **Low**: < 0.50

### 4. Alert Flow
```
High Risk → Database → Blockchain (async) → Notification
```

## 🔧 Configuration

### Risk Threshold Tuning

Update threshold dynamically:
```bash
curl -X POST "http://localhost:8000/api/v1/predict/threshold?new_threshold=0.75"
```

Or in `.env`:
```
HIGH_RISK_THRESHOLD=0.75
```

### Blockchain Configuration

Set in `.env`:
```
WEB3_NETWORK=sepolia
WEB3_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-key
ALERT_REGISTRY_CONTRACT=0x...
PRIVATE_KEY=your-private-key
```

## 🎨 Design Decisions

### Why Isolation Forest?
✅ No labeled attack data required  
✅ Fast training (<1 minute)  
✅ Interpretable risk scores  
✅ Production-ready performance

### Why Separate Inference & Scoring?
✅ Detection ≠ Decision logic  
✅ Easy threshold tuning per protocol  
✅ Clear architectural boundaries  
✅ Testable components

### Why Isolated Web3?
✅ Blockchain failures don't break API  
✅ Can run without Web3 for testing  
✅ Clear operational boundaries

## 📈 Production Considerations

1. **Model Retraining**: Schedule offline retraining with latest data
2. **Monitoring**: Track alert rates, false positives
3. **Caching**: Cache model in memory (already done)
4. **Rate Limiting**: Implement for public endpoints
5. **Authentication**: Add API keys for production
6. **Database**: Migrate to PostgreSQL for production
7. **Logging**: Add structured logging
8. **Metrics**: Prometheus/Grafana integration

## 🧪 Testing

```bash
# Run demo script
python scripts/demo.py

# Test specific endpoint
curl http://localhost:8000/api/v1/health
```

## 📝 Judge-Ready Talking Points

✅ **"We separate inference, decision-making, and persistence to avoid tight coupling"**

✅ **"Models are trained offline and only used for inference in production"**

✅ **"Blockchain is used for auditability, not computation"**

✅ **"The system fails gracefully - Web3 down? Backend still works"**

✅ **"Database is mutable, blockchain is authoritative"**

## 🤝 Contributing

This is a hackathon project demonstrating production-grade architecture for DeFi security.

## 📄 License

MIT License - See LICENSE file