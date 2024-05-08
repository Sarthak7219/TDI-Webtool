//UNSENSORED-GRAPH
    var myDataArray = []; // Create an array to store the data

    for (var i = 1; i <= 18; i++) {
        var myDattaElement = document.getElementById(`my-data_uncensored${i}`);
        var myDatta = myDattaElement.getAttribute("data-my-data");
        myDataArray.push(myDatta); // Store the data in the array
    }



    const uncensored_data = {
        labels: ['Chronic Disease', 'Immunisation', 'Maternal Care', 'Under 5 child mortality', 'Food Security', 'Level of Education', 'Drop-out', 'Institutional Credit', 'Land Ownership', 'Sanitation', 'Cooking Fuel', 'Source of Drinking Water', 'Electricity', 'Assets', 'Language', 'Arts and Culture', 'Voted', 'Meetings'],
        datasets: [
            {
                label: 'Uncensored',
                data: myDataArray,
                fill: false,
                backgroundColor: [
                    '#BDD7EE',
                    '#BDD7EE',
                    '#BDD7EE',
                    '#BDD7EE',
                    '#BDD7EE',
                    '#C5E0B4',
                    '#C5E0B4',
                    '#FFE699',
                    '#FFE699',
                    '#FFE699',
                    '#FFE699',
                    '#FFE699',
                    '#FFE699',
                    '#FFE699',
                    '#D9D9D9',
                    '#D9D9D9',
                    '#F8CBAD',
                    '#F8CBAD',
                ],
                // borderColor: 'rgba(75,192,192,1)',
                borderWidth: 1,
            },
        ],
    };

    const config_uncensored = {
        type: 'bar',
        data: uncensored_data,
        options: {
            indexAxis: 'y',
            scales: {
                xAxes: [
                    {
                        ticks: {
                            stepSize: 1,
                            beginAtZero: true,
                            autoSkip: false,

                        },

                    },
                ],
                y: 
                    {
                        ticks: {
                            stepSize: 1,
                            beginAtZero: true,
                            maxTicksLimit: 18,
                            autoSkip: false
                        },

                    },
                
                    y2: {
                        
                        labels: ['Health', 'Education', 'Sol', 'Culture', 'Governance'], // Replace with your desired labels
                        ticks: {
                            stepSize: 10,
                            beginAtZero: true,
                            maxTicksLimit: 9,
                            autoSkip: false,
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Custom Y2 Scale Name', // Replace with your desired scale name
                        },
                
                    },
                x: {
                    grid: {
                        drawOnChartArea: false,
                        display: false
                    }
                },
                y: {
                    grid: {
                        drawOnChartArea: false,
                        display: false
                    }
                }
            },
            plugins: {
                datalabels: {
                    formatter: (value, context) => {
                        return value + '%';
                    },
                    anchor: "end",
                    align: "right"
                }
            }
        },
        plugins: [ChartDataLabels]
    };

    const uncensored_graph = new Chart(document.getElementById('uncensored-graph'), config_uncensored);
    //*******************************************




      //CENSORED-GRAPH
      var censored_tribe_arr = {{ censored_tribe_arr| safe }}; // Create an array to store the data

      // Assuming you have an array of data for each category
      const healthData = censored_tribe_arr.slice(0, 5);
      const educationData = censored_tribe_arr.slice(5, 7);
      const standardOfLivingData = censored_tribe_arr.slice(7, 14);
      const cultureData = censored_tribe_arr.slice(14, 16);
      const governanceData = censored_tribe_arr.slice(16, 18);
  
      const censored_data = {
    labels: ['Chronic Disease', 'Food Security', 'Under 5 Child Mortality', 'Maternal Care', 'Immunisation', 'Drop-out', 'Level of Education', 'Assets', 'Electricity', 'Source of Drinking Water', 'Cooking Fuel', 'Sanitation', 'Land Ownership', 'Institutional Credit', 'Arts and Culture', 'Language', 'Meetings', 'Voted'],
    datasets: [
      {
        label: 'Health',
        data: healthData,
        fill: false,
        backgroundColor: '#BDD7EE',
        borderWidth: 1,
        yAxisID: 'y1', // Associate with the left Y-axis (y1)
      },
      {
        label: 'Education',
        data: educationData,
        fill: false,
        backgroundColor: '#C5E0B4',
        borderWidth: 1,
        yAxisID: 'y2', // Associate with the right Y-axis (y2)
      },
      {
        label: 'Culture',
        data: cultureData,
        fill: false,
        backgroundColor: '#F8CBAD',
        borderWidth: 1,
        yAxisID: 'y2', // Associate with the right Y-axis (y2)
      },
      {
        label: 'Governance',
        data: governanceData,
        fill: false,
        backgroundColor: '#D9D9D9',
        borderWidth: 1,
        yAxisID: 'y2', // Associate with the right Y-axis (y2)
      },
      {
        label: 'Standard of Living',
        data: standardOfLivingData,
        fill: false,
        backgroundColor: '#FFE699',
        borderWidth: 1,
        yAxisID: 'y2', // Associate with the right Y-axis (y2)
      },
    ],
  };
  
  const config_censored = {
    type: 'bar',
    data: censored_data,
    options: {
      indexAxis: 'y',
      scales: {
        x: {
          grid: {
            drawOnChartArea: false,
            display: false,
          },
        },
        y1: {
          position: 'left', // Left Y-axis for Health
          ticks: {
            stepSize: 1,
            beginAtZero: true,
            maxTicksLimit: 18,
            autoSkip: false,
          },
          title: {
            display: true,
            text: 'Health',
          },
        },
        y2: {
          position: 'right', // Right Y-axis for Education, Culture, Governance, Standard of Living
          ticks: {
            stepSize: 10,
            beginAtZero: true,
            maxTicksLimit: 9,
            autoSkip: false,
          },
          title: {
            display: true,
            text: 'Education, Culture, Governance, Standard of Living',
          },
        },
      },
      plugins: {
        datalabels: {
          formatter: (value, context) => {
            return value + '%';
          },
          anchor: 'end',
          align: 'right',
        },
      },
    },
    plugins: [ChartDataLabels],
  };
  
  const censored_graph = new Chart(document.getElementById('censored-graph'), config_censored);
  