async function fetchStats() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        document.getElementById('userCount').innerText = data.user_count;
        document.getElementById('groupCount').innerText = data.group_count;
        document.getElementById('messageCount').innerText = data.message_count_today;
    } catch (error) {
        console.error('Failed to fetch stats:', error);
    }
}

// Refresh stats every 5 seconds
setInterval(fetchStats, 5000);
fetchStats();
