import { createContext, useContext, useEffect, useState } from 'react'
import { TRANSLATIONS } from '../i18n/translations.js'

const LanguageContext = createContext(null)

export const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिंदी' },
  { code: 'hinglish', label: 'Hinglish' },
]

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => localStorage.getItem('bs_lang') || 'en')

  useEffect(() => {
    localStorage.setItem('bs_lang', lang)
  }, [lang])

  function t(key) {
    const entry = TRANSLATIONS[key]
    if (!entry) return key
    return entry[lang] || entry.en || key
  }

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const ctx = useContext(LanguageContext)
  if (!ctx) throw new Error('useLanguage must be used within LanguageProvider')
  return ctx
}
