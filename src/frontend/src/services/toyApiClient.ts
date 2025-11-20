import { API_CONFIG } from '../config/apiConfig';
import type { Toy, CreateToyRequest, UpdateToyRequest } from '../types/toy';

class ToyApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_CONFIG.TOY_SERVICE_BASE_URL;
  }

  private async fetch(url: string, options: RequestInit = {}): Promise<Response> {
    const response = await fetch(url, options);
    return response;
  }

  async getAllToys(): Promise<Toy[]> {
    // Fetch with high limit to get all toys (backend default is 20)
    // TODO: Implement proper pagination if catalog grows large
    const response = await this.fetch(`${this.baseUrl}/toy?limit=1000`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch toys: ${response.statusText}`);
    }

    const data = await response.json();
    // Backend returns paginated response: {items: [...], total: number, limit: number, offset: number}
    return data.items || [];
  }

  async getToy(id: string): Promise<Toy> {
    const response = await this.fetch(`${this.baseUrl}/toy/${id}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch toy: ${response.statusText}`);
    }

    return response.json();
  }

  async createToy(data: CreateToyRequest): Promise<Toy> {
    const response = await this.fetch(`${this.baseUrl}/toy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to create toy: ${response.statusText}`);
    }

    return response.json();
  }

  async updateToy(id: string, data: UpdateToyRequest): Promise<Toy> {
    const response = await this.fetch(`${this.baseUrl}/toy/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to update toy: ${response.statusText}`);
    }

    return response.json();
  }

  async deleteToy(id: string): Promise<void> {
    const response = await this.fetch(`${this.baseUrl}/toy/${id}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete toy: ${response.statusText}`);
    }
  }

  async uploadAvatar(id: string, file: File): Promise<void> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.fetch(`${this.baseUrl}/toy/${id}/avatar`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error(`Failed to upload avatar: ${response.statusText}`);
    }
  }

  async deleteAvatar(id: string): Promise<void> {
    const response = await this.fetch(`${this.baseUrl}/toy/${id}/avatar`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete avatar: ${response.statusText}`);
    }
  }

  async getAvatarBlob(id: string): Promise<string> {
    const response = await this.fetch(`${this.baseUrl}/toy/${id}/avatar`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch avatar: ${response.statusText}`);
    }

    const blob = await response.blob();
    return URL.createObjectURL(blob);
  }

  getAvatarUrl(id: string): string {
    return `${this.baseUrl}/toy/${id}/avatar`;
  }
}

export const toyApiClient = new ToyApiClient();
