import React, { useState, useEffect } from 'react';
import { api } from './api';
import type { Alert, Job } from './api';
import { Briefcase, MapPin, Bell, Trash2, RefreshCw, ExternalLink, CheckCircle } from 'lucide-react';
import { format } from 'date-fns';

function App() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [keyword, setKeyword] = useState('');
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [alertsRes, jobsRes] = await Promise.all([
        api.getAlerts(),
        api.getJobs()
      ]);
      setAlerts(alertsRes.data);
      setJobs(jobsRes.data);
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyword || !location) return;
    try {
      await api.createAlert({ keyword, location });
      setKeyword('');
      setLocation('');
      fetchData();
    } catch (error) {
      console.error("Failed to create alert", error);
    }
  };

  const handleDeleteAlert = async (id: number) => {
    try {
      await api.deleteAlert(id);
      fetchData();
    } catch (error) {
      console.error("Failed to delete alert", error);
    }
  };

  const handleTriggerScrape = async () => {
    setScraping(true);
    try {
      await api.triggerScrape();
      alert("Scraping started in background!");
    } catch (error) {
      console.error("Failed to trigger scrape", error);
    } finally {
      setScraping(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2 text-blue-400">
              <Bell className="w-8 h-8" />
              LinkedIn Job Alerts
            </h1>
            <p className="text-gray-400">Monitor and get updates for your dream jobs.</p>
          </div>
          <button 
            onClick={handleTriggerScrape}
            disabled={scraping}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors font-medium"
          >
            <RefreshCw className={`w-4 h-4 ${scraping ? 'animate-spin' : ''}`} />
            {scraping ? 'Scraping...' : 'Refresh Jobs Now'}
          </button>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Sidebar: Manage Alerts */}
          <div className="lg:col-span-1 space-y-6">
            <section className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <PlusIcon className="w-5 h-5 text-blue-400" />
                Add New Alert
              </h2>
              <form onSubmit={handleCreateAlert} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Job Keyword</label>
                  <div className="relative">
                    <Briefcase className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                    <input 
                      type="text" 
                      value={keyword}
                      onChange={(e) => setKeyword(e.target.value)}
                      placeholder="e.g. Software Engineer"
                      className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-1">Location</label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                    <input 
                      type="text" 
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      placeholder="e.g. San Francisco"
                      className="w-full bg-gray-800 border border-gray-700 rounded-lg pl-10 pr-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                    />
                  </div>
                </div>
                <button 
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
                >
                  Create Alert
                </button>
              </form>
            </section>

            <section className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Bell className="w-5 h-5 text-blue-400" />
                Active Alerts
              </h2>
              {alerts.length === 0 ? (
                <p className="text-gray-500 text-sm">No alerts configured yet.</p>
              ) : (
                <div className="space-y-3">
                  {alerts.map(alert => (
                    <div key={alert.id} className="flex justify-between items-center bg-gray-800 p-3 rounded-lg border border-gray-700">
                      <div>
                        <p className="font-medium text-gray-100">{alert.keyword}</p>
                        <p className="text-xs text-gray-400 flex items-center gap-1">
                          <MapPin className="w-3 h-3" /> {alert.location}
                        </p>
                      </div>
                      <button 
                        onClick={() => handleDeleteAlert(alert.id)}
                        className="text-gray-500 hover:text-red-400 transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>

          {/* Main Content: Job Feed */}
          <div className="lg:col-span-2">
            <section className="bg-gray-900 border border-gray-800 rounded-xl p-6 h-full">
              <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-blue-400" />
                Latest Matches
              </h2>
              {loading ? (
                <div className="flex justify-center items-center h-64">
                  <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
                </div>
              ) : jobs.length === 0 ? (
                <div className="text-center py-20 bg-gray-800/50 rounded-lg border border-dashed border-gray-700">
                  <Briefcase className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400">No matching jobs found yet.</p>
                  <p className="text-sm text-gray-500">Add an alert and trigger a refresh to get started.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {jobs.map(job => (
                    <div key={job.id} className="bg-gray-800 border border-gray-700 p-4 rounded-xl hover:border-blue-500/50 transition-all group">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="text-lg font-bold text-blue-400 group-hover:text-blue-300 transition-colors">
                            {job.title}
                          </h3>
                          <p className="text-gray-300 font-medium">{job.company}</p>
                        </div>
                        <a 
                          href={job.link} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-gray-400 hover:text-blue-400 transition-colors"
                        >
                          <ExternalLink className="w-5 h-5" />
                        </a>
                      </div>
                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400 mt-4">
                        <span className="flex items-center gap-1">
                          <MapPin className="w-4 h-4" /> {job.location}
                        </span>
                        <span className="flex items-center gap-1">
                          <CheckCircle className={`w-4 h-4 ${job.emailed ? 'text-green-500' : 'text-gray-500'}`} />
                          {job.emailed ? 'Email Sent' : 'Pending Email'}
                        </span>
                        <span className="text-gray-600 ml-auto">
                          Discovered: {format(new Date(job.discovered_at), 'MMM d, HH:mm')}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}

function PlusIcon({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className={className}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
    </svg>
  );
}

export default App;
