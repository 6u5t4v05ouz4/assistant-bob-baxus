/**
 * Create charts for visualizing whisky collection data
 */

// Create spirit distribution chart
function createSpiritChart(data) {
    const ctx = document.getElementById('spiritChart').getContext('2d');
    
    // Extract labels and values
    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Define colors
    const backgroundColors = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)',
        'rgba(83, 102, 255, 0.7)',
        'rgba(40, 159, 64, 0.7)',
        'rgba(210, 199, 199, 0.7)'
    ];
    
    // Create the chart
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: backgroundColors.slice(0, labels.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#ffffff',
                        font: {
                            size: 12
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Spirit Types',
                    color: '#ffffff',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Create region distribution chart
function createRegionChart(data) {
    const ctx = document.getElementById('regionChart').getContext('2d');
    
    // Extract labels and values
    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Define colors
    const backgroundColors = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)',
        'rgba(83, 102, 255, 0.7)',
        'rgba(40, 159, 64, 0.7)',
        'rgba(210, 199, 199, 0.7)'
    ];
    
    // Create the chart
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: backgroundColors.slice(0, labels.length),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#ffffff',
                        font: {
                            size: 12
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Regions',
                    color: '#ffffff',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Create price distribution chart
function createPriceChart(data) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    // Extract labels and values
    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Create the chart
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Bottles',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Price Distribution',
                    color: '#ffffff',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Create age distribution chart
function createAgeChart(data) {
    const ctx = document.getElementById('ageChart').getContext('2d');
    
    // Extract labels and values
    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Create the chart
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Bottles',
                data: values,
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Age Distribution',
                    color: '#ffffff',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Create proof distribution chart
function createProofChart(data) {
    const ctx = document.getElementById('proofChart').getContext('2d');
    
    // Extract labels and values
    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Create the chart
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Bottles',
                data: values,
                backgroundColor: 'rgba(255, 159, 64, 0.7)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#ffffff'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Proof Distribution',
                    color: '#ffffff',
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}

// Initialize all charts if data is available
function initializeCharts(stats) {
    if (stats.spirits_count) {
        createSpiritChart(stats.spirits_count);
    }
    
    if (stats.regions_count) {
        createRegionChart(stats.regions_count);
    }
    
    if (stats.price_distribution) {
        createPriceChart(stats.price_distribution);
    }
    
    if (stats.age_distribution) {
        createAgeChart(stats.age_distribution);
    }
    
    if (stats.proof_distribution) {
        createProofChart(stats.proof_distribution);
    }
}
