function submitForm(formType) {
    const form = document.getElementById(`${formType}Form`);
    const formData = new FormData(form);
    
    // Show loading state
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    submitButton.innerHTML = 'Processing...';
    submitButton.disabled = true;

    fetch(`/get_${formType}_advice`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Reset button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;

        // Display the advice or error
        const resultDiv = document.getElementById(`${formType}Result`);
        if (data.error) {
            resultDiv.innerHTML = `<div class="error">${data.error}</div>`;
        } else {
            resultDiv.innerHTML = `<div class="advice">${data.advice}</div>`;
        }
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    })
    .catch(error => {
        // Reset button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;

        // Display error
        const resultDiv = document.getElementById(`${formType}Result`);
        resultDiv.innerHTML = '<div class="error">Failed to get advice. Please try again.</div>';
    });

    return false; // Prevent form submission
} 