def summarize_logs(logs):
    categories = {
        "Chrome": "Research",
        "PyCharm": "Coding",
        "Slack": "Communication",
        "Word": "Documentation",
    }

    summary = {}
    for log in logs:
        category = None
        for keyword, cat in categories.items():
            if keyword.lower() in log.lower():
                category = cat
                break
        category = category or "Other"
        summary[category] = summary.get(category, 0) + 1

    return summary
