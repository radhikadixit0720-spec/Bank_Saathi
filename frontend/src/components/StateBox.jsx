import { AlertCircle, Inbox } from 'lucide-react'

export function LoadingState({ message = 'Loading...' }) {
  return (
    <div className="state-box">
      <div className="spinner" />
      <p>{message}</p>
    </div>
  )
}

export function ErrorState({ message = 'Something went wrong.', onRetry }) {
  return (
    <div className="state-box error">
      <AlertCircle size={28} />
      <p>{message}</p>
      {onRetry && (
        <button className="btn btn-secondary small" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  )
}

export function EmptyState({ message = 'Nothing here yet.', icon: Icon = Inbox }) {
  return (
    <div className="state-box">
      <Icon size={28} />
      <p>{message}</p>
    </div>
  )
}
