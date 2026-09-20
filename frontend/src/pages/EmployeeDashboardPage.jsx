import { useEffect, useState } from 'react'
import { Users, Clock3, CheckCircle2, FileWarning, AlertTriangle } from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState, EmptyState } from '../components/StateBox.jsx'

export default function EmployeeDashboardPage() {
  const { t } = useLanguage()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  function load() {
    setLoading(true)
    setError('')
    api
      .getEmployeeDashboard()
      .then(setData)
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load the dashboard.'))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  if (loading) return <LoadingState message={t('loading')} />
  if (error) return <ErrorState message={error} onRetry={load} />
  if (!data) return null

  return (
    <div>
      <div className="grid grid-3" style={{ marginBottom: 24 }}>
        <SummaryTile icon={Users} color="#3b4fe0" bg="#eef0fd" label={t('emp_total')} value={data.total_requests} />
        <SummaryTile icon={Clock3} color="#d97706" bg="#fef3e2" label={t('emp_pending')} value={data.pending_count} />
        <SummaryTile icon={CheckCircle2} color="#0d9488" bg="#e6f7f5" label={t('emp_completed')} value={data.completed_count} />
      </div>

      {data.requests.length === 0 ? (
        <EmptyState message={t('emp_empty')} icon={Users} />
      ) : (
        <div className="grid grid-2">
          {data.requests.map((r) => (
            <div className="card" key={r.request_id}>
              <div className="flex justify-between items-center" style={{ marginBottom: 10 }}>
                <div>
                  <strong>{r.customer_name || r.customer_id}</strong>
                  <p className="muted small-text" style={{ margin: '2px 0 0', textTransform: 'capitalize' }}>
                    {r.request_type.replaceAll('_', ' ')} &middot; {r.request_id}
                  </p>
                </div>
                <span className="badge badge-info">{r.status.replaceAll('_', ' ')}</span>
              </div>

              {r.missing_documents.length > 0 && (
                <div style={{ marginBottom: 10 }}>
                  <p className="small-text" style={{ fontWeight: 600, marginBottom: 4, color: 'var(--color-red)' }}>
                    <FileWarning size={13} style={{ verticalAlign: -2 }} /> Missing documents
                  </p>
                  <ul style={{ margin: 0, paddingLeft: 18 }}>
                    {r.missing_documents.map((doc) => (
                      <li key={doc} className="small-text muted">{doc}</li>
                    ))}
                  </ul>
                </div>
              )}

              {r.error_alerts.length > 0 && (
                <div>
                  <p className="small-text" style={{ fontWeight: 600, marginBottom: 4, color: 'var(--color-amber)' }}>
                    <AlertTriangle size={13} style={{ verticalAlign: -2 }} /> Validation alerts
                  </p>
                  <ul style={{ margin: 0, paddingLeft: 18 }}>
                    {r.error_alerts.map((msg, idx) => (
                      <li key={idx} className="small-text muted">{msg}</li>
                    ))}
                  </ul>
                </div>
              )}

              {r.missing_documents.length === 0 && r.error_alerts.length === 0 && (
                <p className="small-text" style={{ color: 'var(--color-teal)' }}>
                  <CheckCircle2 size={13} style={{ verticalAlign: -2 }} /> Nothing outstanding for this request.
                </p>
              )}
            </div>
          ))}
        </div>
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
