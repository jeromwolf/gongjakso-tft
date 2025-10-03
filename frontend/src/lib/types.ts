/**
 * API Types for Gongjakso TFT
 */

// User & Auth Types
export type UserRole = 'admin' | 'user';

export interface User {
  id: number;
  email: string;
  name: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login: string | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  name: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Blog Types
export type BlogStatus = 'draft' | 'published' | 'archived';

export interface Blog {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt: string | null;
  author: string;
  tags: string[];
  status: BlogStatus;
  view_count: number;
  created_at: string;
  updated_at: string;
  published_at: string | null;
}

export interface BlogListItem {
  id: number;
  title: string;
  slug: string;
  excerpt: string | null;
  author: string;
  status: BlogStatus;
  tags: string[];
  view_count: number;
  created_at: string;
  published_at: string | null;
}

export interface BlogListResponse {
  items: BlogListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface BlogCreateRequest {
  title: string;
  content: string;
  excerpt?: string;
  status?: BlogStatus;
  tags?: string[];
}

export interface BlogUpdateRequest {
  title?: string;
  content?: string;
  excerpt?: string;
  status?: BlogStatus;
  tags?: string[];
}

// Newsletter Types
export type SubscriberStatus = 'active' | 'unsubscribed';
export type NewsletterStatus = 'draft' | 'sent' | 'scheduled';

export interface Subscriber {
  id: number;
  email: string;
  status: SubscriberStatus;
  subscribed_at: string;
  unsubscribed_at: string | null;
}

export interface SubscriberCreateRequest {
  email: string;
}

export interface SubscriptionStatus {
  subscribed: boolean;
  email: string;
  subscribed_at: string | null;
}

export interface Newsletter {
  id: number;
  title: string;
  content: string;
  status: NewsletterStatus;
  sent_at: string | null;
  sent_count: number;
  created_at: string;
  updated_at: string;
}

export interface NewsletterListItem {
  id: number;
  title: string;
  status: NewsletterStatus;
  sent_at: string | null;
  sent_count: number;
  created_at: string;
}

export interface NewsletterListResponse {
  items: NewsletterListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface NewsletterCreateRequest {
  title: string;
  content: string;
}

export interface NewsletterSendRequest {
  newsletter_id: number;
}

export interface SubscriberListResponse {
  items: Subscriber[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Project Types
export type ProjectStatus = 'active' | 'in_progress' | 'completed' | 'archived';

export interface Project {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  content: string | null;
  github_url: string | null;
  demo_url: string | null;
  thumbnail_url: string | null;
  tech_stack: string[] | null;
  status: ProjectStatus;
  category: string | null;
  difficulty: string | null;
  view_count: number;
  star_count: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectListItem {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  github_url: string | null;
  demo_url: string | null;
  thumbnail_url: string | null;
  tech_stack: string[] | null;
  status: ProjectStatus;
  category: string | null;
  difficulty: string | null;
  view_count: number;
  star_count: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectListResponse {
  items: ProjectListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ProjectCreateRequest {
  name: string;
  slug: string;
  description?: string;
  content?: string;
  github_url?: string;
  demo_url?: string;
  thumbnail_url?: string;
  tech_stack?: string[];
  status?: ProjectStatus;
  category?: string;
  difficulty?: string;
}

export interface ProjectUpdateRequest {
  name?: string;
  slug?: string;
  description?: string;
  content?: string;
  github_url?: string;
  demo_url?: string;
  thumbnail_url?: string;
  tech_stack?: string[];
  status?: ProjectStatus;
  category?: string;
  difficulty?: string;
}

// API Error Type
export interface APIError {
  detail: string;
}
