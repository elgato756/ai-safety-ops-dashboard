'use client'

import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'

type Incident = {
  id: number
  source: string
  source_url?: string
  source_community?: string
  title: string
  raw_content?: string
  category: string
  severity: number
  confidence: number
  summary: string
  escalation_team: string
  should_escalate: boolean
  status: string
  analyst_notes?: string
  created_at: string
}

type AuditEvent = {
  id: number
  incident_id?: number
  action: string
  actor: string
  details?: string
  created_at: string
}

const API_BASE = 'http://localhost:8000'

const FILTERS = [
  'All',
  'High severity',
  'Open',
  'Escalated',
  'Regulatory',
  'Fraud/scam',
  'Jailbreak',
  'X',
]

export default function Home() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)
  const [activeFilter, setActiveFilter] = useState('All')
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null)
  const [notesDraft, setNotesDraft] = useState('')
  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>([])

  useEffect(() => {
    fetchIncidents()
  }, [])

  useEffect(() => {
    if (selectedIncident) {
      setNotesDraft(selectedIncident.analyst_notes || '')
      fetchAuditEvents(selectedIncident.id)
    } else {
      setAuditEvents([])
    }
  }, [selectedIncident])

  const fetchIncidents = async () => {
    const res = await axios.get(`${API_BASE}/incidents`)
    setIncidents(res.data)

    if (selectedIncident) {
      const refreshed = res.data.find((item: Incident) => item.id === selectedIncident.id)
      if (refreshed) {
        setSelectedIncident(refreshed)
      }
    }
  }

  const fetchAuditEvents = async (incidentId: number) => {
    try {
      const res = await axios.get(`${API_BASE}/incidents/${incidentId}/audit`)
      setAuditEvents(res.data)
    } catch {
      setAuditEvents([])
    }
  }

  const scanSource = async (source: 'reddit' | 'regulatory' | 'x') => {
    setLoading(true)
    await axios.post(`${API_BASE}/scan/${source}`)
    await fetchIncidents()
    setLoading(false)
  }

  const scanAll = async () => {
    setLoading(true)

    try {
      await Promise.allSettled([
        axios.post(`${API_BASE}/scan/reddit`),
        axios.post(`${API_BASE}/scan/regulatory`),
        axios.post(`${API_BASE}/scan/x`),
      ])

      await fetchIncidents()
    } finally {
      setLoading(false)
    }
  }


  const updateIncident = async (
    id: number,
    status: string,
    analystNotes?: string
  ) => {
    await axios.patch(`${API_BASE}/incidents/${id}`, {
      status,
      analyst_notes: analystNotes,
    })
    await fetchIncidents()
  }

  const updateStatus = async (id: number, status: string) => {
    await updateIncident(id, status)
  }

  const saveNotes = async () => {
    if (!selectedIncident) return
    await updateIncident(selectedIncident.id, selectedIncident.status, notesDraft)
  }

  const escalate = async (id: number) => {
    await axios.post(`${API_BASE}/incidents/${id}/escalate`)
    await fetchIncidents()
  }

  const filteredIncidents = useMemo(() => {
    return incidents.filter((incident) => {
      const category = incident.category.toLowerCase()

      if (activeFilter === 'All') return true
      if (activeFilter === 'High severity') return incident.severity >= 8
      if (activeFilter === 'Open') return incident.status === 'open'
      if (activeFilter === 'Escalated') return incident.status === 'escalated'
      if (activeFilter === 'Regulatory') return category.includes('regulatory')
      if (activeFilter === 'Fraud/scam') {
        return category.includes('fraud') || category.includes('scam')
      }
      if (activeFilter === 'Jailbreak') return category.includes('jailbreak')
      if (activeFilter === 'X') return incident.source === 'x'

      return true
    })
  }, [incidents, activeFilter])

  const severityClass = (severity: number) => {
    if (severity >= 8) return 'bg-red-100 text-red-800 border-red-200'
    if (severity >= 5) return 'bg-yellow-100 text-yellow-800 border-yellow-200'
    return 'bg-green-100 text-green-800 border-green-200'
  }

  return (
    <main className="min-h-screen bg-slate-50 p-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="mb-2 text-sm font-medium text-slate-500">
              Human-in-the-loop Trust & Safety prototype
            </p>
            <h1 className="text-3xl font-bold text-slate-900">
              AI Safety Ops Dashboard
            </h1>
            <p className="mt-2 max-w-2xl text-slate-600">
              Aggregates emerging AI misuse, policy, integrity, and regulatory signals
              for analyst review. The system recommends review paths but does not make
              automated enforcement decisions.
            </p>
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => scanSource('reddit')}
              disabled={loading}
              className="rounded-xl bg-slate-900 px-4 py-2 text-white shadow-sm disabled:opacity-50"
            >
              {loading ? 'Scanning...' : 'Scan Reddit'}
            </button>

            <button
              onClick={() => scanSource('regulatory')}
              disabled={loading}
              className="rounded-xl border bg-white px-4 py-2 text-slate-800 shadow-sm disabled:opacity-50"
            >
              Scan Regulatory
            </button>

            <button
              onClick={() => scanSource('x')}
              disabled={loading}
              className="rounded-xl border bg-white px-4 py-2 text-slate-800 shadow-sm disabled:opacity-50"
            >
              Scan X
            </button>

            <button
              onClick={scanAll}
              disabled={loading}
              className="rounded-xl border border-slate-900 bg-slate-100 px-4 py-2 text-slate-900 shadow-sm disabled:opacity-50"
            >
              Scan All
            </button>
          </div>
        </div>

        <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-4">
          <Metric label="Total Incidents" value={incidents.length} />
          <Metric label="Open" value={incidents.filter(i => i.status === 'open').length} />
          <Metric label="Escalated" value={incidents.filter(i => i.status === 'escalated').length} />
          <Metric label="High Severity" value={incidents.filter(i => i.severity >= 8).length} />
        </div>

        <div className="mb-6 flex flex-wrap gap-2">
          {FILTERS.map((filter) => (
            <button
              key={filter}
              onClick={() => setActiveFilter(filter)}
              className={`rounded-full border px-3 py-2 text-sm ${
                activeFilter === filter
                  ? 'bg-slate-900 text-white'
                  : 'bg-white text-slate-700'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-[1fr_420px]">
          <section>
            <div className="mb-4 text-sm text-slate-500">
              Showing {filteredIncidents.length} of {incidents.length} incidents
            </div>

            <div className="space-y-4">
              {filteredIncidents.map((incident) => (
                <div
                  key={incident.id}
                  onClick={() => setSelectedIncident(incident)}
                  className={`cursor-pointer rounded-2xl border bg-white p-5 shadow-sm transition hover:border-slate-400 ${
                    selectedIncident?.id === incident.id ? 'border-slate-900' : ''
                  }`}
                >
                  <div className="mb-3 flex items-start justify-between gap-4">
                    <div>
                      <div className="mb-2 flex flex-wrap gap-2">
                        <span className="rounded-full border px-2 py-1 text-xs text-slate-600">
                          r/{incident.source_community}
                        </span>
                        <span className="rounded-full border px-2 py-1 text-xs text-slate-600">
                          {incident.category}
                        </span>
                        <span className="rounded-full border px-2 py-1 text-xs text-slate-600">
                          {incident.status}
                        </span>
                      </div>

                      <h2 className="text-lg font-semibold text-slate-900">
                        {incident.title}
                      </h2>
                    </div>

                    <span className={`rounded-full border px-3 py-1 text-sm font-medium ${severityClass(incident.severity)}`}>
                      Severity {incident.severity}/10
                    </span>
                  </div>

                  <p className="mb-4 text-sm leading-6 text-slate-700">
                    {incident.summary}
                  </p>

                  <div className="mb-4 grid grid-cols-1 gap-3 text-sm md:grid-cols-3">
                    <Info label="Confidence" value={`${Math.round(incident.confidence * 100)}%`} />
                    <Info label="Review Team" value={incident.escalation_team} />
                    <Info label="Review Recommended" value={incident.should_escalate ? 'Yes' : 'No'} />
                  </div>

                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={(event) => {
                        event.stopPropagation()
                        updateStatus(incident.id, 'triaged')
                      }}
                      className="rounded-lg border px-3 py-2 text-sm"
                    >
                      Mark Triaged
                    </button>

                    <button
                      onClick={(event) => {
                        event.stopPropagation()
                        escalate(incident.id)
                      }}
                      className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white"
                    >
                      Escalate
                    </button>

                    <button
                      onClick={(event) => {
                        event.stopPropagation()
                        updateStatus(incident.id, 'closed')
                      }}
                      className="rounded-lg border px-3 py-2 text-sm"
                    >
                      Close
                    </button>
                  </div>
                </div>
              ))}

              {filteredIncidents.length === 0 && (
                <div className="rounded-2xl border bg-white p-8 text-center text-slate-500">
                  No incidents match this filter.
                </div>
              )}
            </div>
          </section>

          <aside className="h-fit rounded-2xl border bg-white p-5 shadow-sm lg:sticky lg:top-8">
            {!selectedIncident ? (
              <div className="py-10 text-center text-slate-500">
                Select an incident to review details, evidence, and analyst notes.
              </div>
            ) : (
              <div>
                <div className="mb-4 flex items-start justify-between gap-3">
                  <div>
                    <p className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-500">
                      Incident Detail
                    </p>
                    <h3 className="text-lg font-semibold text-slate-900">
                      {selectedIncident.title}
                    </h3>
                  </div>

                  <button
                    onClick={() => setSelectedIncident(null)}
                    className="rounded-lg border px-2 py-1 text-sm"
                  >
                    Close
                  </button>
                </div>

                <div className="mb-4 grid grid-cols-2 gap-3 text-sm">
                  <Info label="Status" value={selectedIncident.status} />
                  <Info label="Category" value={selectedIncident.category} />
                  <Info label="Severity" value={`${selectedIncident.severity}/10`} />
                  <Info label="Confidence" value={`${Math.round(selectedIncident.confidence * 100)}%`} />
                </div>

                <div className="mb-4 rounded-xl bg-slate-50 p-4">
                  <p className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-500">
                    Analyst Summary
                  </p>
                  <p className="text-sm leading-6 text-slate-700">
                    {selectedIncident.summary}
                  </p>
                </div>

                <div className="mb-4 rounded-xl bg-slate-50 p-4">
                  <p className="mb-2 text-xs font-medium uppercase tracking-wide text-slate-500">
                    Source Content
                  </p>
                  <p className="text-sm leading-6 text-slate-700">
                    {selectedIncident.raw_content || 'No body text available for this signal.'}
                  </p>
                </div>

                <div className="mb-4">
                  <label className="mb-2 block text-xs font-medium uppercase tracking-wide text-slate-500">
                    Analyst Notes
                  </label>
                  <textarea
                    value={notesDraft}
                    onChange={(event) => setNotesDraft(event.target.value)}
                    placeholder="Add investigation notes, context, reviewer judgment, or follow-up actions..."
                    className="h-36 w-full rounded-xl border p-3 text-sm outline-none focus:border-slate-900"
                  />
                </div>

                <div className="mb-4 flex flex-wrap gap-2">
                  <button
                    onClick={saveNotes}
                    className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white"
                  >
                    Save Notes
                  </button>

                  <button
                    onClick={() => updateIncident(selectedIncident.id, 'triaged', notesDraft)}
                    className="rounded-lg border px-3 py-2 text-sm"
                  >
                    Save & Triaged
                  </button>

                  <button
                    onClick={() => updateIncident(selectedIncident.id, 'closed', notesDraft)}
                    className="rounded-lg border px-3 py-2 text-sm"
                  >
                    Save & Close
                  </button>
                </div>

                <div className="mb-4 rounded-xl bg-slate-50 p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                      Audit Trail
                    </p>
                    <button
                      onClick={() => fetchAuditEvents(selectedIncident.id)}
                      className="rounded-lg border bg-white px-2 py-1 text-xs"
                    >
                      Refresh
                    </button>
                  </div>

                  <div className="space-y-3">
                    {auditEvents.length === 0 ? (
                      <p className="text-sm text-slate-500">
                        No audit events recorded yet.
                      </p>
                    ) : (
                      auditEvents.map((event) => (
                        <div key={event.id} className="rounded-lg border bg-white p-3">
                          <div className="mb-1 flex items-center justify-between gap-2">
                            <p className="text-sm font-medium text-slate-800">
                              {event.action.replaceAll('_', ' ')}
                            </p>
                            <p className="text-xs text-slate-500">
                              {new Date(event.created_at).toLocaleString()}
                            </p>
                          </div>

                          <p className="text-xs text-slate-500">
                            Actor: {event.actor}
                          </p>

                          {event.details && (
                            <p className="mt-2 text-sm leading-5 text-slate-700">
                              {event.details}
                            </p>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                </div>

                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => escalate(selectedIncident.id)}
                    className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
                  >
                    Escalate for Review
                  </button>

                  {selectedIncident.source_url && (
                    <a
                      href={selectedIncident.source_url}
                      target="_blank"
                      className="rounded-lg border px-3 py-2 text-sm"
                    >
                      View Source
                    </a>
                  )}
                </div>
              </div>
            )}
          </aside>
        </div>
      </div>
    </main>
  )
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-2 text-3xl font-bold text-slate-900">{value}</p>
    </div>
  )
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 break-words font-medium text-slate-800">{value}</p>
    </div>
  )
}
