// Centralized API client. Every backend call in the app goes through here
// so there is exactly one place that knows the backend base URL and how
// to translate network/HTTP failures into friendly errors.

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function handleResponse(res) {
  let body = null
  try {
    body = await res.json()
  } catch {
    // no JSON body (e.g. empty 204) - that's fine
  }

  if (!res.ok) {
    const message =
      (body && (body.detail || body.message)) ||
      `Request failed with status ${res.status}.`
    throw new ApiError(
      typeof message === 'string' ? message : 'Something went wrong. Please try again.',
      res.status
    )
  }
  return body
}

async function request(path, options = {}) {
  let res
  try {
    res = await fetch(`${API_URL}${path}`, {
      headers: options.body instanceof FormData ? undefined : { 'Content-Type': 'application/json' },
      ...options,
    })
  } catch (err) {
    throw new ApiError(
      'Could not reach the Bank Saathi server. Please check your internet connection and try again.',
      0
    )
  }
  return handleResponse(res)
}

const get = (path) => request(path, { method: 'GET' })
const post = (path, body) =>
  request(path, { method: 'POST', body: body instanceof FormData ? body : JSON.stringify(body) })
const patch = (path, body) => request(path, { method: 'PATCH', body: JSON.stringify(body) })

export const api = {
  // Form Scanner
  getFormTemplates: (lang = 'en') => get(`/api/form-scanner/templates?lang=${lang}`),
  scanUploadedForm: (templateId, file, lang = 'en') => {
    const formData = new FormData()
    formData.append('template_id', templateId)
    formData.append('file', file)
    formData.append('lang', lang)
    return post('/api/form-scanner/scan', formData)
  },
  scanManualValues: (templateId, values, lang = 'en') =>
    post('/api/form-scanner/scan-manual', { template_id: templateId, values, lang }),

  // Simple Language Assistant
  simplifyText: (text, lang = 'en') => post('/api/language-assistant/simplify', { text, lang }),

  // Document Checklist
  getChecklistServices: (lang = 'en') => get(`/api/checklist/services?lang=${lang}`),
  getChecklist: (serviceId, customerId, lang = 'en') =>
    get(`/api/checklist/${serviceId}?customer_id=${encodeURIComponent(customerId)}&lang=${lang}`),
  updateChecklistStatus: (serviceId, customerId, statuses, lang = 'en') =>
    post(`/api/checklist/${serviceId}/status?lang=${lang}`, { customer_id: customerId, statuses }),

  // Error Checker
  checkForm: (payload) => post('/api/error-checker/check', payload),

  // Requests / Status vault
  createRequest: (payload) => post('/api/requests', payload),
  getCustomerRequests: (customerId) => get(`/api/requests/customer/${encodeURIComponent(customerId)}`),
  updateRequestStatus: (requestId, status, notes) =>
    patch(`/api/requests/${requestId}/status`, { status, notes }),

  // Branch Token / Appointment
  getBranches: () => get('/api/tokens/branches'),
  getBranchServices: (lang = 'en') => get(`/api/tokens/services?lang=${lang}`),
  createToken: (payload) => post('/api/tokens', payload),
  getCustomerTokens: (customerId) => get(`/api/tokens/customer/${encodeURIComponent(customerId)}`),

  // Employee dashboard
  getEmployeeDashboard: () => get('/api/employee/dashboard'),

  // Customer dashboard summary
  getCustomerSummary: (customerId) => get(`/api/customer/${encodeURIComponent(customerId)}/summary`),
}
