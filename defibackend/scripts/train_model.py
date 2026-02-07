#!/usr/bin/env python3
"""
Mock Model Training Script
Creates dummy trained models for demo purposes
In production, this would be a separate training pipeline
"""
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pathlib import Path

def create_mock_training_data():
    """
    Create synthetic training data mimicking normal DeFi behavior
    """
    np.random.seed(42)
    
    # Normal transactions (90% of data)
    n_normal = 900
    normal_data = np.column_stack([
        np.random.lognormal(8, 2, n_normal),  # amount_usd: $3k-$30k typical
        np.random.binomial(1, 0.1, n_normal),  # whale_tx: 10% are whales
        np.random.poisson(50, n_normal),  # tx_count_user: ~50 transactions
        np.random.lognormal(10, 1.5, n_normal)  # rolling_volume: normal activity
    ])
    
    # Anomalous transactions (10% of data)
    n_anomaly = 100
    anomaly_data = np.column_stack([
        np.random.lognormal(13, 1, n_anomaly),  # amount_usd: $400k+ (whales)
        np.random.binomial(1, 0.9, n_anomaly),  # whale_tx: 90% are whales
        np.random.poisson(5, n_anomaly),  # tx_count_user: very few txs (new wallet)
        np.random.lognormal(14, 1, n_anomaly)  # rolling_volume: huge volume spike
    ])
    
    # Combine
    X = np.vstack([normal_data, anomaly_data])
    
    return X

def train_model():
    """
    Train Isolation Forest model
    """
    print("🔬 Generating synthetic training data...")
    X = create_mock_training_data()
    
    print(f"📊 Training set size: {X.shape[0]} samples, {X.shape[1]} features")
    
    # Step 1: Fit scaler
    print("⚙️ Fitting StandardScaler...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Step 2: Train Isolation Forest
    print("🌲 Training Isolation Forest...")
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,  # Expect 10% anomalies
        random_state=42,
        max_samples='auto'
    )
    model.fit(X_scaled)
    
    # Step 3: Validate
    print("✅ Model training complete")
    scores = -model.score_samples(X_scaled)
    print(f"   Mean anomaly score: {scores.mean():.3f}")
    print(f"   Score range: [{scores.min():.3f}, {scores.max():.3f}]")
    
    return model, scaler

def save_models(model, scaler):
    """
    Save trained models to disk
    """
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / "isolation_forest.pkl"
    scaler_path = models_dir / "scaler.pkl"
    
    print(f"\n💾 Saving models...")
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    print(f"   ✅ Model saved to {model_path}")
    print(f"   ✅ Scaler saved to {scaler_path}")

def test_model(model, scaler):
    """
    Test the trained model
    """
    print("\n🧪 Testing model...")
    
    # Normal transaction
    normal_tx = np.array([[5000, 0, 50, 10000]])
    normal_scaled = scaler.transform(normal_tx)
    normal_score = -model.score_samples(normal_scaled)[0]
    
    # Suspicious transaction
    suspicious_tx = np.array([[5000000, 1, 2, 10000000]])
    suspicious_scaled = scaler.transform(suspicious_tx)
    suspicious_score = -model.score_samples(suspicious_scaled)[0]
    
    print(f"   Normal TX score: {normal_score:.3f}")
    print(f"   Suspicious TX score: {suspicious_score:.3f}")
    print(f"   Ratio: {suspicious_score / normal_score:.2f}x")

def main():
    """
    Main training pipeline
    """
    print("\n" + "="*60)
    print("  DeFi Risk Engine - Model Training")
    print("="*60 + "\n")
    
    # Train
    model, scaler = train_model()
    
    # Test
    test_model(model, scaler)
    
    # Save
    save_models(model, scaler)
    
    print("\n✅ Training pipeline complete!")
    print("\nℹ️ In production, this would:")
    print("   1. Use real historical transaction data")
    print("   2. Perform extensive feature engineering")
    print("   3. Validate on held-out test set")
    print("   4. Track model performance metrics")
    print("   5. Version models for reproducibility")

if __name__ == "__main__":
    main()