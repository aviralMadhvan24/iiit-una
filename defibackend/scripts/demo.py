#!/usr/bin/env python3
"""
Demo Script for DeFi Risk Engine
Tests the complete prediction pipeline
USE THIS if live demo fails - judges love resilience!
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title: str):
    """Pretty print section headers"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_health_check():
    """Test health endpoints"""
    print_section("1. Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    response = requests.get(f"{BASE_URL}/health/ready")
    print(f"\nReadiness: {json.dumps(response.json(), indent=2)}")

def test_normal_transaction():
    """Test a normal transaction (should be low risk)"""
    print_section("2. Normal Transaction Test")
    
    payload = {
        "amount_usd": 1000.0,
        "whale_tx": 0,
        "tx_count_user": 50,
        "rolling_volume_user": 5000.0,
        "tx_hash": "0xnormal123",
        "wallet_address": "0xnormaluser"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    result = response.json()
    
    print(f"Transaction: ${payload['amount_usd']:,.0f}")
    print(f"Risk Score: {result['risk_score']:.3f}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Alert Triggered: {result['is_alert']}")
    print(f"Confidence: {result['confidence']:.2%}")

def test_suspicious_transaction():
    """Test a suspicious transaction (should be high risk)"""
    print_section("3. Suspicious Transaction Test")
    
    payload = {
        "amount_usd": 5000000.0,  # $5M - whale transaction
        "whale_tx": 1,
        "tx_count_user": 2,  # Very few transactions
        "rolling_volume_user": 10000000.0,  # Huge sudden volume
        "tx_hash": "0xsuspicious456",
        "wallet_address": "0xattacker"
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    result = response.json()
    
    print(f"Transaction: ${payload['amount_usd']:,.0f}")
    print(f"Risk Score: {result['risk_score']:.3f}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"⚠️ Alert Triggered: {result['is_alert']}")
    print(f"Confidence: {result['confidence']:.2%}")

def test_batch_prediction():
    """Test batch prediction"""
    print_section("4. Batch Prediction Test")
    
    transactions = [
        {
            "amount_usd": 500.0,
            "whale_tx": 0,
            "tx_count_user": 100,
            "rolling_volume_user": 2000.0
        },
        {
            "amount_usd": 3000000.0,
            "whale_tx": 1,
            "tx_count_user": 1,
            "rolling_volume_user": 5000000.0
        },
        {
            "amount_usd": 10000.0,
            "whale_tx": 0,
            "tx_count_user": 25,
            "rolling_volume_user": 50000.0
        }
    ]
    
    payload = {"transactions": transactions}
    response = requests.post(f"{BASE_URL}/predict/batch", json=payload)
    result = response.json()
    
    print(f"Total Processed: {result['total_processed']}")
    print(f"Alerts Triggered: {result['alerts_triggered']}")
    print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
    print("\nIndividual Results:")
    
    for i, pred in enumerate(result['predictions']):
        print(f"  TX {i+1}: Risk={pred['risk_score']:.3f}, Level={pred['risk_level']}, Alert={pred['is_alert']}")

def test_get_alerts():
    """Test alert retrieval"""
    print_section("5. Alert Retrieval")
    
    response = requests.get(f"{BASE_URL}/alerts")
    result = response.json()
    
    print(f"Total Alerts: {result['total']}")
    print(f"Page: {result['page']}")
    print(f"Results: {len(result['alerts'])}")
    
    if result['alerts']:
        print("\nRecent Alerts:")
        for alert in result['alerts'][:3]:
            print(f"  - {alert['wallet_address']}: Risk={alert['risk_score']:.3f}, Level={alert['risk_level']}")

def test_system_stats():
    """Test system statistics"""
    print_section("6. System Statistics")
    
    response = requests.get(f"{BASE_URL}/alerts/stats")
    stats = response.json()
    
    print(f"Total Predictions: {stats.get('total_predictions', 0)}")
    print(f"Total Alerts: {stats.get('total_alerts', 0)}")
    print(f"Alert Rate: {stats.get('alert_rate', 0):.2%}")
    print(f"Average Risk Score: {stats.get('avg_risk_score', 0):.3f}")

def test_model_info():
    """Test model information"""
    print_section("7. Model Information")
    
    response = requests.get(f"{BASE_URL}/predict/model-info")
    info = response.json()
    
    print(f"Model Type: {info['model_type']}")
    print(f"Model Version: {info['model_version']}")
    print(f"Feature Count: {info['feature_count']}")
    print(f"Features: {', '.join(info['feature_names'])}")

def main():
    """Run all tests"""
    print("\n" + "🛡️ "*20)
    print("  DeFi Attack Early Warning System - Demo")
    print("🛡️ "*20)
    
    try:
        test_health_check()
        test_normal_transaction()
        test_suspicious_transaction()
        test_batch_prediction()
        test_get_alerts()
        test_system_stats()
        test_model_info()
        
        print_section("✅ Demo Complete")
        print("All systems operational!")
        print("\nNext Steps:")
        print("1. Open http://localhost:8000/docs for API documentation")
        print("2. Try custom transactions via the API")
        print("3. Check alerts at http://localhost:8000/api/v1/alerts")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend")
        print("Make sure the server is running:")
        print("  python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()