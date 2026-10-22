import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Pathways
export const getPathways = () => api.get('/api/pathways/').then(r => r.data);
export const createPathway = (data) => api.post('/api/pathways/', data).then(r => r.data);

// Beyonders
export const getBeyonders = (params) => api.get('/api/beyonders/', { params }).then(r => r.data);
export const createBeyonder = (data) => api.post('/api/beyonders/', data).then(r => r.data);
export const updateBeyonder = (id, data) => api.put(`/api/beyonders/${id}`, data).then(r => r.data);
export const deleteBeyonder = (id) => api.delete(`/api/beyonders/${id}`).then(r => r.data);

// Potions
export const getPotions = (params) => api.get('/api/potions/', { params }).then(r => r.data);
export const createPotion = (data) => api.post('/api/potions/', data).then(r => r.data);

// Commissions
export const getCommissions = (params) => api.get('/api/commissions/', { params }).then(r => r.data);
export const createCommission = (data) => api.post('/api/commissions/', data).then(r => r.data);
export const updateCommission = (id, data) => api.put(`/api/commissions/${id}`, data).then(r => r.data);
export const deleteCommission = (id) => api.delete(`/api/commissions/${id}`).then(r => r.data);
export const claimCommission = (commissionId, beyonderId) => 
  api.post(`/api/commissions/${commissionId}/claim`, { beyonder_id: beyonderId }).then(r => r.data);

// Claims & Dispatch
export const getClaims = (params) => api.get('/api/claims/', { params }).then(r => r.data);
export const dispatchClaim = (data) => api.post('/api/claims/', data).then(r => r.data);
export const postDebrief = (claimId, data) => api.post(`/api/claims/${claimId}/debrief`, data).then(r => r.data);
export const getMetrics = () => api.get('/api/claims/metrics').then(r => r.data);

// Squads Formation
export const getSquads = () => api.get('/api/squads/').then(r => r.data);
export const getSquad = (id) => api.get(`/api/squads/${id}`).then(r => r.data);
export const createSquad = (data) => api.post('/api/squads/', data).then(r => r.data);
export const updateSquad = (id, data) => api.put(`/api/squads/${id}`, data).then(r => r.data);
export const deleteSquad = (id) => api.delete(`/api/squads/${id}`).then(r => r.data);
export const dispatchSquad = (squadId, commissionId) => 
  api.post(`/api/squads/${squadId}/dispatch`, { commission_id: commissionId }).then(r => r.data);
