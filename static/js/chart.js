import 'https://cdn.jsdelivr.net/npm/chart.js';

export function renderChart(ctx, type, labels, title, dataValues, show) {
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: dataValues,
                backgroundColor: [
                    'rgba(0, 123, 255, 0.6)',  
                    'rgba(0, 200, 155, 0.6)',  
                    'rgba(255, 193, 7, 0.6)',  
                    'rgba(220, 53, 69, 0.6)'   
                ],
                borderColor: [
                    'rgba(0, 123, 255, 1)',    
                    'rgba(0, 200, 155, 1)',    
                    'rgba(255, 193, 7, 1)',    
                    'rgba(220, 53, 69, 1)'     
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: false, 
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: show,
                    }, 
                    ticks: {
                        color: 'white',
                        display: show, 
                    },
                },
                x: {
                    grid: {
                        display: show, 
                    }, 
                    ticks: {
                        color: 'white',
                        display: show, 
                    },
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: 'rgba(255, 255, 255, 1)',
                    }
                }
            }
        }
    });
}