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

// Theme Switcher Functions:
const themeToggle = document.getElementById('themeToggle');
    const themeLabel = document.getElementById('themeLabel');
    const body = document.body;

    // Load theme from local storage on page load
    document.addEventListener('DOMContentLoaded', () => {
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            body.classList.add('dark-theme');
            themeToggle.checked = true;
            themeLabel.textContent = 'Dark Theme';
        }
    });

    // Toggle theme
    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            body.classList.add('dark-theme');
            themeLabel.textContent = 'Dark Theme';
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-theme');
            themeLabel.textContent = 'Light Theme';
            localStorage.setItem('theme', 'light');
        }
    });

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

async function createGrowthChart(apiEndpoint, chartId, label, xLabel, yLabel) {
    try {
        const response = await fetch(apiEndpoint);
        const data = await response.json();

        console.log(`Data for ${chartId}:`, data); // Debugging log

        const labels = data.map(item => item.date);
        const values = data.map(item => item.growth); // Adjust for growth

        new Chart(document.getElementById(chartId), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: values,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                    tooltip: { enabled: true }
                },
                scales: {
                    x: { title: { display: true, text: xLabel } },
                    y: {
                        title: { display: true, text: yLabel },
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error(`Failed to create chart (${chartId}):`, error);
    }
}

// Create all charts
createChart('/api/total_users_by_date', 'totalUsersByDateChart', 'Total Users by Date', 'Date', 'Users');
createChart('/api/daily_new_users', 'dailyNewUsersChart', 'Daily New Users', 'Date', 'Users');
createChart('/api/total_groups_by_date', 'totalGroupsByDateChart', 'Total Groups by Date', 'Date', 'Groups');
createChart('/api/daily_new_groups', 'dailyNewGroupsChart', 'Daily New Groups', 'Date', 'Groups');
createChart('/api/total_messages_by_date', 'totalMessagesByDateChart', 'Total Messages by Date', 'Date', 'Messages');
createChart('/api/daily_new_messages', 'dailyNewMessagesChart', 'Daily New Messages', 'Date', 'Messages');

createGrowthChart('/api/weekly_user_growth', 'weeklyUserGrowthChart', 'Weekly User Growth (%)', 'Date', 'Growth (%)');
createGrowthChart('/api/weekly_group_growth', 'weeklyGroupGrowthChart', 'Weekly Group Growth (%)', 'Date', 'Growth (%)');
createGrowthChart('/api/weekly_message_growth', 'weeklyMessageGrowthChart', 'Weekly Message Growth (%)', 'Date', 'Growth (%)');


// Pie Chart: User Count vs Language
new Chart(document.getElementById('userCountByLanguageChart'), {
    type: 'pie',
    data: {
        labels: ['fa', 'en', 'ar'],
        datasets: [{
            data: [59.9, 36.3, 3.8],
            backgroundColor: ['#FFC107', '#007BFF', '#FF5722']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: true },
            title: { display: true, text: 'User Count vs Language' }
        }
    }
});

// Pie Chart: Message Count vs Chat Type
new Chart(document.getElementById('messageCountByChatTypeChart'), {
    type: 'pie',
    data: {
        labels: ['User', 'Group'],
        datasets: [{
            data: [65.6, 34.4],
            backgroundColor: ['#FF5722', '#007BFF']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: true },
            title: { display: true, text: 'Message Count vs Chat Type' }
        }
    }
});

// Pie Chart: Message Count vs Language
new Chart(document.getElementById('messageCountByLanguageChart'), {
    type: 'pie',
    data: {
        labels: ['fa', 'en', 'ar'],
        datasets: [{
            data: [93.9, 3.9, 2.2],
            backgroundColor: ['#FFC107', '#007BFF', '#FF5722']
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: true },
            title: { display: true, text: 'Message Count vs Language' }
        }
    }
});