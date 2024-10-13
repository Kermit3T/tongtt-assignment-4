document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const queryInput = document.getElementById('query');
    const resultsDiv = document.getElementById('results');
    const chartDiv = document.getElementById('chart');
    
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = queryInput.value;
        
        try {
            const response = await axios.post('/search', { query });
            const results = response.data;
            
            // Display results
            resultsDiv.innerHTML = results.map((result, index) => `
                <div class="document">
                    <h3>Document ${index + 1}</h3>
                    <p>${result.document}</p>
                    <p class="similarity-score">Similarity Score: ${result.score.toFixed(4)}</p>
                </div>
            `).join('');
            
            // Create bar chart
            const data = [{
                x: results.map((_, i) => `Doc ${i + 1}`),
                y: results.map(r => r.score),
                type: 'bar',
                marker: {
                    color: '#344E41', // Dark Green
                    opacity: 0.6 // Slight transparency
                }
            }];
            
            const layout = {
                title: 'Document Similarity Scores',
                xaxis: { title: 'Documents' },
                yaxis: { title: 'Cosine Similarity' },
                font: {
                    family: 'Roboto, sans-serif'
                },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            };
            
            Plotly.newPlot(chartDiv, data, layout);
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = '<p>An error occurred while searching.</p>';
        }
    });
});
