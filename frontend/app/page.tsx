'use client'

import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'

type Incident = {
  id: number
  source: string
  source_url?: string
  source_community?: string
  title: string
  is_relevant: boolean
  category: string
  severity: number
  confidence: number
  evidence?: string
  missing_context?: string
  analyst_summary: string
  suggested_next_steps?: string
  recommended_review_team: string
  human_review_recommended: boolean
  status: string
  analyst_notes?: string
  created_at: string
}

const API_BASE = 'http://localhost:8000'
const STATUSES = ['open', 'triaged', 'escalated', 'closed']

export default function Home() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)
  const [categoryFilter, setCategoryFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null)
  const [notes, setNotes] = useState('')

  useEffect(() => {
    fetchIncidents()
  }, [])

  const fetchIncidents = async () => {
    const res = await axios.get(`${API_BASE}/incidents`)
    setIncidents(res.data)
  }

  const scanReddit = async () => {
    setLoading(true)
    try {
      await axios.post(`${API_BASE}/scan/reddit`)
      await fetchIncidents()
    } finally {
      setLoading(false)
    }
  }

  const updateStatus = async (id: number, status: string, analystNotes?: string) => {
    await axios.patch(`${API_BASE}/incidents/${id}`, {
      status,
      analyst_notes: analystNotes,
    })
    await fetchIncidents()
  }

  const escalate = async (id: number) => {
    await axios.post(`${API_BASE}/incidents/${id}/escalate`)
    await fetchIncidents()
  }

  const categories = useMemo(() => {
    return Array.from(new Set(incidents.map((incident) => incident.category))).sort()
  }, [incidents])

  const filteredIncidents = useMemo(() => {
    return incidents.filter((incident) => {
      const matchesCategory = categoryFilter === 'all' || incident.category === categoryFilter
      const matchesStatus = statusFilter === 'all' || incident.status === statusFilter
      return matchesCategory && matchesStatus
    })
  }, [incidents, categoryFilter, statusFilter])

  const openIncident = (incident: Incident) => {
    setSelectedIncident(incident)
    setNotes(incident.analyst_notes || '')
  }

  const highSeverityCount = incidents.filter((incident) => incident.severity >= 8).length
  const reviewRecommendedCount = incidents.filter((incident) => incident.human_review_recommended).length

  return (
    <main className="min-h-screen bg-slate-50 p-6 text-slate-900 md:p-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="mb-2 text-sm font-medium uppercase tracking-wide text-slate-500">
              Human-in-the-loop Trust & Safety prototype
            </p>
            <h1 className="text-3xl font-bold tracking-tight md:text-4xl">
              AI Risk Intelligence Dashboard
            </h1>
            <p className="mt-2 max-w-3xl text-slate-600">
              Aggregates public signals, structures possible risks, and recommends review paths for analysts. It does not make final enforcement decisions.
            </p>
          </div>

          <button
            onClick={scanReddit}
            disabled={loading}
            className="rounded-2xl bg-slate-900 px-5 py-3 font-medium text-white shadow-sm transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Scanning signals...' : 'Scan Reddit'}
          </button>
        </div>

        <section className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-4">
          <Metric label="Total Incidents" value={incidents.length} />
          <Metric label="Open" value={incidents.filter((i) => i.status === 'open').length} />
          <Metric label="High Severity" value={highSeverityCount} />
          <Metric label="Review Recommended" value={reviewRecommendedCount} />
        </section>

        <section className="mb-6 flex flex-col gap-3 rounded-2xl border bg-white p-4 shadow-sm md:flex-row md:items-center">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-slate-500">Category</label>
            <select
              value={categoryFilter}
              onChange={(event) => setCategoryFilter(event.target.value)}
              className="rounded-xl border bg-white px-3 py-2 text-sm"
            >
              <option value="all">All categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-slate-500">Status</label>
            <select
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value)}
              className="rounded-xl border bg-white px-3 py-2 text-sm"
            >
              <option value="all">All statuses</option>
              {STATUSES.map((status) => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>
        </section>

        <section className="space-y-4">
          {filteredIncidents.map((incident) => (
            <article key={incident.id} className="rounded-2xl border bg-white p-5 shadow-sm">
              <div className="mb-3 flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                <div>
                  <div className="mb-2 flex flex-wrap gap-2">
                    <Pill>r/{incident.source_community || 'unknown'}</Pill>
                    <Pill>{incident.category}</Pill>
                    <Pill>{incident.status}</Pill>
                    {incident.human_review_recommended && <Pill>human review</Pill>}
                  </div>
                  <h2 className="text-lg font-semibold">{incident.title}</h2>
                </div>

                <span className={`rounded-full border px-3 py-1 text-sm font-semibold ${severityClass(incident.severity)}`}>
                  Severity {incident.severity}/10
                </span>
              </div>

              <p className="mb-4 text-sm leading-6 text-slate-700">{incident.analyst_summary}</p>

              <div className="mb-4 grid grid-cols-1 gap-3 text-sm md:grid-cols-3">
                <Info label="Confidence" value={`${Math.round(incident.confidence * 100)}%`} />
                <Info label="Review Team" value={incident.recommended_review_team} />
                <Info label="Relevant" value={incident.is_relevant ? 'Yes' : 'No'} />
              </div>

              <div className="flex flex-wrap gap-2">
                <button onClick={() => updateStatus(incident.id, 'triaged')} className="rounded-xl border px-3 py-2 text-sm hover:bg-slate-50">
                  Mark Triaged
                </button>
                <button onClick={() => escalate(incident.id)} className="rounded-xl bg-slate-900 px-3 py-2 text-sm text-white hover:bg-slate-700">
                  Escalate
                </button>
                <button onClick={() => updateStatus(incident.id, 'closed')} className="rounded-xl border px-3 py-2 text-sm hover:bg-slate-50">
                  Close
                </button>
                <button onClick={() => openIncident(incident)} className="rounded-xl border px-3 py-2 text-sm hover:bg-slate-50">
                  Review Details
                </button>
                {incident.source_url && (
                  <a href={incident.source_url} target="_blank" className="rounded-xl border px-3 py-2 text-sm hover:bg-slate-50">
                    View Source
                  </a>
                )}
              </div>
            </article>
          ))}

          {filteredIncidents.length === 0 && (
            <div className="rounded-2xl border bg-white p-10 text-center text-slate-600 shadow-sm">
              No incidents yet. Start by scanning Reddit.
            </div>
          )}
        </section>
      </div>

      {selectedIncident && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4">
          <div className="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-3xl bg-white p-6 shadow-xl">
            <div className="mb-4 flex items-start justify-between gap-4">
              <div>
                <p className="text-sm text-slate-500">Incident #{selectedIncident.id}</p>
                <h2 className="text-2xl font-bold">{selectedIncident.title}</h2>
              </div>
              <button onClick={() => setSelectedIncident(null)} className="rounded-xl border px-3 py-2 text-sm">
                Close
              </button>
            </div>

            <DetailBlock title="Analyst Summary" body={selectedIncident.analyst_summary} />
            <DetailBlock title="Evidence" body={selectedIncident.evidence || 'No evidence details returned.'} />
            <DetailBlock title="Missing Context" body={selectedIncident.missing_context || 'No missing context noted.'} />
            <DetailBlock title="Suggested Next Steps" body={selectedIncident.suggested_next_steps || 'No next steps returned.'} />

            <div className="mt-5">
              <label className="mb-2 block text-sm font-medium text-slate-700">Analyst Notes</label>
              <textarea
                value={notes}
                onChange={(event) => setNotes(event.target.value)}
                className="h-32 w-full rounded-2xl border p-3 text-sm"
                placeholder="Add context, decision rationale, or follow-up notes..."
              />
              <div className="mt-3 flex gap-2">
                <button
                  onClick={async () => {
                    await updateStatus(selectedIncident.id, selectedIncident.status, notes)
                    setSelectedIncident(null)
                  }}
                  className="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white"
                >
                  Save Notes
                </button>
                <button
                  onClick={async () => {
                    await updateStatus(selectedIncident.id, 'triaged', notes)
                    setSelectedIncident(null)
                  }}
                  className="rounded-xl border px-4 py-2 text-sm"
                >
                  Save & Mark Triaged
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </div>
  )
}

function Pill({ children }: { children: React.ReactNode }) {
  return <span className="rounded-full border px-2 py-1 text-xs text-slate-600">{children}</span>
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 font-medium text-slate-800">{value}</p>
    </div>
  )
}

function DetailBlock({ title, body }: { title: string; body: string }) {
  return (
    <div className="mb-4 rounded-2xl bg-slate-50 p-4">
      <h3 className="mb-2 font-semibold">{title}</h3>
      <p className="whitespace-pre-wrap text-sm leading-6 text-slate-700">{body}</p>
    </div>
  )
}

function severityClass(severity: number) {
  if (severity >= 8) return 'bg-red-100 text-red-800 border-red-200'
  if (severity >= 5) return 'bg-yellow-100 text-yellow-800 border-yellow-200'
  return 'bg-green-100 text-green-800 border-green-200'
}
