def compute_running_total(data):
    """Compute running total for the given date-wise data."""
    running_total = 0
    cumulative_data = []
    for entry in data:
        running_total += entry['count']
        cumulative_data.append({'date': entry['date'], 'count': running_total})
    return cumulative_data
