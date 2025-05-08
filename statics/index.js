document.getElementById('ogp-form').addEventListener('submit', async function(event) {
    const formData = {};
    const fields = ['path', 'og_title', 'og_description', 'og_image', 'og_url'];

    fields.forEach(field => {
        const value = document.getElementById(field).value.trim();
        if (value) {
            formData[field] = value;
        }
    });

    try {
        const response = await fetch('/api/ogp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        const messageDiv = document.getElementById('response-message');
        if (response.ok) {
            const path = result.ogp.path;
            const fullUrl = `${window.location.origin}/${path}`;
            messageDiv.innerHTML = `
                OGP created successfully!<br><strong>${fullUrl}</strong>
                <button id="copy-path" style="margin-left: 10px;">Copy</button>
            `;
            messageDiv.style.color = 'green';

            document.getElementById('copy-path').addEventListener('click', () => {
                copyToClipboard(fullUrl);
            });
        } else {
            messageDiv.textContent = `Error: ${result.detail}`;
            messageDiv.style.color = 'red';
        }
    } catch (error) {
        const messageDiv = document.getElementById('response-message');
        messageDiv.textContent = 'An error occurred while creating OGP.';
        messageDiv.style.color = 'red';
    }
});

function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyMessage('URL copied to clipboard!', 'green');
        }).catch(() => {
            fallbackCopyText(text);
        });
    } else {
        fallbackCopyText(text);
    }
}

function fallbackCopyText(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    try {
        document.execCommand('copy');
        showCopyMessage('URL copied to clipboard!', 'green');
    } catch (err) {
        showCopyMessage('Failed to copy URL.', 'red');
    }
    document.body.removeChild(textarea);
}

function showCopyMessage(message, color) {
    const messageDiv = document.getElementById('response-message');
    const copyMessage = document.createElement('div');
    copyMessage.textContent = message;
    copyMessage.style.color = color;
    copyMessage.style.marginTop = '10px';
    copyMessage.style.fontSize = '0.9em';

    messageDiv.appendChild(copyMessage);

    setTimeout(() => {
        copyMessage.remove();
    }, 3000);
}