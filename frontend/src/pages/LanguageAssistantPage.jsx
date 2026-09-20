import { useState } from 'react'
import { Languages, Sparkles } from 'lucide-react'
import { api, ApiError } from '../api/client.js'
import { useLanguage } from '../context/LanguageContext.jsx'
import { LoadingState, ErrorState } from '../components/StateBox.jsx'

const EXAMPLES = [
  'Please furnish proof of residential address.',
  'The undersigned hereby declares that the aforementioned details are true.',
  'Kindly furnish duly filled KYC documents prior to account activation.',
]

export default function LanguageAssistantPage() {
  const { lang, t } = useLanguage()
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    if (!text.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const data = await api.simplifyText(text.trim(), lang)
      setResult(data)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not simplify this text.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-2" style={{ alignItems: 'start' }}>
      <div className="card">
        <h3 style={{ marginBottom: 14 }}>{t('la_paste_label')}</h3>
        <form onSubmit={handleSubmit}>
          <div className="field-group">
            <textarea
              className="text-input"
              rows={6}
              placeholder={t('la_placeholder')}
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
          </div>
          <button className="btn btn-primary btn-block" type="submit" disabled={loading || !text.trim()}>
            <Languages size={17} />
            {loading ? t('la_simplifying') : t('la_submit_btn')}
          </button>
        </form>

        <h4 className="small-text muted" style={{ marginTop: 20, marginBottom: 8 }}>{t('la_try_example')}</h4>
        <div className="flex flex-col gap-8">
          {EXAMPLES.map((ex) => (
            <button key={ex} className="btn btn-ghost small" style={{ justifyContent: 'flex-start', textAlign: 'left' }} onClick={() => setText(ex)}>
              {ex}
            </button>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 14 }}>{t('la_result_title')}</h3>
        {loading && <LoadingState message={t('la_working')} />}
        {!loading && error && <ErrorState message={error} />}
        {!loading && !error && !result && (
          <div className="state-box">
            <Sparkles size={26} />
            <p>{t('la_result_empty')}</p>
          </div>
        )}
        {!loading && result && (
          <div>
            <div className="badge badge-info" style={{ marginBottom: 14 }}>
              {result.method === 'ai_provider' ? t('la_ai_generated') : t('la_rule_based')}
            </div>
            <div className="field-row" style={{ borderLeft: '4px solid var(--color-teal)', flexDirection: 'column', alignItems: 'flex-start' }}>
              <p style={{ margin: 0, lineHeight: 1.6 }}>{result.simple_explanation}</p>
            </div>
            {result.note && <p className="muted small-text" style={{ marginTop: 10 }}>{result.note}</p>}
          </div>
        )}
      </div>
    </div>
  )
}
