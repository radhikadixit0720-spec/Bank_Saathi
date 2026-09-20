import { AlertTriangle, CheckCircle2, Clock, XCircle } from 'lucide-react'

const CONFIG = {
  matched: { cls: 'badge-success', icon: CheckCircle2, text: 'Matched' },
  available: { cls: 'badge-success', icon: CheckCircle2, text: 'Available' },
  completed: { cls: 'badge-success', icon: CheckCircle2, text: 'Completed' },
  missing: { cls: 'badge-danger', icon: XCircle, text: 'Missing' },
  rejected: { cls: 'badge-danger', icon: XCircle, text: 'Rejected' },
  needs_attention: { cls: 'badge-warning', icon: AlertTriangle, text: 'Needs verification' },
  action_required: { cls: 'badge-warning', icon: AlertTriangle, text: 'Action required' },
  not_applicable: { cls: 'badge-neutral', icon: Clock, text: 'Not applicable' },
  submitted: { cls: 'badge-info', icon: Clock, text: 'Submitted' },
  pending: { cls: 'badge-info', icon: Clock, text: 'Pending' },
  waiting: { cls: 'badge-info', icon: Clock, text: 'Waiting' },
}

export default function StatusBadge({ status, label }) {
  const conf = CONFIG[status] || { cls: 'badge-neutral', icon: Clock, text: label || status }
  const Icon = conf.icon
  return (
    <span className={`badge ${conf.cls}`}>
      <Icon size={13} />
      {label || conf.text}
    </span>
  )
}
