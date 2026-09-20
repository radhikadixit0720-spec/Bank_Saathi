import { useEffect, useState } from 'react'
import { ClipboardCheck, Circle, CheckCircle2, MinusCircle } from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useCustomer } from '../context/CustomerContext.jsx'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState } from '../components/StateBox.jsx'

const STATUS_CYCLE = ['missing', 'available', 'not_applicable']
const STATUS_META = {
  missing: { icon: Circle, label: 'Missing', color: '#dc2626' },
  available: { icon: CheckCircle2, label: 'Available', color: '#0d9488' },
  not_applicable: { icon: MinusCircle, label: 'Not applicable', color: '#9aa0c9' },
}

export default function ChecklistPage() {
  const { customerId } = useCustomer()
  const { lang, t } = useLanguage()
  const [services, setServices] = useState([])
  const [serviceId, setServiceId] = useState('')
  const [checklist, setChecklist] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    api
      .getChecklistServices(lang)
      .then((data) => {
        setServices(data)
        if (data.length) setServiceId((prev) => prev || data[0].service_id)
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load services.'))
  }, [lang])

  useEffect(() => {
    if (!serviceId) return
    setLoading(true)
    setError('')
    api
      .getChecklist(serviceId, customerId, lang)
      .then(setChecklist)
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load checklist.'))
      .finally(() => setLoading(false))
  }, [serviceId, customerId, lang])

  async function cycleStatus(docId, currentStatus) {
    const nextStatus = STATUS_CYCLE[(STATUS_CYCLE.indexOf(currentStatus) + 1) % STATUS_CYCLE.length]
    setSaving(true)
    try {
      const updated = await api.updateChecklistStatus(serviceId, customerId, { [docId]: nextStatus }, lang)
      setChecklist(updated)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not update this document.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="field-group" style={{ marginBottom: 0, maxWidth: 360 }}>
          <label>{t('cl_select_service')}</label>
          <select className="select-input" value={serviceId} onChange={(e) => setServiceId(e.target.value)}>
            {services.map((s) => (
              <option key={s.service_id} value={s.service_id}>{s.service_name}</option>
            ))}
          </select>
        </div>
      </div>

      {loading && <LoadingState message={t('cl_loading')} />}
      {!loading && error && <ErrorState message={error} />}

      {!loading && !error && checklist && (
        <div className="card">
          <div className="flex justify-between items-center" style={{ marginBottom: 16 }}>
            <h3 style={{ margin: 0 }}>{checklist.service_name}</h3>
            <span className={`badge ${checklist.remaining_required === 0 ? 'badge-success' : 'badge-warning'}`}>
              <ClipboardCheck size={13} /> {checklist.summary}
            </span>
          </div>

          {checklist.documents.map((doc) => {
            const meta = STATUS_META[doc.status]
            const Icon = meta.icon
            const nextLabel = STATUS_CYCLE.filter((s) => s !== doc.status)[0].replaceAll('_', ' ')
            return (
              <button
                key={doc.doc_id}
                className="field-row"
                style={{ width: '100%', cursor: 'pointer', border: '1px solid var(--color-border)', textAlign: 'left' }}
                onClick={() => cycleStatus(doc.doc_id, doc.status)}
                disabled={saving}
              >
                <div className="flex items-center gap-12">
                  <Icon size={20} color={meta.color} />
                  <div>
                    <div className="field-row-label">{doc.label}{doc.required && ' *'}</div>
                    <div className="field-row-message">{t('cl_tap_to_mark')} {nextLabel}</div>
                  </div>
                </div>
                <span className={`badge ${doc.status === 'available' ? 'badge-success' : doc.status === 'missing' ? 'badge-danger' : 'badge-neutral'}`}>
                  {meta.label}
                </span>
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}
