$(document).ready(function () {
  let threshold = 60;
  $('#new-threshold-input').val(threshold);
  $('#new-threshold-input').keypress(function (event) {
    if (event.which === 13) {
      const newThreshold = parseInt($('#new-threshold-input').val());
      if (!isNaN(newThreshold)) {
        threshold = newThreshold;
        sendRequest();
      }
    }
  });


const gridOptions = {
    columnDefs: [],
    defaultColDef: { resizable: true },
  };
  new agGrid.Grid(document.querySelector('#ag-grid'), gridOptions);

  // Function to update grid data based on the selected datatype
  function updateGridData(datatype, data) {
    const websites = Object.keys(data.site_results);
    const algorithms = Object.keys(data.site_results[websites[0]]);

    // Define column definitions based on selected datatype
    const columnDefs = [
      {
        headerName: 'Website',
        field: 'website',
        cellRenderer: (params) => {
          var iframe = document.getElementById("iframe");
          var statusInfo = document.getElementById("status-info");
          const entry = params.value;
    
          const cellElement = document.createElement('a');
          cellElement.textContent = entry;
    
          cellElement.addEventListener('click', function (event) {
            event.preventDefault();
            
            // Get the domain from the clicked cell
            const domain = entry;
    
            // Replicate the same logic you used for the buttons
            switchContainer("iframeContainer");
            setActiveTab("iframeTab");
            active_domain = domain;
            setButtonBackgroundColor(active_domain);
            if (domain === 'firetrol.net') {
              iframe.src = "http://" + 'www.' + domain;
            } else {
              iframe.src = "http://" + domain;
            }
    
            // Fetch and display additional information
            const domainInfo = findDomainInfo(domain);
            if (domainInfo) {
              // Calculate the reduction percentage and display information
              const lineCountBefore = domainInfo['line_count_before'];
              const lineCountAfter = domainInfo['line_count_after'];
              const num_of_links = domainInfo['scrapped_links'];
              const reductionPercentage = ((lineCountBefore - lineCountAfter) / lineCountBefore * 100).toFixed(2);
              const textColorClass = reductionPercentage > 0 ? 'text-danger' : 'text-success';
    
              const infoHTML = `
                <p><strong>Number of links scraped : </strong> ${num_of_links}</p>
                <p><strong>Lines before Preprocessing:</strong> ${lineCountBefore}</p>
                <p><strong>Lines After Preprocessing:</strong> ${lineCountAfter}</p>
                <p><strong>Words Before Preprocessing:</strong> ${domainInfo['word_count_before']}</p>
                <p><strong>Words After Preprocessing:</strong> ${domainInfo['word_count_after']}</p>
                <p class="${textColorClass}"><strong>Reduction Percentage:</strong> ${reductionPercentage}%</p>
              `;
              statusInfo.innerHTML = infoHTML;
            } else {
              statusInfo.innerHTML = "no stats available";
            }
          });
    
          return cellElement;
        }
      }      
    ,
    ...algorithms.map((algorithm) => {
      const algorithmName = algorithm.split('_')[0] + '   %';
      return {
        headerName: algorithmName,
        field: algorithm,
        width: 150,
        cellStyle: (params) => {
          const similarity = parseFloat(params.value);
          if (similarity === -1) {
            return {
                backgroundColor: '#98989C'
            };
        } else {
            return {
                backgroundColor: similarity >= threshold ? '#90EE90' : '#FF7276'
            };
        }
        },
      };
    }),
  ];
    // Update the grid with new column definitions and data
    gridOptions.api.setColumnDefs(columnDefs);

    const rowData = websites.map((website) => {
      const row = { website };
      algorithms.forEach((algorithm) => {
        row[algorithm] = data.site_results[website][algorithm];
      });
      return row;
    });
    gridOptions.api.setRowData(rowData);
  }

  document.getElementById('datatype').addEventListener('change', () => {
    sendRequest();
  });

  document.getElementById('algorithm').addEventListener('change', () => {
    sendRequest();
  });

  document.getElementById('export-csv-button').addEventListener('click', () => {
    gridOptions.api.exportDataAsCsv();
  });

  sendRequest();

  function sendRequest() {
    const datatype = document.getElementById('datatype').value;
    const algorithm = document.getElementById('algorithm').value;

    fetch('/similarity_comparison', {
      method: 'POST',
      body: JSON.stringify({ datatype, algorithm }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Update the grid data based on the selected datatype
        updateGridData(datatype, data);
      })
      .catch((error) => {
        console.error('Error running algorithm:', error);
      });
  }

});