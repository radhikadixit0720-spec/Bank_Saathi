import { Routes, Route } from 'react-router-dom'
import { CustomerProvider } from './context/CustomerContext.jsx'
import { LanguageProvider } from './context/LanguageContext.jsx'
import Layout from './components/Layout.jsx'
import CustomerDashboard from './pages/CustomerDashboard.jsx'
import FormScannerPage from './pages/FormScannerPage.jsx'
import LanguageAssistantPage from './pages/LanguageAssistantPage.jsx'
import ChecklistPage from './pages/ChecklistPage.jsx'
import ErrorCheckerPage from './pages/ErrorCheckerPage.jsx'
import StatusVaultPage from './pages/StatusVaultPage.jsx'
import TokenAppointmentPage from './pages/TokenAppointmentPage.jsx'
import EmployeeDashboardPage from './pages/EmployeeDashboardPage.jsx'
import LegacyWalkthroughPage from './pages/LegacyWalkthroughPage.jsx'

export default function App() {
  return (
    <LanguageProvider>
      <CustomerProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<CustomerDashboard />} />
            <Route path="/form-scanner" element={<FormScannerPage />} />
            <Route path="/language-assistant" element={<LanguageAssistantPage />} />
            <Route path="/checklist" element={<ChecklistPage />} />
            <Route path="/error-checker" element={<ErrorCheckerPage />} />
            <Route path="/status-vault" element={<StatusVaultPage />} />
            <Route path="/appointment" element={<TokenAppointmentPage />} />
            <Route path="/employee" element={<EmployeeDashboardPage />} />
          </Route>
          {/* Original guided, Hindi text-to-speech field walkthrough - kept
              working exactly as it was, reachable without the new layout. */}
          <Route path="/classic-walkthrough" element={<LegacyWalkthroughPage />} />
        </Routes>
      </CustomerProvider>
    </LanguageProvider>
  )
}
