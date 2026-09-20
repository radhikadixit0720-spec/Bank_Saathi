import { useState } from 'react'
import { ShieldAlert, ShieldCheck, XCircle } from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useCustomer } from '../context/CustomerContext.jsx'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState } from '../components/StateBox.jsx'

export default function ErrorCheckerPage() {
  const { customerId } = useCustomer()
  const { lang, t } = useLanguage()
  const FIELDS = [
    { id: 'account_number', label: t('field_account_number'), required: true },
    { id: 'mobile_number', label: t('field_mobile_number'), required: true },
    { id: 'email', label: t('field_email'), required: false },
    { id: 'pan_number', label: t('field_pan_number'), required: false },
    { id: 'date_of_birth', label: t('field_dob'), required: true },
  ]
  const [values, setValues] = useState({})
  const [consent, setConsent] = useState(false)
  const [signature, setSignature] = useState(false)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  function setValue(id, val) {
    setValues((prev) => ({ ...prev, [id]: val }))
  }

  async function handleCheck(e) {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await api.checkForm({
        values,
        consent_given: consent,
        signature_present: signature,
        required_fields: FIELDS.filter((f) => f.required).map((f) => f.id),
        customer_id: customerId,
        request_type: 'general_check',
        lang,
      })
      setResult(data)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not run the error check.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-2" style={{ alignItems: 'start' }}>
      <div className="card">
        <h3 style={{ marginBottom: 14 }}>{t('ec_enter_values')}</h3>
        <form onSubmit={handleCheck}>
          {FIELDS.map((f) => (
            <div className="field-group" key={f.id}>
              <label>{f.label}{f.required && ' *'}</label>
              <input
                className="text-input"
                value={values[f.id] || ''}
                onChange={(e) => setValue(f.id, e.target.value)}
              />
            </div>
          ))}
          <label className="flex items-center gap-8 small-text muted" style={{ marginBottom: 10 }}>
            <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
            {t('ec_consent')}
          </label>
          <label className="flex items-center gap-8 small-text muted" style={{ marginBottom: 18 }}>
            <input type="checkbox" checked={signature} onChange={(e) => setSignature(e.target.checked)} />
            {t('ec_signature')}
          </label>
          <button className="btn btn-primary btn-block" type="submit" disabled={loading}>
            <ShieldAlert size={17} />
            {loading ? t('ec_checking') : t('ec_check_btn')}
          </button>
        </form>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 14 }}>{t('ec_results_title')}</h3>
        {loading && <LoadingState message={t('ec_checking')} />}
        {!loading && error && <ErrorState message={error} />}
        {!loading && !error && !result && (
          <div className="state-box">
            <ShieldCheck size={26} />
            <p>{t('ec_results_empty')}</p>
          </div>
        )}
        {!loading && result && (
          <div>
            {result.is_valid ? (
              <div className="field-row" style={{ borderLeft: '4px solid var(--color-teal)' }}>
                <div className="field-row-label">{t('ec_no_errors')}</div>
                <ShieldCheck size={20} color="#0d9488" />
              </div>
            ) : (
              result.errors.map((err, idx) => (
                <div key={idx} className="field-row missing" style={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                  <div className="flex items-center gap-8">
                    <XCircle size={16} color="#dc2626" />
                    <span className="field-row-label">{err.field.replaceAll('_', ' ')}</span>
                  </div>
                  <p className="field-row-message" style={{ marginLeft: 24 }}>{err.message}</p>
                  <p className="small-text" style={{ marginLeft: 24, color: 'var(--color-primary-dark)' }}>{err.suggestion}</p>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
}
