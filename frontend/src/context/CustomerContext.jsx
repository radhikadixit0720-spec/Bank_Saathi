import { createContext, useContext, useEffect, useState } from 'react'

const CustomerContext = createContext(null)

function makeGuestId() {
  return `guest-${Math.random().toString(36).slice(2, 8)}`
}

export function CustomerProvider({ children }) {
  const [customerId, setCustomerId] = useState(() => {
    return localStorage.getItem('bs_customer_id') || makeGuestId()
  })
  const [customerName, setCustomerName] = useState(() => {
    return localStorage.getItem('bs_customer_name') || ''
  })

  useEffect(() => {
    localStorage.setItem('bs_customer_id', customerId)
  }, [customerId])

  useEffect(() => {
    localStorage.setItem('bs_customer_name', customerName)
  }, [customerName])

  return (
    <CustomerContext.Provider value={{ customerId, customerName, setCustomerName, setCustomerId }}>
      {children}
    </CustomerContext.Provider>
  )
}

export function useCustomer() {
  const ctx = useContext(CustomerContext)
  if (!ctx) throw new Error('useCustomer must be used within CustomerProvider')
  return ctx
}
