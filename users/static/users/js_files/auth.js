// auth.js

function $(sel, root = document) { return root.querySelector(sel); }
function $all(sel, root = document) { return Array.from(root.querySelectorAll(sel)); }

function setFieldError(inputEl, msg) {
  const field = inputEl.closest('.input');
  const err = field.querySelector('.field-error');
  field.classList.add('invalid');
  if (err) err.textContent = msg;
}

function clearFieldError(inputEl) {
  const field = inputEl.closest('.input');
  const err = field.querySelector('.field-error');
  field.classList.remove('invalid');
  if (err) err.textContent = '';
}

function clearAllErrors(form) {
  $all('.input', form).forEach(f => f.classList.remove('invalid'));
  const alert = $('.form-alert', form);
  if (alert) { alert.className = 'form-alert'; alert.textContent = ''; }
}

function showFormAlert(form, msg, type = 'error') {
  const alert = $('.form-alert', form);
  if (!alert) return;
  alert.textContent = msg;
  alert.classList.add('show', type);
}

function bindPasswordToggles(root = document) {
  $all('.toggle[data-target]', root).forEach(btn => {
    btn.addEventListener('click', () => {
      const target = $(btn.dataset.target);
      if (!target) return;
      const type = target.getAttribute('type') === 'password' ? 'text' : 'password';
      target.setAttribute('type', type);
      btn.setAttribute('aria-pressed', type === 'text');
      btn.textContent = type === 'text' ? 'Hide' : 'Show';
      target.focus();
    });
  });
}

async function postJSON(url, payload) {
  const headers = { 'Content-Type': 'application/json' };
  // const csrf = document.querySelector('meta[name="csrf-token"]')?.content;
  // if (csrf) headers['X-CSRF-Token'] = csrf;
  const res = await fetch(url, {
    method: 'POST',
    headers,
    credentials: 'include', // allows server to set HttpOnly cookies
    body: JSON.stringify(payload)
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const message = data?.message || data?.error || `Request failed (${res.status})`;
    const fieldErrors = data?.errors || null; // { email: "...", password: "..." }
    const err = new Error(message);
    err.fieldErrors = fieldErrors;
    err.status = res.status;
    throw err;
  }
  return data;
}

function bindForm(formId, { endpoint, onSuccessRedirect }) {
  const form = document.getElementById(formId);
  if (!form) return;
  const submitBtn = $('button[type="submit"]', form);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    clearAllErrors(form);

    // Use native constraint validation first
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // Gather data
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    // Optional: normalize
    if (payload.username) payload.username = String(payload.username).trim();

    submitBtn.disabled = true;
    submitBtn.dataset.originalText = submitBtn.textContent;
    submitBtn.textContent = 'Please wait…';

    try {
      await postJSON(endpoint, payload);
      showFormAlert(form, 'Success! Redirecting…', 'success');
      if (onSuccessRedirect) {
        window.location.assign(onSuccessRedirect);
      }
    } catch (err) {
      if (err.fieldErrors && typeof err.fieldErrors === 'object') {
        for (const [name, message] of Object.entries(err.fieldErrors)) {
          const inputEl = form.elements.namedItem(name);
          if (inputEl) setFieldError(inputEl, message || 'Invalid value');
        }
      }
      showFormAlert(form, err.message || 'Something went wrong. Please try again.');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = submitBtn.dataset.originalText || 'Submit';
    }
  });

  // Clear a field's error on input
  $all('input', form).forEach(input => {
    input.addEventListener('input', () => clearFieldError(input));
  });
}

document.addEventListener('DOMContentLoaded', () => {
  bindPasswordToggles();
});
