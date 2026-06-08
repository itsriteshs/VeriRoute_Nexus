// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: Typed HTTP API client helpers.

export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';

export async function apiRequest<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function apiGet<T>(path: string): Promise<T> {
  return apiRequest<T>(path, { method: 'GET' });
}

export async function apiPost<T>(path: string, body?: any): Promise<T> {
  return apiRequest<T>(path, {
    method: 'POST',
    body: body ? JSON.stringify(body) : undefined,
  });
}
