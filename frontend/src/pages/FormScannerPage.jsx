import { useEffect, useState } from 'react'
import { UploadCloud, ScanLine, CheckCircle2, XCircle, AlertTriangle, FileText } from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState } from '../components/StateBox.jsx'

const STATUS_ICON = {
  matched: <CheckCircle2 size={18} color="#0d9488" />,
  missing: <XCircle size={18} color="#dc2626" />,
  needs_attention: <AlertTriangle size={18} color="#d97706" />,
}

export default function FormScannerPage() {
  const { lang, t } = useLanguage()
  const [templates, setTemplates] = useState([])
  const [templateId, setTemplateId] = useState('')
  const [file, setFile] = useState(null)
  const [scanning, setScanning] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loadingTemplates, setLoadingTemplates] = useState(true)

  useEffect(() => {
    setLoadingTemplates(true)
    api
      .getFormTemplates(lang)
      .then((data) => {
        setTemplates(data)
        if (data.length) setTemplateId((prev) => prev || data[0].template_id)
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : 'Could not load templates.'))
      .finally(() => setLoadingTemplates(false))
  }, [lang])

  async function handleScan(e) {
    e.preventDefault()
    if (!templateId || !file) return
    setScanning(true)
    setError('')
    setResult(null)
    try {
      const data = await api.scanUploadedForm(templateId, file, lang)
      setResult(data)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not scan this form.')
    } finally {
      setScanning(false)
    }
  }

  if (loadingTemplates) return <LoadingState message={t('loading')} />

  return (
    <div>
      <div className="grid grid-2" style={{ alignItems: 'start' }}>
        <div className="card">
          <h3 style={{ marginBottom: 14 }}>{t('fs_step1')}</h3>
          <div className="field-group">
            <label>{t('fs_template_label')}</label>
            <select className="select-input" value={templateId} onChange={(e) => setTemplateId(e.target.value)}>
              {templates.map((tpl) => (
                <option key={tpl.template_id} value={tpl.template_id}>
                  {tpl.name} ({tpl.field_count})
                </option>
              ))}
            </select>
          </div>

          <h3 style={{ margin: '22px 0 14px' }}>{t('fs_step2')}</h3>
          <form onSubmit={handleScan}>
            <label
              htmlFor="form-upload"
              className="field-group"
              style={{
                display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8,
                border: '2px dashed var(--color-border)', borderRadius: 14, padding: '28px 16px',
                cursor: 'pointer', background: 'var(--color-primary-light)',
              }}
            >
              <UploadCloud size={26} color="#3b4fe0" />
              <span className="small-text muted">{file ? file.name : t('fs_upload_hint')}</span>
              <input
                id="form-upload"
                type="file"
                accept=".pdf,.txt,image/*"
                style={{ display: 'none' }}
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
            </label>
            <button className="btn btn-primary btn-block" type="submit" disabled={!file || scanning}>
              <ScanLine size={17} />
              {scanning ? t('fs_scanning') : t('fs_scan_btn')}
            </button>
          </form>
          <p className="muted small-text" style={{ marginTop: 12 }}>{t('fs_disclaimer')}</p>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: 14 }}>{t('fs_result_title')}</h3>
          {scanning && <LoadingState message={t('fs_analyzing')} />}
          {!scanning && error && <ErrorState message={error} />}
          {!scanning && !error && !result && (
            <div className="state-box">
              <FileText size={26} />
              <p>{t('fs_result_empty')}</p>
            </div>
          )}
          {!scanning && result && (
            <div>
              {!result.ocr_used && result.fallback_reason && (
                <div className="disclaimer-banner">{result.fallback_reason}</div>
              )}
              <div className="flex gap-8" style={{ marginBottom: 16 }}>
                <span className="badge badge-success">{result.matched_count} {t('fs_matched')}</span>
                <span className="badge badge-danger">{result.missing_count} {t('fs_missing')}</span>
                <span className="badge badge-warning">{result.needs_attention_count} {t('fs_needs_attention')}</span>
              </div>
              {result.fields.map((f) => (
                <div key={f.field_id} className={`field-row ${f.status}`}>
                  <div>
                    <div className="field-row-label">{f.label}{f.required && ' *'}</div>
                    <div className="field-row-message">{f.message}</div>
                  </div>
                  {STATUS_ICON[f.status]}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
