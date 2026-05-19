import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

export interface Alert {
  id: number;
  keyword: string;
  location: string;
  is_active: boolean;
  created_at: string;
}

export interface Job {
  id: number;
  linkedin_id: string;
  title: string;
  company: string;
  location: string;
  link: string;
  alert_id: number;
  discovered_at: string;
  emailed: boolean;
}

export const api = {
  getAlerts: () => axios.get<Alert[]>(`${API_BASE_URL}/alerts`),
  createAlert: (alert: { keyword: string; location: string }) => 
    axios.post<Alert>(`${API_BASE_URL}/alerts`, alert),
  deleteAlert: (id: number) => axios.delete(`${API_BASE_URL}/alerts/${id}`),
  getJobs: () => axios.get<Job[]>(`${API_BASE_URL}/jobs`),
  triggerScrape: () => axios.post(`${API_BASE_URL}/trigger-scrape`),
};
