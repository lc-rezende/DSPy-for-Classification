# DSPy-for-Classification

Demo repository for DSPy framework applied in sentiment analysis classification.

---

**DSPy** is a declarative framework for building modular AI software. It allows you to iterate fast on structured code, rather than brittle strings, and offers algorithms that compile AI programs into effective prompts and weights for your language models, whether you're building simple classifiers, sophisticated RAG pipelines, or Agent loops.

For more information about the DSPy framework, access: https://dspy.ai/

## Slack Notifications

Send Slack alerts for high churn-risk sites derived from the trusted churn dataset.

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export SLACK_CHANNEL="#churn-alerts"
python scripts/notify_slack_high_risk.py
```
