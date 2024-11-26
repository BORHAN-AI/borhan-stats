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

// --------------------------------------------------------------------------------------------------------------------

// Function to fetch data from an API and plot it
async function createChart(apiEndpoint, chartId, label, xLabel, yLabel) {
    const response = await fetch(apiEndpoint);
    const data = await response.json();

    const labels = data.map(item => item.date);
    const values = data.map(item => item.count);

    new Chart(document.getElementById(chartId), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                tooltip: { enabled: true },
            },
            scales: {
                x: { title: { display: true, text: xLabel } },
                y: { title: { display: true, text: yLabel } },
            }
        }
    });
}

// Create all charts
createChart('/api/total_users_by_date', 'totalUsersByDateChart', 'Total Users by Date', 'Date', 'Users');
createChart('/api/daily_new_users', 'dailyNewUsersChart', 'Daily New Users', 'Date', 'Users');
createChart('/api/total_groups_by_date', 'totalGroupsByDateChart', 'Total Groups by Date', 'Date', 'Groups');
createChart('/api/daily_new_groups', 'dailyNewGroupsChart', 'Daily New Groups', 'Date', 'Groups');
createChart('/api/total_messages_by_date', 'totalMessagesByDateChart', 'Total Messages by Date', 'Date', 'Messages');
createChart('/api/daily_new_messages', 'dailyNewMessagesChart', 'Daily New Messages', 'Date', 'Messages');
