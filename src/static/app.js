const form = document.getElementById('lead-form');
if (form) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = document.getElementById('form-status');
    status.className = '';
    if (!form.reportValidity()) {
      status.textContent = 'Check the highlighted fields and try again.';
      status.className = 'error';
      return;
    }
    const fields = new FormData(form);
    const payload = {
      name: fields.get('name'), email: fields.get('email'),
      service: fields.get('service'), message: fields.get('message'),
      website: fields.get('website'), consent: fields.get('consent') === 'on'
    };
    const button = form.querySelector('button[type=submit]');
    button.disabled = true;
    status.textContent = 'Submitting demo request…';
    try {
      const response = await fetch('/api/leads', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      if (response.ok) {
        form.reset();
        status.className = 'success';
        status.textContent = 'Demo request saved locally. No message or email was sent.';
      } else if (response.status === 429) {
        status.className = 'error';
        status.textContent = 'Too many demo submissions. Try again later.';
      } else if (response.status === 422) {
        status.className = 'error';
        status.textContent = 'The server rejected some fields. Review your input.';
      } else {
        status.className = 'error';
        status.textContent = 'Local demo unavailable. Nothing was confirmed saved.';
      }
    } catch (_) {
      status.className = 'error';
      status.textContent = 'Network error. Request was not confirmed. Please retry carefully.';
    } finally { button.disabled = false; }
  });
}
