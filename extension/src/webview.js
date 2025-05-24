const vscode = acquireVsCodeApi();

function submit() {
    const input = document.getElementById('responseInput');
    const text = input.value.trim();
    console.log('Submit function called with text:', text);
    
    try {
        vscode.postMessage({
            command: 'submit',
            text: text
        });
        console.log('Message sent successfully');
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

function cancel() {
    console.log('Cancel function called');
    try {
        vscode.postMessage({
            command: 'cancel'
        });
        console.log('Cancel message sent successfully');
    } catch (error) {
        console.error('Error sending cancel message:', error);
    }
}

// Handle keyboard events
function handleKeyDown(e) {
    console.log('Key pressed:', e.key, 'Ctrl:', e.ctrlKey, 'Shift:', e.shiftKey);
    
    if (e.ctrlKey && e.key === 'Enter') {
        console.log('Ctrl+Enter detected - submitting');
        e.preventDefault();
        submit();
        return;
    }
    
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
        console.log('Enter detected - submitting');
        e.preventDefault();
        submit();
        return;
    }
    
    if (e.key === 'Enter' && e.shiftKey) {
        console.log('Shift+Enter detected - allowing new line');
        // Allow default behavior for new line
        return;
    }
}

// Set up event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    
    const responseInput = document.getElementById('responseInput');
    const submitBtn = document.querySelector('.submit-btn');
    const cancelBtn = document.querySelector('.cancel-btn');
    
    if (responseInput) {
        responseInput.addEventListener('keydown', handleKeyDown);
        responseInput.focus();
        console.log('Event listeners added to textarea');
    } else {
        console.error('responseInput element not found!');
    }
    
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            console.log('Submit button clicked');
            submit();
        });
        console.log('Submit button event listener added');
    } else {
        console.error('Submit button not found!');
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            console.log('Cancel button clicked');
            cancel();
        });
        console.log('Cancel button event listener added');
    } else {
        console.error('Cancel button not found!');
    }
});

// Backup: Also try on window load
window.addEventListener('load', function() {
    console.log('Window loaded');
    const responseInput = document.getElementById('responseInput');
    if (responseInput) {
        responseInput.focus();
        console.log('Input focused on window load');
    }
}); 