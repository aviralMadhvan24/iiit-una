ALERTS = []

def add_alert(alert: dict):
    ALERTS.append(alert)

def get_alerts():
    return ALERTS

def get_alert_stats():
    total = len(ALERTS)
    if total == 0:
        return {
            "total_alerts": 0,
            "avg_risk_score": 0,
            "alert_rate": 0,
            "total_predictions": 0,
        }

    avg_risk = sum(a["risk_score"] for a in ALERTS) / total

    return {
        "total_alerts": total,
        "avg_risk_score": avg_risk,
        "alert_rate": total / max(total, 1),
        "total_predictions": total,
    }
