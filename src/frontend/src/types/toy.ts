export interface Toy {
  id: string;
  owner_oid: string;
  name: string;
  description?: string;
  avatar_blob_name?: string;
  created_at: string;
  updated_at: string;
  tripCount?: number; // Loaded asynchronously from trip service
}

export interface CreateToyRequest {
  name: string;
  description?: string;
}

export interface UpdateToyRequest {
  name?: string;
  description?: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    correlation_id?: string;
    details?: unknown[];
  };
}
