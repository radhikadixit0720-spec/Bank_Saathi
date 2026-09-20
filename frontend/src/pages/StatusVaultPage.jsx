import { useEffect, useState } from 'react'
import { Receipt, PlusCircle, CheckCircle2, Clock3, FileWarning } from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useCustomer } from '../context/CustomerContext.jsx'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState, EmptyState } from '../components/StateBox.jsx'

const REQUEST_TYPES = [
  { id: 'account_opening', label: 'Account Opening' },
  { id: 'kyc_update', label: 'KYC Update' },
  { id: 'address_change', label: 'Address Change' },
  { id: 'pan_update', label: 'PAN Update' },
  { id: 'loan_enquiry', label: 'Loan Enquiry' },
  { id: 'cheque_request', label: 'Cheque Request' },
  { id: 'atm_card_request', label: 'ATM/Debit Card Request' },
]

const STEPS = ['submitted', 'pending', 'completed']
const STEP_ICON = { submitted: Clock3, pending: Clock3, completed: CheckCircle2, action_required: FileWarning, rejected: FileWarning }

export default function StatusVaultPage() {
  const { customerId, customerName } = useCustomer()
  const { t } = useLanguage()
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [requestType, setRequestType] = useState(REQUEST_TYPES[0].id)
  const [notes, setNotes] = useState('')
  const [creating, setCreating] = useState(false)

  function load() {
    setLoading(true)
    setError('')
    api
      .getCustomerRequests(customerId)
      .then(setRequests)
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load your requests.'))
      .finally(() => setLoading(false))
  }

  useEffect(load, [customerId])

  async function handleCreate(e) {
    e.preventDefault()
    setCreating(true)
    try {
      await api.createRequest({ customer_id: customerId, customer_name: customerName || undefined, request_type: requestType, notes: notes || undefined })
      setNotes('')
      load()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create the request.')
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="grid grid-2" style={{ alignItems: 'start' }}>
      <div className="card">
        <h3 style={{ marginBottom: 14 }}>{t('sv_submit_new')}</h3>
        <form onSubmit={handleCreate}>
          <div className="field-group">
            <label>{t('sv_request_type')}</label>
            <select className="select-input" value={requestType} onChange={(e) => setRequestType(e.target.value)}>
              {REQUEST_TYPES.map((tp) => <option key={tp.id} value={tp.id}>{tp.label}</option>)}
            </select>
          </div>
          <div className="field-group">
            <label>{t('sv_notes_optional')}</label>
            <textarea className="text-input" rows={3} value={notes} onChange={(e) => setNotes(e.target.value)} />
          </div>
          <button className="btn btn-primary btn-block" type="submit" disabled={creating}>
            <PlusCircle size={17} />
            {creating ? t('sv_submitting') : t('sv_submit_btn')}
          </button>
        </form>
        <p className="muted small-text" style={{ marginTop: 12 }}>{t('sv_note')}</p>
      </div>

      <div className="card">
        <div className="flex justify-between items-center" style={{ marginBottom: 14 }}>
          <h3 style={{ margin: 0 }}>{t('sv_your_requests')}</h3>
          <Receipt size={18} color="#4f46e5" />
        </div>
        {loading && <LoadingState message={t('sv_loading')} />}
        {!loading && error && <ErrorState message={error} onRetry={load} />}
        {!loading && !error && requests.length === 0 && <EmptyState message={t('sv_empty')} icon={Receipt} />}
        {!loading && !error && requests.map((r) => (
          <div key={r.request_id} className="card" style={{ marginBottom: 14, boxShadow: 'none' }}>
            <div className="flex justify-between items-center" style={{ marginBottom: 10 }}>
              <div>
                <strong style={{ textTransform: 'capitalize' }}>{r.request_type.replaceAll('_', ' ')}</strong>
                <p className="muted small-text" style={{ margin: '2px 0 0' }}>
                  {r.request_id} &middot; Receipt {r.receipt_number}
                </p>
              </div>
              <span className="badge badge-info">{r.status.replaceAll('_', ' ')}</span>
            </div>
            <Timeline status={r.status} />
          </div>
        ))}
      </div>
    </div>
  )
}

function Timeline({ status }) {
  const activeIndex = STEPS.indexOf(status)
  const isSpecial = activeIndex === -1 // rejected / action_required
  return (
    <div className="timeline">
      {STEPS.map((step, idx) => {
        const Icon = STEP_ICON[step]
        const done = !isSpecial && idx <= activeIndex
        return (
          <div className="timeline-step" key={step}>
            <div className="timeline-marker-col">
              <div className="timeline-dot" style={{ background: done ? '#e6f7f5' : '#eef0f5', color: done ? '#0d9488' : '#9aa0c9' }}>
                <Icon size={14} />
              </div>
              {idx < STEPS.length - 1 && <div className="timeline-line" />}
            </div>
            <div className="timeline-content">
              <h4 style={{ textTransform: 'capitalize', color: done ? 'var(--color-text)' : 'var(--color-muted)' }}>{step}</h4>
            </div>
          </div>
        )
      })}
      {isSpecial && (
        <div className="badge badge-warning" style={{ marginTop: -6 }}>
          <FileWarning size={13} /> {status.replaceAll('_', ' ')}
        </div>
      )}
    </div>
  )
}
