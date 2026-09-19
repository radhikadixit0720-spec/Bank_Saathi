import { useEffect, useState, useCallback } from 'react'
import './App.css'

// Set VITE_API_URL in a .env file when you deploy the backend somewhere
// other than localhost. See the README for deployment instructions.
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function speak(text, rate = 1) {
  if (!('speechSynthesis' in window)) {
    alert('Is browser me awaaz (text-to-speech) support nahi hai.')
    return
  }
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = 'hi-IN'
  utterance.rate = rate
  const voices = window.speechSynthesis.getVoices()
  const hindiVoice = voices.find((v) => v.lang === 'hi-IN')
  if (hindiVoice) utterance.voice = hindiVoice
  window.speechSynthesis.speak(utterance)
}

export default function App() {
  const [fields, setFields] = useState([])
  const [stepIndex, setStepIndex] = useState(0)
  const [values, setValues] = useState({})
  const [explanation, setExplanation] = useState('')
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)
  const [slow, setSlow] = useState(false)
  const [stage, setStage] = useState('form') // 'form' | 'review' | 'done'
  const [missingFields, setMissingFields] = useState([])

  const currentField = fields[stepIndex]

  // Load the dummy form template from the backend on first render.
  useEffect(() => {
    fetch(`${API_URL}/form-template`)
      .then((res) => {
        if (!res.ok) throw new Error('Network response was not ok')
        return res.json()
      })
      .then((data) => {
        setFields(data)
        setLoading(false)
      })
      .catch(() => {
        setLoadError(true)
        setLoading(false)
      })
  }, [])

  // Fetch a fresh explanation whenever the current field changes.
  const loadExplanation = useCallback((fieldId) => {
    fetch(`${API_URL}/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ field_id: fieldId }),
    })
      .then((res) => res.json())
      .then((data) => setExplanation(data.explanation))
      .catch(() => setExplanation('Explanation load nahi ho payi. Internet check karein.'))
  }, [])

  useEffect(() => {
    if (currentField) loadExplanation(currentField.field_id)
  }, [currentField, loadExplanation])

  function handleChange(fieldId, value) {
    setValues((prev) => ({ ...prev, [fieldId]: value }))
  }

  function goNext() {
    if (stepIndex < fields.length - 1) {
      setStepIndex((i) => i + 1)
    } else {
      checkAndReview()
    }
  }

  function goPrev() {
    if (stepIndex > 0) setStepIndex((i) => i - 1)
  }

  function checkAndReview() {
    fetch(`${API_URL}/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ values }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMissingFields(data.missing_fields || [])
        setStage('review')
      })
      .catch(() => setStage('review'))
  }

  function goToField(fieldId) {
    const idx = fields.findIndex((f) => f.field_id === fieldId)
    if (idx >= 0) {
      setStepIndex(idx)
      setStage('form')
    }
  }

  if (loading) {
    return (
      <div className="screen center">
        <p className="muted">Bank Saathi load ho raha hai...</p>
      </div>
    )
  }

  if (loadError) {
    return (
      <div className="screen center">
        <p className="error-text">
          Backend se connect nahi ho paya. Kripya check karein ki API chal rahi hai
          (<code>{API_URL}</code>).
        </p>
      </div>
    )
  }

  return (
    <div className="screen">
      <header className="app-header">
        <div>
          <h1>Bank Saathi</h1>
          <p className="tagline">Form samjhiye, apni bhasha mein</p>
        </div>
        <span className="demo-badge">Demo only — final verification by bank staff required</span>
      </header>

      {stage === 'form' && currentField && (
        <FieldStep
          field={currentField}
          value={values[currentField.field_id] || ''}
          explanation={explanation}
          stepNumber={stepIndex + 1}
          totalSteps={fields.length}
          slow={slow}
          onSlowToggle={() => setSlow((s) => !s)}
          onChange={(v) => handleChange(currentField.field_id, v)}
          onSpeak={() => speak(explanation, slow ? 0.7 : 1)}
          onNext={goNext}
          onPrev={goPrev}
          isFirst={stepIndex === 0}
          isLast={stepIndex === fields.length - 1}
        />
      )}

      {stage === 'review' && (
        <ReviewStep
          fields={fields}
          values={values}
          missingFields={missingFields}
          onEditField={goToField}
          onConfirm={() => setStage('done')}
          onBack={() => setStage('form')}
        />
      )}

      {stage === 'done' && <DoneStep />}
    </div>
  )
}

function FieldStep({
  field,
  value,
  explanation,
  stepNumber,
  totalSteps,
  slow,
  onSlowToggle,
  onChange,
  onSpeak,
  onNext,
  onPrev,
  isFirst,
  isLast,
}) {
  return (
    <main className="card">
      <div className="progress-row">
        {Array.from({ length: totalSteps }).map((_, i) => (
          <span
            key={i}
            className={`dot ${i === stepNumber - 1 ? 'dot-active' : ''} ${
              i < stepNumber - 1 ? 'dot-done' : ''
            }`}
          />
        ))}
      </div>
      <p className="step-count">
        Field {stepNumber} of {totalSteps}
      </p>

      <h2 className="field-label">
        {field.label}
        {field.required && <span className="required-star"> *</span>}
      </h2>

      <div className="explanation-box">
        <p>{explanation || 'Loading...'}</p>
      </div>

      <div className="audio-row">
        <button className="btn btn-accent" onClick={onSpeak}>
          🔊 Sunao
        </button>
        <button className="btn btn-ghost" onClick={onSpeak}>
          🔁 Repeat
        </button>
        <label className="slow-toggle">
          <input type="checkbox" checked={slow} onChange={onSlowToggle} />
          Slow
        </label>
      </div>

      <label className="input-label" htmlFor={field.field_id}>
        Apna jawab yahan likhein
      </label>
      <input
        id={field.field_id}
        className="text-input"
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={field.required ? 'Zaroori (required)' : 'Optional'}
      />

      <div className="nav-row">
        <button className="btn btn-secondary" onClick={onPrev} disabled={isFirst}>
          ← Pichla
        </button>
        <button className="btn btn-primary" onClick={onNext}>
          {isLast ? 'Review karein →' : 'Aage →'}
        </button>
      </div>
    </main>
  )
}

function ReviewStep({ fields, values, missingFields, onEditField, onConfirm, onBack }) {
  const isComplete = missingFields.length === 0
  return (
    <main className="card">
      <h2 className="field-label">Apna form check karein</h2>
      <ul className="review-list">
        {fields.map((f) => {
          const val = values[f.field_id]
          const isMissing = missingFields.includes(f.field_id)
          return (
            <li key={f.field_id} className={isMissing ? 'review-item missing' : 'review-item'}>
              <div>
                <strong>{f.label}</strong>
                <div className="review-value">{val ? val : isMissing ? 'Khaali hai!' : '—'}</div>
              </div>
              <button className="btn btn-ghost small" onClick={() => onEditField(f.field_id)}>
                Edit
              </button>
            </li>
          )
        })}
      </ul>

      {!isComplete && (
        <p className="error-text">
          Kuch zaroori fields khaali hain. Kripya unhe bharein cursor par "Edit" dabakar.
        </p>
      )}

      <div className="nav-row">
        <button className="btn btn-secondary" onClick={onBack}>
          ← Wapas
        </button>
        <button className="btn btn-primary" onClick={onConfirm} disabled={!isComplete}>
          Confirm karein →
        </button>
      </div>
    </main>
  )
}

function DoneStep() {
  return (
    <main className="card center-text">
      <div className="success-icon">✅</div>
      <h2 className="field-label">Form ready for bank verification</h2>
      <p className="muted">
        Aapne form samajh liya hai. Ab ise bank staff ko dikhaiye final verification ke liye.
        Bank Saathi ne koi data bank ko submit nahi kiya hai — ye sirf ek samjhane wala tool hai.
      </p>
    </main>
  )
}
