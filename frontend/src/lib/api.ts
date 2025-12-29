/**
 * API client for communicating with the backend.
 *
 * This module provides a typed fetch wrapper for API calls with
 * automatic credentials inclusion for session management.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';


/**
 * API response wrapper with error handling.
 */
export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}


/**
 * Get authorization headers from auth client.
 */
function getAuthHeaders(): Record<string, string> {
  if (typeof window === 'undefined') return {};

  const sessionStr = localStorage.getItem('auth_session');
  if (!sessionStr) return {};

  try {
    const session = JSON.parse(sessionStr);
    if (session?.token) {
      return {
        Authorization: `Bearer ${session.token}`,
      };
    }
  } catch {
    // Invalid session data
  }

  return {};
}


/**
 * Fetch wrapper that handles API responses and errors.
 *
 * @param endpoint - API endpoint path (e.g., '/todos')
 * @param options - Fetch options
 * @returns Promise resolving to response data
 */
export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const url = `${API_URL}${endpoint}`;

  const authHeaders = getAuthHeaders();

  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
    ...authHeaders,
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        // Response might not be JSON, use default message
      }

      return { data: null, error: errorMessage };
    }

    // Handle empty responses
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      return { data: null as T, error: null };
    }

    const data = await response.json();
    return { data, error: null };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Network error';
    return { data: null, error: errorMessage };
  }
}


/**
 * HTTP method helpers for cleaner API calls.
 */
export const api = {
  get: <T>(endpoint: string, options?: RequestInit) =>
    apiFetch<T>(endpoint, { ...options, method: 'GET' }),

  post: <T>(endpoint: string, body?: unknown, options?: RequestInit) =>
    apiFetch<T>(endpoint, {
      ...options,
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    }),

  put: <T>(endpoint: string, body?: unknown, options?: RequestInit) =>
    apiFetch<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
    }),

  patch: <T>(endpoint: string, body?: unknown, options?: RequestInit) =>
    apiFetch<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: body ? JSON.stringify(body) : undefined,
    }),

  delete: <T>(endpoint: string, options?: RequestInit) =>
    apiFetch<T>(endpoint, { ...options, method: 'DELETE' }),
};
