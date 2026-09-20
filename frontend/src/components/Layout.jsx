import { useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  ScanLine,
  Languages,
  ClipboardList,
  ShieldAlert,
  Receipt,
  Ticket,
  Users,
  Menu,
  X,
  Landmark,
} from 'lucide-react'
import { useCustomer } from '../context/CustomerContext.jsx'
import { useLanguage, LANGUAGES } from '../context/LanguageContext.jsx'

const CUSTOMER_LINKS = [
  { to: '/', key: 'nav_dashboard', icon: LayoutDashboard, end: true },
  { to: '/form-scanner', key: 'nav_form_scanner', icon: ScanLine },
  { to: '/language-assistant', key: 'nav_language_assistant', icon: Languages },
  { to: '/checklist', key: 'nav_checklist', icon: ClipboardList },
  { to: '/error-checker', key: 'nav_error_checker', icon: ShieldAlert },
  { to: '/status-vault', key: 'nav_status_vault', icon: Receipt },
  { to: '/appointment', key: 'nav_appointment', icon: Ticket },
]

const STAFF_LINKS = [
  { to: '/employee', key: 'nav_employee', icon: Users },
]

const TITLE_KEYS = {
  '/': ['title_home', 'subtitle_home'],
  '/form-scanner': ['title_form_scanner', 'subtitle_form_scanner'],
  '/language-assistant': ['title_language_assistant', 'subtitle_language_assistant'],
  '/checklist': ['title_checklist', 'subtitle_checklist'],
  '/error-checker': ['title_error_checker', 'subtitle_error_checker'],
  '/status-vault': ['title_status_vault', 'subtitle_status_vault'],
  '/appointment': ['title_appointment', 'subtitle_appointment'],
  '/employee': ['title_employee', 'subtitle_employee'],
}

function NavLinks({ onNavigate, t }) {
  return (
    <>
      <div className="sidebar-section-label">{t('nav_customer_section')}</div>
      {CUSTOMER_LINKS.map(({ to, key, icon: Icon, end }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          onClick={onNavigate}
          className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
        >
          <Icon size={17} />
          {t(key)}
        </NavLink>
      ))}
      <div className="sidebar-section-label">{t('nav_staff_section')}</div>
      {STAFF_LINKS.map(({ to, key, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          onClick={onNavigate}
          className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
        >
          <Icon size={17} />
          {t(key)}
        </NavLink>
      ))}
    </>
  )
}

function LanguageSwitcher() {
  const { lang, setLang } = useLanguage()
  return (
    <div className="lang-switcher">
      {LANGUAGES.map((l) => (
        <button
          key={l.code}
          className={`lang-pill${lang === l.code ? ' active' : ''}`}
          onClick={() => setLang(l.code)}
        >
          {l.label}
        </button>
      ))}
    </div>
  )
}

export default function Layout() {
  const [drawerOpen, setDrawerOpen] = useState(false)
  const { customerName, setCustomerName, customerId } = useCustomer()
  const { t } = useLanguage()
  const location = useLocation()
  const [titleKey, subtitleKey] = TITLE_KEYS[location.pathname] || ['brand_name', '']

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-mark">
            <Landmark size={19} />
          </div>
          <div className="sidebar-brand-text">
            <h1>{t('brand_name')}</h1>
            <p>{t('brand_tagline')}</p>
          </div>
        </div>
        <LanguageSwitcher />
        <nav className="sidebar-nav">
          <NavLinks t={t} />
        </nav>
        <div className="sidebar-footer">
          {t('nav_footer')}
          <br />
          <a href="/classic-walkthrough" style={{ color: '#aeb4ea' }}>
            {t('nav_classic_walkthrough')}
          </a>
        </div>
      </aside>

      <div className="main-area">
        <div className="mobile-topbar">
          <button
            className="btn btn-ghost small"
            style={{ color: '#fff', borderColor: 'rgba(255,255,255,0.4)' }}
            onClick={() => setDrawerOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={18} />
          </button>
          <strong>{t('brand_name')}</strong>
          <span style={{ width: 34 }} />
        </div>

        {drawerOpen && (
          <div className="mobile-nav-drawer" onClick={() => setDrawerOpen(false)}>
            <div className="mobile-nav-panel" onClick={(e) => e.stopPropagation()}>
              <div className="flex justify-between items-center" style={{ marginBottom: 16 }}>
                <strong style={{ color: '#fff' }}>{t('brand_name')}</strong>
                <button
                  className="btn btn-ghost small"
                  style={{ color: '#fff', borderColor: 'rgba(255,255,255,0.4)' }}
                  onClick={() => setDrawerOpen(false)}
                  aria-label="Close menu"
                >
                  <X size={16} />
                </button>
              </div>
              <LanguageSwitcher />
              <div style={{ height: 10 }} />
              <NavLinks onNavigate={() => setDrawerOpen(false)} t={t} />
            </div>
          </div>
        )}

        <header className="topbar">
          <div>
            <h2>{t(titleKey)}</h2>
            {subtitleKey && <p className="topbar-sub">{t(subtitleKey)}</p>}
          </div>
          <div className="customer-chip" title={`Customer ID: ${customerId}`}>
            <Users size={14} />
            <input
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              placeholder={t('your_name_placeholder')}
            />
          </div>
        </header>

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
