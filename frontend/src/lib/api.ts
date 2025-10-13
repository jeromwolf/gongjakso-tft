/**
 * API Client for Gongjakso TFT Backend
 */
import axios, { AxiosError } from 'axios';
import type {
  AuthResponse,
  LoginRequest,
  SignupRequest,
  User,
  Blog,
  BlogListResponse,
  BlogCreateRequest,
  BlogUpdateRequest,
  SubscriberCreateRequest,
  SubscriptionStatus,
  Newsletter,
  NewsletterListResponse,
  NewsletterCreateRequest,
  SubscriberListResponse,
  Project,
  ProjectListResponse,
  ProjectCreateRequest,
  ProjectUpdateRequest,
  Activity,
  ActivityListResponse,
  ActivityCreateRequest,
  ActivityUpdateRequest,
  APIError,
} from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<APIError>) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============ Auth API ============

export const authAPI = {
  /**
   * Sign up a new user
   */
  signup: async (data: SignupRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/signup', data);
    // Store token and user info
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  },

  /**
   * Log in an existing user
   */
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/login', data);
    // Store token and user info
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    return response.data;
  },

  /**
   * Get current user profile
   */
  getMe: async (): Promise<User> => {
    const response = await api.get<User>('/api/auth/me');
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  /**
   * Log out (client-side only)
   */
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/';
  },

  /**
   * Get current user from localStorage
   */
  getCurrentUser: (): User | null => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },
};

// ============ Blog API ============

export const blogAPI = {
  /**
   * Get blog list with pagination
   */
  list: async (params: {
    page?: number;
    page_size?: number;
    status?: string;
  } = {}): Promise<BlogListResponse> => {
    const response = await api.get<BlogListResponse>('/api/blog', { params });
    return response.data;
  },

  /**
   * Get single blog post by ID
   */
  getById: async (id: number): Promise<Blog> => {
    const response = await api.get<Blog>(`/api/blog/${id}`);
    return response.data;
  },

  /**
   * Get single blog post by slug
   */
  getBySlug: async (slug: string): Promise<Blog> => {
    const response = await api.get<Blog>(`/api/blog/slug/${slug}`);
    return response.data;
  },

  /**
   * Create a new blog post (requires auth)
   */
  create: async (data: BlogCreateRequest): Promise<Blog> => {
    const response = await api.post<Blog>('/api/blog', data);
    return response.data;
  },

  /**
   * Update an existing blog post (requires auth)
   */
  update: async (id: number, data: BlogUpdateRequest): Promise<Blog> => {
    const response = await api.put<Blog>(`/api/blog/${id}`, data);
    return response.data;
  },

  /**
   * Delete a blog post (requires auth)
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/blog/${id}`);
  },

  /**
   * Publish/unpublish a blog post (requires auth)
   */
  togglePublish: async (id: number, publish: boolean): Promise<Blog> => {
    const response = await api.post<Blog>(`/api/blog/${id}/publish`, { publish });
    return response.data;
  },
};

// ============ Newsletter API ============

export const newsletterAPI = {
  /**
   * Subscribe to newsletter
   */
  subscribe: async (data: SubscriberCreateRequest): Promise<SubscriptionStatus> => {
    const response = await api.post<SubscriptionStatus>('/api/newsletter/subscribe', data);
    return response.data;
  },

  /**
   * Unsubscribe from newsletter
   */
  unsubscribe: async (email: string): Promise<void> => {
    await api.post('/api/newsletter/unsubscribe', { email });
  },

  /**
   * Check subscription status
   */
  checkStatus: async (email: string): Promise<SubscriptionStatus> => {
    const response = await api.get<SubscriptionStatus>('/api/newsletter/status', {
      params: { email },
    });
    return response.data;
  },

  /**
   * Get newsletter list (Admin)
   */
  list: async (params: {
    page?: number;
    page_size?: number;
    status?: string;
  } = {}): Promise<NewsletterListResponse> => {
    const response = await api.get<NewsletterListResponse>('/api/newsletter', { params });
    return response.data;
  },

  /**
   * Get newsletter by ID (Admin)
   */
  getById: async (id: number): Promise<Newsletter> => {
    const response = await api.get<Newsletter>(`/api/newsletter/${id}`);
    return response.data;
  },

  /**
   * Create newsletter (Admin)
   */
  create: async (data: NewsletterCreateRequest): Promise<Newsletter> => {
    const response = await api.post<Newsletter>('/api/newsletter', data);
    return response.data;
  },

  /**
   * Send newsletter to all subscribers (Admin)
   */
  send: async (id: number): Promise<void> => {
    await api.post(`/api/newsletter/${id}/send`);
  },

  /**
   * Get subscriber list (Admin)
   */
  subscribers: async (params: {
    page?: number;
    page_size?: number;
    status?: string;
  } = {}): Promise<SubscriberListResponse> => {
    const response = await api.get<SubscriberListResponse>('/api/newsletter/subscribers', { params });
    return response.data;
  },
};

// ============ Project API ============

export const projectAPI = {
  /**
   * Get project list with pagination
   */
  list: async (params: {
    page?: number;
    page_size?: number;
    status?: string;
    category?: string;
  } = {}): Promise<ProjectListResponse> => {
    const response = await api.get<ProjectListResponse>('/api/projects', { params });
    return response.data;
  },

  /**
   * Get single project by ID
   */
  getById: async (id: number): Promise<Project> => {
    const response = await api.get<Project>(`/api/projects/${id}`);
    return response.data;
  },

  /**
   * Get single project by slug
   */
  getBySlug: async (slug: string): Promise<Project> => {
    const response = await api.get<Project>(`/api/projects/slug/${slug}`);
    return response.data;
  },

  /**
   * Create a new project (requires admin auth)
   */
  create: async (data: ProjectCreateRequest): Promise<Project> => {
    const response = await api.post<Project>('/api/projects', data);
    return response.data;
  },

  /**
   * Update an existing project (requires admin auth)
   */
  update: async (id: number, data: ProjectUpdateRequest): Promise<Project> => {
    const response = await api.put<Project>(`/api/projects/${id}`, data);
    return response.data;
  },

  /**
   * Delete a project (requires admin auth)
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/projects/${id}`);
  },
};

// ============ AI API ============

export interface AIGenerateBlogRequest {
  topic: string;
  style?: 'technical' | 'casual' | 'tutorial';
  length?: 'short' | 'medium' | 'long';
  save_as_draft?: boolean;
}

export interface AIGenerateBlogResponse {
  blog_id?: number;
  title: string;
  excerpt: string;
  content: string;
  tags: string[];
  status: string;
}

export const aiAPI = {
  /**
   * Generate blog content using AI (requires admin auth)
   */
  generateBlog: async (data: AIGenerateBlogRequest): Promise<AIGenerateBlogResponse> => {
    const response = await api.post<AIGenerateBlogResponse>('/api/ai/generate-blog', data);
    return response.data;
  },

  /**
   * Preview AI-generated content (requires admin auth)
   */
  preview: async (topic: string, style: string = 'technical'): Promise<any> => {
    const response = await api.post('/api/ai/preview', { topic, style });
    return response.data;
  },
};

// ============ Activity API ============

export const activityAPI = {
  /**
   * Get activity list with pagination
   */
  list: async (params: {
    page?: number;
    page_size?: number;
    activity_type?: string;
  } = {}): Promise<ActivityListResponse> => {
    const response = await api.get<ActivityListResponse>('/api/activity', { params });
    return response.data;
  },

  /**
   * Get single activity by ID
   */
  getById: async (id: number): Promise<Activity> => {
    const response = await api.get<Activity>(`/api/activity/${id}`);
    return response.data;
  },

  /**
   * Create a new activity (requires auth)
   */
  create: async (data: ActivityCreateRequest): Promise<Activity> => {
    const response = await api.post<Activity>('/api/activity', data);
    return response.data;
  },

  /**
   * Update an existing activity (requires auth)
   */
  update: async (id: number, data: ActivityUpdateRequest): Promise<Activity> => {
    const response = await api.put<Activity>(`/api/activity/${id}`, data);
    return response.data;
  },

  /**
   * Delete an activity (requires auth)
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/activity/${id}`);
  },
};

export default api;
