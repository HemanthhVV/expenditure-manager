const ctx1 = document.getElementById('chart1');
const ctx2 = document.getElementById('chart2');
const ctx1_1 = document.getElementById('chart1_1');


const renderChart = (labels, datum) => {
    new Chart(ctx1, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Income Sources ',
                data: datum,
                borderWidth: 1
            }]
        },
        options: {
            title: "Hello",
            plugins: {
                title: {
                    display: true,  // Show the title
                    text: 'Income based by source',  // The title text
                    font: {
                        size: 18  // Font size for the title
                    },
                    padding: {
                        top: 10,
                        bottom: 20  // Padding for spacing around the title
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
const renderPolarChart = (labels, datum) => {
    new Chart(ctx1_1, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'source via times ',
                data: datum,
                borderWidth: 2,
                backgroundColor: [
                    'rgb(255, 99, 132,0.65)',
                    'rgb(75, 192, 192,0.65)',
                    'rgb(255, 205, 86,0.65)',
                    'rgb(201, 203, 207,0.65)',
                    'rgb(54, 162, 235,0.65)'
                ]
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,  // Show the title
                    text: 'Frequent incomes sources',  // The title text
                    font: {
                        size: 18  // Font size for the title
                    },
                    padding: {
                        top: 10,
                        bottom: 20  // Padding for spacing around the title
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

const renderLineChart = (labels, datum) => {
    new Chart(ctx2, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses Spent ',
                data: datum,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,  // Show the title
                    text: 'Income received with respect to time',  // The title text
                    font: {
                        size: 18  // Font size for the title
                    },
                    padding: {
                        top: 10,
                        bottom: 20  // Padding for spacing around the title
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

const getData = () => {
    fetch('/incomes/income-summary-category')
        .then(res => res.json())
        .then(data => {
            // category_wise, date_wise  = datum.dict, datum.date_wise;
            const { expense_wise, date_wise, category_wise } = data;
            renderChart(Object.keys(expense_wise), Object.values(expense_wise));
            renderLineChart(Object.keys(date_wise), Object.values(date_wise));
            renderPolarChart(Object.keys(category_wise), Object.values(category_wise));
        })

}

document.onload = getData()