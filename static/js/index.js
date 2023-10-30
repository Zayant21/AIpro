var active_domain = null;

function findDomainInfo(domain) {
    for (var i = 0; i < result_dict.length; i++) {
        if (result_dict[i]['company_domain'] === domain) {
            return result_dict[i];
        }
    }
    return null; // Return null if the domain is not found in the data
}

/* Fetching Charts from Domain Name without PreProsessing*/
function Spacey_TFIDF_Chart_WO(domainId) {
    if (domainId in spacey_tfidf_dict_wo) {
        return spacey_tfidf_dict_wo[domainId];
    }
    return null;
}

function KeyBertWordChartWO(domainId) {
    if (domainId in keybert_relevance_dict_wo) {
        return keybert_relevance_dict_wo[domainId];
    }
    return null;
}

function rake_Unconstrained_Chart_WO(domainId) {
    if (domainId in rake_unconstrained_dict_wo) {
        return rake_unconstrained_dict_wo[domainId];
    }
    return null;
}

function nltk_Word_Chart_WO(domainId) {
    if (domainId in nltk_word_dict_wo) {
        return nltk_word_dict_wo[domainId];
    }
    return null;
}

function textrank_Phrase_Chart_WO(domainId) {
    if (domainId in textrank_phrase_dict_wo) {
        return textrank_phrase_dict_wo[domainId];
    }
    return null;
}


function yake_Phrase_Chart_WO(domainId) {
    if (domainId in yake_phrase_dict_wo) {
        return yake_phrase_dict_wo[domainId];
    }
    return null;
}

function pke_Phrase_Chart_WO(domainId) {
    if (domainId in pke_phrase_dict_wo) {
        return pke_phrase_dict_wo[domainId];
    }
    return null;
}

/* Fetching Charts from Domain Name with PreProsessing*/
function Spacey_TFIDF_Chart(domainId) {
    if (domainId in spacey_tfidf_dict) {
        return spacey_tfidf_dict[domainId];
    }
    return null;
}

function KeyBertWordChart(domainId) {
    if (domainId in keybert_relevance_dict) {
        return keybert_relevance_dict[domainId];
    }
    return null;
}

function rake_Unconstrained_Chart(domainId) {
    if (domainId in rake_unconstrained_dict) {
        return rake_unconstrained_dict[domainId];
    }
    return null;
}

function nltk_Word_Chart(domainId) {
    if (domainId in nltk_word_dict) {
        return nltk_word_dict[domainId];
    }
    return null;
}

function textrank_Phrase_Chart(domainId) {
    if (domainId in textrank_phrase_dict) {
        return textrank_phrase_dict[domainId];
    }
    return null;
}


function yake_Phrase_Chart(domainId) {
    if (domainId in yake_phrase_dict) {
        return yake_phrase_dict[domainId];
    }
    return null;
}

function pke_Phrase_Chart(domainId) {
    if (domainId in pke_phrase_dict) {
        return pke_phrase_dict[domainId];
    }
    return null;
}

//to make the current company domain button active 
function toggleActive(button) {
    var buttons = document.querySelectorAll('.company-domain');
    buttons.forEach(function(btn) {
        btn.classList.remove('active');
    });
    button.classList.add('active');
}

function setButtonBackgroundColor(domain) {
    const button = document.getElementById(`company-button-${domain}`);
    if (button) {
        toggleActive(button);
        scrollToListItem(domain);
    }
}
function scrollToListItem(domain) {
    const button = document.getElementById(`company-button-${domain}`);
    if (button) {
        const list = button.closest('ul');
        if (list) {
            list.scrollTop = button.offsetTop - list.offsetTop;
        }
    }
}

// Function to switch between tabs
function setActiveTab(tabId) {
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove("active");
    }
    document.getElementById(tabId).classList.add("active");
}

// Function to switch between containers
function switchContainer(containerType) {
    // array of container IDs
    var containers = ["iframeContainer", "scrapedDataContainer", "processedDataContainer","barPlotContainer", "wordcloudContainer", "keywordsContainer", "similarityContainer", "resultsContainer","ResultGridContainer"];
    
    // Hide all containers
    containers.forEach(function(container) {
        document.getElementById(container).style.display = "none";
    });
    var temp_container = document.getElementById(containerType);
    temp_container.style.display = "block";
}

//set bar plot
function setBarPlot(domain_name, name) {
    if(domain_name === 'firetrol.net'){
        domain_name=domain_name+'.com';
    }
    var temp_container = document.getElementById('barPlotContainer');
    temp_container.innerHTML = '';

    var container = document.createElement('div');
    container.style.width = "1200px"; // Set the desired width

    // Create and add the first image and header
    var p_temp = document.createElement('h3');
    p_temp.textContent = `${name} without Preprocessing`;
    container.appendChild(p_temp);
    var image = document.createElement('img');
    image.src = `../static/images/${name}_lineplots/${domain_name}_lineplot.png`;
    image.alt = "Line Plot";
    // Set the width and height of the image
    image.style.width = "900px"; 
    image.style.height = "400px";
    container.appendChild(image);

    // Create and add the second image and header
    var p_temp1 = document.createElement('h3');
    p_temp1.textContent = `${name} with Preprocessing`;
    container.appendChild(p_temp1);
    var image1 = document.createElement('img');
    image1.src = `../static/images/${name}_p_lineplots/${domain_name}_lineplot.png`;
    image1.alt = "Line Plot";
    // Set the width and height of the image
    image1.style.width = "900px";
    image1.style.height = "400px";
    container.appendChild(image1);

    // Append the container to the main container
    temp_container.appendChild(container);
}


//set word cloud
function setWordCloud(domain_name, name){
    if(domain_name === 'firetrol.net'){
        domain_name=domain_name+'.com';
    }
    var temp_container = document.getElementById('wordcloudContainer');
    temp_container.innerHTML = '';

    var container = document.createElement('div');
    container.style.width = "1200px"; // Set the desired width

    // Create and add the first image and header
    var p_temp = document.createElement('h3');
    p_temp.textContent = `${name} without Preprocessing`;
    container.appendChild(p_temp);
    var image = document.createElement('img');
    image.src = `../static/images/${name}_wordclouds/${domain_name}_wordcloud.png`;
    image.alt = "Word Cloud";
    // Set the width and height of the image
    image.style.width = "900px"; 
    image.style.height = "400px";
    container.appendChild(image);

    // Create and add the second image and header
    var p_temp1 = document.createElement('h3');
    p_temp1.textContent = `${name} with Preprocessing`;
    container.appendChild(p_temp1);
    var image1 = document.createElement('img');
    image1.src = `../static/images/${name}_p_wordclouds/${domain_name}_wordcloud.png`;
    image1.alt = "Word Cloud";
    // Set the width and height of the image
    image1.style.width = "900px";
    image1.style.height = "400px";
    container.appendChild(image1);

    // Append the container to the main container
    temp_container.appendChild(container);
}

//Set Keywords
function setKeywords(domain_name){
    var domainInfo = findDomainInfo(domain_name);
    var keybert_relevance_dict_wo = KeyBertWordChartWO(domainInfo['id']);
    var spacey_tfidf_dict_wo = Spacey_TFIDF_Chart_WO(domainInfo['id']);
    var rake_unconstrained_dict_wo = rake_Unconstrained_Chart_WO(domainInfo['id']);
    var nltk_word_dict_wo = nltk_Word_Chart_WO(domainInfo['id']);
    var textrank_phrase_dict_wo = textrank_Phrase_Chart_WO(domainInfo['id']);
    var yake_phrase_dict_wo = yake_Phrase_Chart_WO(domainInfo['id']);
    var pke_phrase_dict_wo = pke_Phrase_Chart_WO(domainInfo['id']);

    var keybert_relevance_dict = KeyBertWordChart(domainInfo['id']);
    var spacey_tfidf_dict = Spacey_TFIDF_Chart(domainInfo['id']);
    var rake_unconstrained_dict = rake_Unconstrained_Chart(domainInfo['id']);
    var nltk_word_dict = nltk_Word_Chart(domainInfo['id']);
    var textrank_phrase_dict = textrank_Phrase_Chart(domainInfo['id']);
    var yake_phrase_dict = yake_Phrase_Chart(domainInfo['id']);
    var pke_phrase_dict = pke_Phrase_Chart(domainInfo['id']);
    if (keybert_relevance_dict_wo && keybert_relevance_dict) {
        var domainInfo = domainInfo['company_domain'];
        var wordHTML = '';

        wordHTML += '<div style="display: flex; justify-content: space-between;"><table>';
        wordHTML += '<tr><td><h3> Keybert Word Relevance w/o Pre Processing </h3>';
        wordHTML += '<table><tr><td><strong>Word</strong></td><td><strong>Relevance</strong></td></tr>';
    
        for (var i = 0; i < Math.min(20, keybert_relevance_dict_wo.length); i++) {
            var word = keybert_relevance_dict_wo[i]['word'];
            var relevance = keybert_relevance_dict_wo[i]['relevance'];
    
            wordHTML += `
                <tr>
                    <td>${word}</td>
                    <td>${relevance}</td>
                </tr>
            `;
        }
    
        wordHTML += '</table></td></tr></table>';

        var wordHTML_Processed = '<table>';
        wordHTML_Processed += '<tr><td><h3> Keybert Word Relevance Pre Processed </h3>';
        wordHTML_Processed += '<table><tr><td><strong>Word</strong></td><td><strong>Relevance</strong></td></tr>';
       
        for (var i = 0; i < Math.min(20, keybert_relevance_dict.length); i++) {
            var word = keybert_relevance_dict[i]['word'];
            var relevance = keybert_relevance_dict[i]['relevance'];
    
            wordHTML_Processed += `
                <tr>
                    <td>${word}</td>
                    <td>${relevance}</td>
                </tr>
            `;
        }
        wordHTML_Processed += '</table></td></tr></table>';
    
        // Display both tables side by side
        wordHTML += wordHTML_Processed + '</div>';
    
        keywordsContainer.innerHTML = wordHTML;
    } else {
        keywordsContainer.innerHTML = `<div style="color: red;"><h3>KeyBert relevance chart is not available for this site</h3></div>`;
    }

    if (spacey_tfidf_dict_wo && spacey_tfidf_dict) {
        wordHTML += '<div style="display: flex; justify-content: space-between;"><table>';
        wordHTML += '<tr><td><h3> Spacey Term Frequency Inverse Document Frequency w/o Pre Processing  </h3>';
        wordHTML += '<table><tr><td><strong>Word</strong></td><td><strong>TFIDF</strong></td></tr>';

        
        for (var i = 0; i < Math.min(20, spacey_tfidf_dict_wo.length); i++) {
            var word = spacey_tfidf_dict_wo[i]['word'];
            var tfidf = spacey_tfidf_dict_wo[i]['tfidf'];
    
            wordHTML += `
                <tr>
                    <td>${word}</td>
                    <td>${tfidf}</td>
                </tr>
            `;
        }
    
        wordHTML += '</table></td></tr></table>';

        var wordHTML_Processed = '<table>';
        wordHTML_Processed += '<tr><td><h3> Spacey Term Frequency Inverse Document Frequency Pre Processed</h3>';
        wordHTML_Processed += '<table><tr><td><strong>Word</strong></td><td><strong>TFIDF</strong></td></tr>';
        
        for (var i = 0; i < Math.min(20, spacey_tfidf_dict.length); i++) {
            var word = spacey_tfidf_dict[i]['word'];
            var tfidf = spacey_tfidf_dict[i]['tfidf'];
    
            wordHTML_Processed += `
                <tr>
                    <td>${word}</td>
                    <td>${tfidf}</td>
                </tr>
            `;
        }

        wordHTML_Processed += '</table></td></tr></table>';
        wordHTML += wordHTML_Processed + '</div>';

        keywordsContainer.innerHTML = wordHTML;
    } else {
        keywordsContainer.innerHTML += `<div style="color: red;"><h3>Spacey Term Frequency Inverse Document Frequency chart is not available for this site</h3></div>`;
    }

    if (textrank_phrase_dict_wo && textrank_phrase_dict) {
        wordHTML += '<div style="display: flex; justify-content: space-between;"><table>';
        wordHTML += '<tr><td><h3> Textrank Phrase Score w/o Pre Processing  </h3>';
        wordHTML += '<table><tr><td><strong>Phrase</strong></td><td><strong>Score</strong></td></tr>';

        
        for (var i = 0; i < Math.min(20, textrank_phrase_dict_wo.length); i++) {
            var phrase = textrank_phrase_dict_wo[i]['phrase'];
            var score = textrank_phrase_dict_wo[i]['score'];
    
            wordHTML += `
                <tr>
                    <td>${phrase}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }
    
        wordHTML += '</table></td></tr></table>';

        var wordHTML_Processed = '<table>';
        wordHTML_Processed += '<tr><td><h3> Textrank Phrase Score Pre Processed </h3>';
        wordHTML_Processed += '<table><tr><td><strong>Phrase</strong></td><td><strong>Score</strong></td></tr>';
        
        for (var i = 0; i < Math.min(20, textrank_phrase_dict.length); i++) {
            var phrase = textrank_phrase_dict[i]['phrase'];
            var score = textrank_phrase_dict[i]['score'];
    
            wordHTML_Processed += `
                <tr>
                    <td>${phrase}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }

        wordHTML_Processed += '</table></td></tr></table>';
        wordHTML += wordHTML_Processed + '</div>';

        keywordsContainer.innerHTML = wordHTML;
    } else {
        keywordsContainer.innerHTML += `<div style="color: red;"><h3>Textrank Phrase Score chart is not available for this site</h3></div>`;
    }

    if (nltk_word_dict_wo && nltk_word_dict) {
        wordHTML += '<div style="display: flex; justify-content: space-between;"><table>';
        wordHTML += '<tr><td><h3> NLTK Word Score w/o Pre Processing </h3>';
        wordHTML += '<table><tr><td><strong>Word</strong></td><td><strong>Score</strong></td></tr>';

        
        for (var i = 0; i < Math.min(20, nltk_word_dict_wo.length); i++) {
            var word = nltk_word_dict_wo[i]['word'];
            var score = nltk_word_dict_wo[i]['score'];
    
            wordHTML += `
                <tr>
                    <td>${word}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }
    
        wordHTML += '</table></td></tr></table>';

        var wordHTML_Processed = '<table>';
        wordHTML_Processed += '<tr><td><h3> NLTK Word Score Pre Processed  </h3>';
        wordHTML_Processed += '<table><tr><td><strong>Word</strong></td><td><strong>Score</strong></td></tr>';
        
        for (var i = 0; i < Math.min(20, nltk_word_dict.length); i++) {
            var word = nltk_word_dict[i]['word'];
            var score = nltk_word_dict[i]['score'];
    
            wordHTML_Processed += `
                <tr>
                    <td>${word}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }

        wordHTML_Processed += '</table></td></tr></table>';
        wordHTML += wordHTML_Processed + '</div>';

        keywordsContainer.innerHTML = wordHTML;
    } else {
        keywordsContainer.innerHTML += `<div style="color: red;"><h3>NLTK Word Score chart is not available for this site</h3></div>`;
    }

    if (yake_phrase_dict_wo && yake_phrase_dict) {
        wordHTML += '<div style="display: flex; justify-content: space-between;"><table>';
        wordHTML += '<tr><td><h3> Yake Phrase Score w/o Pre Processing </h3>';
        wordHTML += '<table><tr><td><strong>Phrase</strong></td><td><strong>Score</strong></td></tr>';

        
        for (var i = 0; i < Math.min(20, yake_phrase_dict_wo.length); i++) {
            var phrase = yake_phrase_dict_wo[i]['phrase'];
            var score = yake_phrase_dict_wo[i]['score'];
    
            wordHTML += `
                <tr>
                    <td>${phrase}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }
    
        wordHTML += '</table></td></tr></table>';

        var wordHTML_Processed = '<table>';
        wordHTML_Processed += '<tr><td><h3>  Yake Phrase Score Pre Processed  </h3>';
        wordHTML_Processed += '<table><tr><td><strong>Phrase</strong></td><td><strong>Score</strong></td></tr>';
        
        for (var i = 0; i < Math.min(20, yake_phrase_dict_wo.length); i++) {
            var word = yake_phrase_dict_wo[i]['phrase'];
            var score = yake_phrase_dict_wo[i]['score'];
    
            wordHTML_Processed += `
                <tr>
                    <td>${word}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }

        wordHTML_Processed += '</table></td></tr></table>';
        wordHTML += wordHTML_Processed + '</div>';

        keywordsContainer.innerHTML = wordHTML;
    } else {
        keywordsContainer.innerHTML += `<div style="color: red;"><h3>Yake Phrase Score chart is not available for this site</h3></div>`;
    }

    if (pke_phrase_dict_wo && pke_phrase_dict) {
        wordHTML += '<div style="display: flex; justify-content: space-between;"><table>';
        wordHTML += '<tr><td><h3> PKE Phrase Score w/o Pre Processing </h3>';
        wordHTML += '<table><tr><td><strong>Phrase</strong></td><td><strong>Score</strong></td></tr>';

        
        for (var i = 0; i < Math.min(20, pke_phrase_dict_wo.length); i++) {
            var phrase = pke_phrase_dict_wo[i]['phrase'];
            var score = pke_phrase_dict_wo[i]['score'];
    
            wordHTML += `
                <tr>
                    <td>${phrase}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }
    
        wordHTML += '</table></td></tr></table>';

        var wordHTML_Processed = '<table>';
        wordHTML_Processed += '<tr><td><h3> PKE Phrase Score Pre Processed  </h3>';
        wordHTML_Processed += '<table><tr><td><strong>Phrase</strong></td><td><strong>Score</strong></td></tr>';
        
        for (var i = 0; i < Math.min(20, pke_phrase_dict.length); i++) {
            var phrase = pke_phrase_dict[i]['phrase'];
            var score = pke_phrase_dict[i]['score'];
    
            wordHTML_Processed += `
                <tr>
                    <td>${phrase}</td>
                    <td>${score}</td>
                </tr>
        
            `;
        }

        wordHTML_Processed += '</table></td></tr></table>';
        wordHTML += wordHTML_Processed + '</div>';

        keywordsContainer.innerHTML = wordHTML;
    } else {
        keywordsContainer.innerHTML += `<div style="color: red;"><h3>PKE Phrase Score chart is not available for this site</h3></div>`;
    }

    if (rake_unconstrained_dict_wo && rake_unconstrained_dict) {
        wordHTML += '<div style="display: flex; justify-content: space-between;"><table>';
        wordHTML += '<tr><td><h3> Rake Unconstrained Key Phrases w/o Pre Processing</h3>';
        wordHTML += '<table><tr><td><strong>Key Phrase</strong></td><td><strong>Score</strong></td></tr>';

        
        for (var i = 0; i <  Math.min(20, rake_unconstrained_dict_wo.length); i++) {
            var key_phrase = rake_unconstrained_dict_wo[i]['key_phrase'];
            var score = rake_unconstrained_dict_wo[i]['score'];
    
            wordHTML += `
            <tr>
                <td>${key_phrase}</td>
                <td>${score}</td>
            </tr>
            `;
        }
    
        wordHTML += '</table></td></tr></table>';

        var wordHTML_Processed = '<table>';
        wordHTML_Processed += '<tr><td><h3> Rake Unconstrained Key Phrases Pre Processed</h3>';
        wordHTML_Processed += '<table><tr><td><strong>Word</strong></td><td><strong>TFIDF</strong></td></tr>';
        
        for (var i = 0; i <  Math.min(20, rake_unconstrained_dict.length); i++) {
            var key_phrase = rake_unconstrained_dict[i]['key_phrase'];
            var score = rake_unconstrained_dict[i]['score'];
    
            wordHTML_Processed += `
            <tr>
                <td>${key_phrase}</td>
                <td>${score}</td>
            </tr>
            `;
        }

        wordHTML_Processed += '</table></td></tr></table>';
        wordHTML += wordHTML_Processed + '</div>';

        keywordsContainer.innerHTML = wordHTML;
    } else {
        keywordsContainer.innerHTML += `<div style="color: red;"><h3>Spacey Term Frequency Inverse Document Frequency chart is not available for this site</h3></div>`;
    }
}

//set Similarity
function setSimilarity(domain_name) {
    if(domain_name === 'firetrol.net'){
        domain_name=domain_name+'.com';
    }
    var temp_container = document.getElementById('similarityContainer');
    temp_container.innerHTML = '';
    temp_container.innerHTML=`<img src="../static/images/similarity_scores/${domain_name}_lineplot.png" alt="Similarity Score">`;;
}

//set Results
function setResults(){
    var temp_container = document.getElementById('resultsContainer');
    temp_container.innerHTML = '';
    temp_container.innerHTML=`<img src="../static/images/results/barplot.png" alt="Results">`;
}

//set Wiz
function setWiz(){
    var temp_container = document.getElementById('wizContainer');
    temp_container.innerHTML = '';

    var container = document.createElement('div');
    container.style.width = "1200px"; // Set the desired width

    // Create and add the first image and header
    var p_temp = document.createElement('h3');
    p_temp.textContent = `Wiz List compared with Reference`;
    container.appendChild(p_temp);
    var image = document.createElement('img');
    image.src = `../static/images/wiz_result/wiz_reference_barplot.png`;
    image.alt = "Wiz Result";
    // Set the width and height of the image
    image.style.width = "900px"; 
    image.style.height = "400px";
    container.appendChild(image);

    // Create and add the second image and header
    var p_temp1 = document.createElement('h3');
    p_temp1.textContent = `Wiz List compared with Distributors`;
    container.appendChild(p_temp1);
    var image1 = document.createElement('img');
    image1.src = `../static/images/wiz_result/wiz_distributors_barplot .png`;
    image1.alt = "Wiz Result";
    // Set the width and height of the image
    image1.style.width = "900px";
    image1.style.height = "400px";
    container.appendChild(image1);

    // Append the container to the main container
    temp_container.appendChild(container);
}

function setScrapedData(domain_name){
    var new_name = domain_name.replace(/\.com/g, '');
    var temp_container = document.getElementById('scrapedDataContainer');
    temp_container.innerHTML='';
    var p_temp = document.createElement('p');
    p_temp.textContent = "Lines";
    temp_container.appendChild(p_temp);
    var reader = new FileReader();

    reader.onload = function(event) {
        var text = event.target.result;
        var lines = text.split('\n');
        var count =0;
        lines.forEach(function(line) {
            if (line.trim() !== '') {
                // Create a new paragraph element for each non-empty line
                var paragraph = document.createElement('p');
                paragraph.textContent = line;
                temp_container.appendChild(paragraph);
                count++;
            }
        });
        p_temp.innerHTML = `Lines - ${count} lines`;
    };

    // Read the file specified by the filePath
    fetch(`../static/scrapped_files/${new_name}.txt`)
        .then(response => response.text())
        .then(data => {
            reader.readAsText(new Blob([data]));
        })
        .catch(error => {
            console.error('Error reading the file: ', error);
        });
}

function setProcessedData_One(domain_name){
    var new_name = domain_name.replace(/\.com/g, '');;
    var temp_container = document.getElementById('processedDataContainer');
    temp_container.innerHTML='';
    var p_temp = document.createElement('h1');
    p_temp.textContent = "Algorithm 1 (RAB)";
    temp_container.appendChild(p_temp);
    var reader = new FileReader();

    reader.onload = function(event) {
        var text = event.target.result;
        var lines = text.split('\n');
        var count=0;
        lines.forEach(function(line) {
            line = line.trim();
            // Split the line into words
            var words = line.split(/\s+/);
            if (line.trim() !== '' && line.length >= 4 && words.length > 3 && /^[a-zA-Z]/.test(line)) {
                count++;
                // Create a new paragraph element for each non-empty line
                var paragraph = document.createElement('p');
                paragraph.textContent = line;
                temp_container.appendChild(paragraph);
            }
        });
        p_temp.innerHTML = `Algorithm 1 (RAB) - ${count} lines`;
    };

    // Read the file specified by the filePath
    fetch(`../static/scrapped_files/${new_name}.txt`)
        .then(response => response.text())
        .then(data => {
            reader.readAsText(new Blob([data]));
        })
        .catch(error => {
            console.error('Error reading the file: ', error);
        });
}

function setProcessedData_Two(domain_name){
    var new_name = domain_name.replace(/\.com/g, '');
    var temp_container = document.getElementById('processedDataContainer');
    temp_container.innerHTML='';
    var p_temp = document.createElement('h1');
    p_temp.textContent = "JusText";
    temp_container.appendChild(p_temp);
    var reader = new FileReader();

    reader.onload = function(event) {
        var text = event.target.result;
        var lines = text.split('\n');
        var count =0;
        lines.forEach(function(line) {
            if (line.trim() !== '') {
                // Create a new paragraph element for each non-empty line
                var paragraph = document.createElement('p');
                paragraph.textContent = line;
                temp_container.appendChild(paragraph);
                count++;
            }
        });
        p_temp.innerHTML = `JusText - ${count} Lines`;
    };

    // Read the file specified by the filePath
    fetch(`../static/JusText_scraped_files/${new_name}.txt`)
        .then(response => response.text())
        .then(data => {
            reader.readAsText(new Blob([data]));
        })
        .catch(error => {
            console.error('Error reading the file: ', error);
        });
}

function setProcessedData_Three(domain_name){
    var new_name = domain_name.replace(/\.com/g, '');
    var temp_container = document.getElementById('processedDataContainer');
    temp_container.innerHTML='';
    var p_temp = document.createElement('h1');
    p_temp.textContent = "Goose";
    temp_container.appendChild(p_temp);
    var reader = new FileReader();

    reader.onload = function(event) {
        var text = event.target.result;
        var lines = text.split('\n');
        var count =0;
        lines.forEach(function(line) {
            if (line.trim() !== '') {
                // Create a new paragraph element for each non-empty line
                var paragraph = document.createElement('p');
                paragraph.textContent = line;
                temp_container.appendChild(paragraph);
                count++;
            }
        });
        p_temp.innerHTML = `Goose - ${count} Lines`;
    };

    // Read the file specified by the filePath
    fetch(`../static/Goose_scraped_files/${new_name}.txt`)
        .then(response => response.text())
        .then(data => {
            reader.readAsText(new Blob([data]));
        })
        .catch(error => {
            console.error('Error reading the file: ', error);
        });
}

$(document).ready(function () {
    var elements = document.getElementsByClassName("company-domain");
    var iframe = document.getElementById("iframe");
    var statusInfo = document.getElementById("status-info");
    var keywordsContainer = document.getElementById("keywordsContainer");
    switchContainer("iframeContainer");
    setActiveTab("iframeTab");
    
    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener("click", function () {
            switchContainer("iframeContainer");
            setActiveTab("iframeTab");
            var domain = this.innerText;
            active_domain = domain;
            if (domain === 'firetrol.net') {
                iframe.src = "http://" + 'www.' + domain;
            } else {
                iframe.src = "http://" + domain;
            }

            // Fetch and display additional information
            var domainInfo = findDomainInfo(domain);
            if (domainInfo) {

                // Calculate the reduction percentage
                var lineCountBefore = domainInfo['line_count_before'];
                var lineCountAfter = domainInfo['line_count_after'];
                var num_of_links = domainInfo['scrapped_links'];
                var reductionPercentage = ((lineCountBefore - lineCountAfter) / lineCountBefore * 100).toFixed(2);

                var textColorClass = reductionPercentage > 0 ? 'text-danger' : 'text-success';

                var infoHTML = `
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
    }

    // to handle tab switching
    document.getElementById("iframeTab").addEventListener("click", function () {
        switchContainer("iframeContainer");
        setActiveTab("iframeTab");
    });

    document.getElementById("scrapedDataTab").addEventListener("click", function () {
        switchContainer("scrapedDataContainer");
        setActiveTab("scrapedDataTab");
        if(active_domain != null){
            setScrapedData(active_domain);
        }
    });

    // Algo one
    document.getElementById("algo_one").addEventListener("click", function () {
        switchContainer("processedDataContainer");
        setActiveTab("processedDataTab");
        if(active_domain != null){
            setProcessedData_One(active_domain);
        }
    });

    //Algo Two
    document.getElementById("algo_two").addEventListener("click", function () {
        switchContainer("processedDataContainer");
        setActiveTab("processedDataTab");
        if(active_domain != null){
            setProcessedData_Two(active_domain);
        }
    });

    //Algo Three
    document.getElementById("algo_three").addEventListener("click", function () {
        switchContainer("processedDataContainer");
        setActiveTab("processedDataTab");
        if(active_domain != null){
            setProcessedData_Three(active_domain);
        }
    });

    // Line Plot Yake
    document.getElementById("bar_yake").addEventListener("click", function () {
        switchContainer("barPlotContainer");
        setActiveTab("barPlotTab");
        if(active_domain != null){
            setBarPlot(active_domain, 'yake');
        }
    });

    // Line Plot keybert
    document.getElementById("bar_keybert").addEventListener("click", function () {
        switchContainer("barPlotContainer");
        setActiveTab("barPlotTab");
        if(active_domain != null){
            setBarPlot(active_domain, 'keybert');
        }
    });

    // Line Plot nltk
    document.getElementById("bar_nltk").addEventListener("click", function () {
        switchContainer("barPlotContainer");
        setActiveTab("barPlotTab");
        if(active_domain != null){
            setBarPlot(active_domain, 'nltk');
        }
    });

    // Line Plot textrank
    document.getElementById("bar_textrank").addEventListener("click", function () {
        switchContainer("barPlotContainer");
        setActiveTab("barPlotTab");
        if(active_domain != null){
            setBarPlot(active_domain, 'textrank');
        }
    });

    // Line Plot spacy
    document.getElementById("bar_spacy").addEventListener("click", function () {
        switchContainer("barPlotContainer");
        setActiveTab("barPlotTab");
        if(active_domain != null){
            setBarPlot(active_domain, 'spacy');
        }
    });

    // Line Plot pke
    document.getElementById("bar_pke").addEventListener("click", function () {
        switchContainer("barPlotContainer");
        setActiveTab("barPlotTab");
        if(active_domain != null){
            setBarPlot(active_domain, 'pke');
        }
    });

    // Line Plot rake
    document.getElementById("bar_rake").addEventListener("click", function () {
        switchContainer("barPlotContainer");
        setActiveTab("barPlotTab");
        if(active_domain != null){
            setBarPlot(active_domain, 'rake');
        }
    });

    // Word Cloud Yake
    document.getElementById("word_yake").addEventListener("click", function () {
        switchContainer("wordcloudContainer");
        setActiveTab("wordCloudTab");
        if(active_domain != null){
            setWordCloud(active_domain, 'yake');
        }
    });

    // Word Cloud keybert
    document.getElementById("word_keybert").addEventListener("click", function () {
        switchContainer("wordcloudContainer");
        setActiveTab("wordCloudTab");
        if(active_domain != null){
            setWordCloud(active_domain, 'keybert');
        }
    });

    // Word Cloud nltk
    document.getElementById("word_nltk").addEventListener("click", function () {
        switchContainer("wordcloudContainer");
        setActiveTab("wordCloudTab");
        if(active_domain != null){
            setWordCloud(active_domain, 'nltk');
        }
    });

    // Word Cloud textrank
    document.getElementById("word_textrank").addEventListener("click", function () {
        switchContainer("wordcloudContainer");
        setActiveTab("wordCloudTab");
        if(active_domain != null){
            setWordCloud(active_domain, 'textrank');
        }
    });

    // Word Cloud spacy
    document.getElementById("word_spacy").addEventListener("click", function () {
        switchContainer("wordcloudContainer");
        setActiveTab("wordCloudTab");
        if(active_domain != null){
            setWordCloud(active_domain, 'spacy');
        }
    });

    // Word Cloud pke
    document.getElementById("word_pke").addEventListener("click", function () {
        switchContainer("wordcloudContainer");
        setActiveTab("wordCloudTab");
        if(active_domain != null){
            setWordCloud(active_domain, 'pke');
        }
    });

    // Word Cloud rake
    document.getElementById("word_rake").addEventListener("click", function () {
        switchContainer("wordcloudContainer");
        setActiveTab("wordCloudTab");
        if(active_domain != null){
            setWordCloud(active_domain, 'rake');
        }
    });

    document.getElementById("keywordsTab").addEventListener("click", function () {
        switchContainer("keywordsContainer");
        setActiveTab("keywordsTab");
        if(active_domain != null){
            setKeywords(active_domain);
        }
    });


    // Set Similarity
    document.getElementById("similarityTab").addEventListener("click", function () {
        switchContainer("similarityContainer");
        setActiveTab("similarityTab");
        if(active_domain != null){
            setSimilarity(active_domain);
        }
    });

    // Set the result
    document.getElementById("resultTab").addEventListener("click", function () {
        switchContainer("resultsContainer");
        setActiveTab("resultTab");
        if(active_domain != null){
            setResults();
        }
    });
    
    // Set the result
    // document.getElementById("wizTab").addEventListener("click", function () {
    //     switchContainer("wizContainer");
    //     setActiveTab("wizTab");
    //     if(active_domain != null){
    //         setWiz();
    //     }
    // });

    document.getElementById("resultgridTab").addEventListener("click", function () {
        switchContainer("ResultGridContainer");
        setActiveTab("resultgridTab");

    });
});
