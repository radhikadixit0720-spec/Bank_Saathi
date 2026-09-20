import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  ScanLine, Languages, ClipboardList, ShieldAlert, Receipt, Ticket,
  Clock3, CheckCircle2, FileWarning, CalendarClock, ArrowRight,
} from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useCustomer } from '../context/CustomerContext.jsx'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState } from '../components/StateBox.jsx'

export default function CustomerDashboard() {
  const { customerId, customerName } = useCustomer()
  const { t } = useLanguage()
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const QUICK_ACTIONS = [
    { to: '/form-scanner', label: t('nav_form_scanner'), desc: t('qa_form_scanner_desc'), icon: ScanLine, color: '#3b4fe0' },
    { to: '/language-assistant', label: t('nav_language_assistant'), desc: t('qa_language_desc'), icon: Languages, color: '#0d9488' },
    { to: '/checklist', label: t('nav_checklist'), desc: t('qa_checklist_desc'), icon: ClipboardList, color: '#d97706' },
    { to: '/error-checker', label: t('nav_error_checker'), desc: t('qa_error_desc'), icon: ShieldAlert, color: '#dc2626' },
    { to: '/status-vault', label: t('nav_status_vault'), desc: t('qa_status_desc'), icon: Receipt, color: '#4f46e5' },
    { to: '/appointment', label: t('nav_appointment'), desc: t('qa_token_desc'), icon: Ticket, color: '#0891b2' },
  ]

  const load = () => {
    setLoading(true)
    setError('')
    api
      .getCustomerSummary(customerId)
      .then(setSummary)
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load your dashboard.'))
      .finally(() => setLoading(false))
  }

  useEffect(load, [customerId])

  return (
    <div>
      <div className="hero-banner">
        <h1>{t('hero_greeting')}{customerName ? `, ${customerName}` : ''} 👋</h1>
        <p>{t('hero_desc')}</p>
      </div>

      {loading && <LoadingState message={t('loading')} />}
      {!loading && error && <ErrorState message={error} onRetry={load} />}

      {!loading && !error && summary && (
        <div className="grid grid-4" style={{ marginBottom: 28 }}>
          <SummaryTile icon={Clock3} color="#3b4fe0" bg="#eef0fd" label={t('pending_requests')} value={summary.pending_requests} />
          <SummaryTile icon={CheckCircle2} color="#0d9488" bg="#e6f7f5" label={t('completed_requests')} value={summary.completed_requests} />
          <SummaryTile icon={FileWarning} color="#d97706" bg="#fef3e2" label={t('total_requests')} value={summary.total_requests} />
          <SummaryTile
            icon={CalendarClock}
            color="#4f46e5"
            bg="#eef0fd"
            label={t('upcoming_token')}
            value={summary.upcoming_appointment ? summary.upcoming_appointment.token_number : '—'}
          />
        </div>
      )}

      <h3 className="section-title">{t('quick_actions')}</h3>
      <div className="grid grid-3">
        {QUICK_ACTIONS.map((action) => (
          <Link to={action.to} key={action.to} className="card hoverable" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="card-header">
              <div className="card-icon" style={{ background: `${action.color}18` }}>
                <action.icon size={22} color={action.color} />
              </div>
              <ArrowRight size={18} color="#9aa0c9" />
            </div>
            <h4 style={{ marginBottom: 4 }}>{action.label}</h4>
            <p className="muted small-text" style={{ margin: 0 }}>{action.desc}</p>
          </Link>
        ))}
      </div>

      {!loading && !error && summary && summary.recent_requests?.length > 0 && (
        <>
          <h3 className="section-title">{t('recent_requests')}</h3>
          <div className="card">
            {summary.recent_requests.map((r) => (
              <div key={r.request_id} className="flex justify-between items-center" style={{ padding: '10px 0', borderBottom: '1px solid var(--color-border)' }}>
                <div>
                  <strong style={{ fontSize: '0.92rem' }}>{r.request_type.replaceAll('_', ' ')}</strong>
                  <p className="muted small-text" style={{ margin: '2px 0 0' }}>{r.request_id}</p>
                </div>
                <span className="badge badge-info">{r.status.replaceAll('_', ' ')}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function SummaryTile({ icon: Icon, color, bg, label, value }) {
  return (
    <div className="card summary-card">
      <div className="card-icon" style={{ background: bg }}>
        <Icon size={20} color={color} />
      </div>
      <div>
        <div className="summary-value">{value}</div>
        <div className="summary-label">{label}</div>
      </div>
    </div>
  )
}
