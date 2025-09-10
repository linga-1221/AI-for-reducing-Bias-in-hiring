// File upload interaction
document.getElementById('resumeFile').addEventListener('change', function(e) {
    const fileLabel = document.getElementById('fileLabel');
    if (e.target.files.length > 0) {
        const fileName = e.target.files[0].name;
        fileLabel.innerHTML = '📄 Selected: ' + fileName;
        fileLabel.classList.add('file-selected');
    } else {
        fileLabel.innerHTML = '📎 Click to select PDF file or drag & drop here';
        fileLabel.classList.remove('file-selected');
    }
});

// Form submission
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const fileInput = document.getElementById('resumeFile');
    const jobRole = document.getElementById('jobRole').value;
    
    if (!fileInput.files[0]) {
        alert('Please select a PDF file');
        return;
    }
    
    if (!jobRole) {
        alert('Please select a job role');
        return;
    }
    
    formData.append('job_role', jobRole);
    formData.append('resume', fileInput.files[0]);
    
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        const result = document.getElementById('result');
        
        if (data.error) {
            result.innerHTML = '<h3>❌ Error:</h3><p>' + data.error + '</p>';
        } else {
            let html = '<h2>📊 Analysis Results</h2>';
            
            // Job Match Score
            html += '<div class="section">';
            html += '<h3>🎯 Job Match Analysis</h3>';
            html += '<div class="match-score" style="color: ' + (data.match_percentage > 70 ? '#28a745' : data.match_percentage > 40 ? '#f39c12' : '#e74c3c') + ';">';
            html += data.match_percentage + '%</div>';
            
            let matchLevel = '';
            let matchColor = '';
            if (data.match_percentage > 70) {
                matchLevel = '🎆 Excellent Match';
                matchColor = '#28a745';
            } else if (data.match_percentage > 40) {
                matchLevel = '🟡 Good Match';
                matchColor = '#f39c12';
            } else {
                matchLevel = '🔴 Limited Match';
                matchColor = '#e74c3c';
            }
            
            html += '<div style="text-align: center; margin: 20px 0; padding: 15px; background: rgba(255,255,255,0.8); border-radius: 10px;">';
            html += '<h4 style="color: ' + matchColor + '; margin-bottom: 10px;">' + matchLevel + '</h4>';
            html += '<div class="recommendation">' + data.recommendation + '</div>';
            html += '</div>';
            html += '</div>';
            
            // Skills Analysis
            html += '<div class="section">';
            html += '<h3>💼 Skills Analysis</h3>';
            html += '<h4>✅ Matching Skills:</h4>';
            html += '<div class="skills-list">';
            data.matching_skills.forEach(skill => {
                html += '<span class="skill-tag">' + skill + '</span>';
            });
            html += '</div>';
            
            if (data.missing_skills.length > 0) {
                html += '<h4>❌ Missing Skills:</h4>';
                html += '<div class="skills-list">';
                data.missing_skills.forEach(skill => {
                    html += '<span class="skill-tag missing-skill">' + skill + '</span>';
                });
                html += '</div>';
            }
            html += '</div>';
            
            // Bias Analysis
            html += '<div class="section">';
            html += '<h3>⚖️ Hiring Bias Detection Analysis</h3>';
            if (data.bias_detected) {
                html += '<div class="bias-warning">';
                html += '<h4>⚠️ Potential Bias Detected in Job Description:</h4>';
                data.bias_details.forEach(bias => {
                    html += '<div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.7); border-radius: 8px;">';
                    html += '<strong>📊 ' + bias.category + ' Bias:</strong> ';
                    html += '<span style="background: #fff; padding: 3px 8px; border-radius: 15px; margin: 0 5px; border: 1px solid #f39c12;">' + bias.words.join('</span> <span style="background: #fff; padding: 3px 8px; border-radius: 15px; margin: 0 5px; border: 1px solid #f39c12;">') + '</span>';
                    html += '</div>';
                });
                html += '<div style="margin-top: 15px; padding: 15px; background: rgba(255,255,255,0.9); border-radius: 10px; border-left: 4px solid #f39c12;">';
                html += '<strong>💡 Recommendation:</strong> Consider replacing biased terms with neutral alternatives to ensure fair hiring practices and attract diverse candidates.';
                html += '</div>';
                html += '</div>';
            } else {
                html += '<div class="bias-safe">';
                html += '<h4>✅ Bias-Free Job Description</h4>';
                html += '<p>No significant bias detected in the job description. The language appears to be neutral and inclusive, promoting fair hiring practices.</p>';
                html += '</div>';
            }
            html += '</div>';
            
            // Anonymized Resume
            html += '<div class="section">';
            html += '<h3>🔒 Bias-Free Anonymized Resume</h3>';
            html += '<p style="color: #7f8c8d; margin-bottom: 15px; font-style: italic;">Personal identifiers have been removed to ensure fair evaluation based solely on qualifications and skills.</p>';
            html += '<div style="background: linear-gradient(45deg, #f8f9fa, #e9ecef); padding: 20px; border-radius: 12px; border: 1px solid #dee2e6; max-height: 400px; overflow-y: auto;">';
            html += '<pre style="white-space: pre-wrap; font-family: \'Courier New\', monospace; font-size: 14px; line-height: 1.5; margin: 0;">' + data.anonymized_resume + '</pre>';
            html += '</div>';
            html += '</div>';
            
            result.innerHTML = html;
        }
        result.style.display = 'block';
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('result').innerHTML = '<h3>❌ Error:</h3><p>Network error: ' + error.message + '</p>';
        document.getElementById('result').style.display = 'block';
    });
});