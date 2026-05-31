'use client'

import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'

type Incident = {
  id: number
  source: string
  source_url?: string
  source_community?: string
  title: string
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

const API_BASE = 'http://localhost:8000'

const FILTERS = [
  'All',
  'High severity',
  'Open',
  'Escalated',
  'Regulatory',
  'Fraud/scam',
  'Jailbreak',
]

export default function Home() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(false)
  const [activeFilter, setActiveFilter] = useState('All')

  useEffect(() => {
    fetchIncidents()
  }, [])

  const fetchIncidents = async () => {
    const res = await axios.get(`${API_BASE}/incidents`)
    setIncidents(res.data)
  }

  const scanReddit = async () => {
    setLoading(true)
    await axios.post(`${API_BASE}/scan/reddit`)
    await fetchIncidents()
    setLoading(false)
  }

  const updateStatus = async (id: number, status: string) => {
    await axios.patch(`${API_BASE}/incidents/${id}`, { status })
    await fetchIncidents()
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
      <div className="mx-auto max-w-6xl">
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

          <button
            onClick={scanReddit}
            disabled={loading}
            className="rounded-xl bg-slate-900 px-4 py-2 text-white shadow-sm disabled:opacity-50"
          >
            {loading ? 'Scanning...' : 'Scan Reddit'}
          </button>
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

        <div className="mb-4 text-sm text-slate-500">
          Showing {filteredIncidents.length} of {incidents.length} incidents
        </div>

        <div className="space-y-4">
          {filteredIncidents.map((incident) => (
            <div
              key={incident.id}
              className="rounded-2xl border bg-white p-5 shadow-sm"
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
                <Info label="Recommended Review Team" value={incident.escalation_team} />
                <Info label="Human Review Recommended" value={incident.should_escalate ? 'Yes' : 'No'} />
              </div>

              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => updateStatus(incident.id, 'triaged')}
                  className="rounded-lg border px-3 py-2 text-sm"
                >
                  Mark Triaged
                </button>

                <button
                  onClick={() => escalate(incident.id)}
                  className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white"
                >
                  Escalate
                </button>

                <button
                  onClick={() => updateStatus(incident.id, 'closed')}
                  className="rounded-lg border px-3 py-2 text-sm"
                >
                  Close
                </button>

                {incident.source_url && (
                  <a
                    href={incident.source_url}
                    target="_blank"
                    className="rounded-lg border px-3 py-2 text-sm"
                  >
                    View Source
                  </a>
                )}
              </div>
            </div>
          ))}

          {filteredIncidents.length === 0 && (
            <div className="rounded-2xl border bg-white p-8 text-center text-slate-500">
              No incidents match this filter.
            </div>
          )}
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
      <p className="mt-1 font-medium text-slate-800">{value}</p>
    </div>
  )
}
