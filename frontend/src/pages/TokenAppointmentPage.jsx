import { useEffect, useState } from 'react'
import { Ticket, MapPin, PlusCircle } from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useCustomer } from '../context/CustomerContext.jsx'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState, EmptyState } from '../components/StateBox.jsx'

export default function TokenAppointmentPage() {
  const { customerId, customerName } = useCustomer()
  const { lang, t } = useLanguage()
  const [branches, setBranches] = useState([])
  const [services, setServices] = useState([])
  const [branchId, setBranchId] = useState('')
  const [serviceId, setServiceId] = useState('')
  const [tokens, setTokens] = useState([])
  const [loading, setLoading] = useState(true)
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([api.getBranches(), api.getBranchServices(lang)])
      .then(([b, s]) => {
        setBranches(b)
        setServices(s)
        setBranchId((prev) => prev || (b.length ? b[0].branch_id : ''))
        setServiceId((prev) => prev || (s.length ? s[0].service_id : ''))
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load branches.'))
  }, [lang])

  function loadTokens() {
    setLoading(true)
    api
      .getCustomerTokens(customerId)
      .then(setTokens)
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load your tokens.'))
      .finally(() => setLoading(false))
  }

  useEffect(loadTokens, [customerId])

  async function handleCreate(e) {
    e.preventDefault()
    if (!branchId || !serviceId) return
    setCreating(true)
    setError('')
    try {
      await api.createToken({ customer_id: customerId, customer_name: customerName || undefined, branch_id: branchId, service_id: serviceId, lang })
      loadTokens()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not create a token.')
    } finally {
      setCreating(false)
    }
  }

  return (
    <div className="grid grid-2" style={{ alignItems: 'start' }}>
      <div className="card">
        <div className="disclaimer-banner">{t('tk_disclaimer')}</div>
        <h3 style={{ marginBottom: 14 }}>{t('tk_request_token')}</h3>
        <form onSubmit={handleCreate}>
          <div className="field-group">
            <label>{t('tk_branch')}</label>
            <select className="select-input" value={branchId} onChange={(e) => setBranchId(e.target.value)}>
              {branches.map((b) => <option key={b.branch_id} value={b.branch_id}>{b.name} - {b.city}</option>)}
            </select>
          </div>
          <div className="field-group">
            <label>{t('tk_service')}</label>
            <select className="select-input" value={serviceId} onChange={(e) => setServiceId(e.target.value)}>
              {services.map((s) => <option key={s.service_id} value={s.service_id}>{s.service_name}</option>)}
            </select>
          </div>
          <button className="btn btn-primary btn-block" type="submit" disabled={creating}>
            <PlusCircle size={17} />
            {creating ? t('tk_requesting') : t('tk_request_btn')}
          </button>
        </form>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 14 }}>{t('tk_your_tokens')}</h3>
        {loading && <LoadingState message={t('tk_loading')} />}
        {!loading && error && <ErrorState message={error} onRetry={loadTokens} />}
        {!loading && !error && tokens.length === 0 && <EmptyState message={t('tk_empty')} icon={Ticket} />}
        {!loading && !error && tokens.map((tkn) => (
          <div key={tkn.token_id} className="card" style={{ marginBottom: 14, boxShadow: 'none', background: 'var(--color-primary-light)' }}>
            <div className="flex justify-between items-center">
              <div>
                <div style={{ fontSize: '1.6rem', fontWeight: 700, fontFamily: "'Baloo 2', sans-serif", color: 'var(--color-primary-dark)' }}>
                  {tkn.token_number}
                </div>
                <p className="muted small-text" style={{ margin: '4px 0 0' }}>
                  <MapPin size={12} style={{ verticalAlign: -1 }} /> {tkn.branch_name} &middot; {tkn.service_name}
                </p>
              </div>
              <span className="badge badge-info">{tkn.status}</span>
            </div>
            <p className="small-text muted" style={{ marginTop: 10 }}>{t('tk_queue_position')}: {tkn.position_in_queue}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
