import { API_CONFIG } from '../config/apiConfig';
import type { Trip, TripCreate, TripUpdate, TripListResponse } from '../types/trip';

class TripApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_CONFIG.TRIP_SERVICE_BASE_URL;
  }

  private async fetch(url: string, options: RequestInit = {}): Promise<Response> {
    const response = await fetch(url, options);
    return response;
  }

  async createTrip(data: TripCreate): Promise<Trip> {
    const response = await this.fetch(`${this.baseUrl}/trip`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to create trip: ${response.statusText} - ${error}`);
    }

    return response.json();
  }

  async getTrip(id: string): Promise<Trip> {
    const response = await this.fetch(`${this.baseUrl}/trip/${id}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch trip: ${response.statusText}`);
    }

    return response.json();
  }

  async listTrips(params: {
    toy_id?: string;
    owner_oid?: string;
    limit?: number;
    offset?: number;
  }): Promise<TripListResponse> {
    const queryParams = new URLSearchParams();
    
    if (params.toy_id) queryParams.append('toy_id', params.toy_id);
    if (params.owner_oid) queryParams.append('owner_oid', params.owner_oid);
    if (params.limit) queryParams.append('limit', params.limit.toString());
    if (params.offset) queryParams.append('offset', params.offset.toString());

    const response = await this.fetch(`${this.baseUrl}/trip?${queryParams}`);
    
    if (!response.ok) {
      throw new Error(`Failed to list trips: ${response.statusText}`);
    }

    return response.json();
  }

  async updateTrip(id: string, data: TripUpdate): Promise<Trip> {
    const response = await this.fetch(`${this.baseUrl}/trip/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to update trip: ${response.statusText}`);
    }

    return response.json();
  }

  async deleteTrip(id: string): Promise<void> {
    const response = await this.fetch(`${this.baseUrl}/trip/${id}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete trip: ${response.statusText}`);
    }
  }

  async uploadGalleryImage(
    tripId: string,
    file: File,
    metadata?: {

      landmark?: string;
      caption?: string;
    }
  ): Promise<Trip> {
    const formData = new FormData();
    formData.append('file', file);

    const queryParams = new URLSearchParams();

    if (metadata?.landmark) queryParams.append('landmark', metadata.landmark);
    if (metadata?.caption) queryParams.append('caption', metadata.caption);

    const url = `${this.baseUrl}/trip/${tripId}/gallery${queryParams.toString() ? '?' + queryParams.toString() : ''}`;

    const response = await this.fetch(url, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to upload gallery image: ${response.statusText} - ${error}`);
    }

    return response.json();
  }

  getGalleryImageUrl(tripId: string, imageId: string): string {
    return `${this.baseUrl}/trip/${tripId}/gallery/${imageId}`;
  }

  async getGalleryImageBlob(tripId: string, imageId: string): Promise<string> {
    const response = await this.fetch(`${this.baseUrl}/trip/${tripId}/gallery/${imageId}`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch gallery image: ${response.statusText}`);
    }

    const blob = await response.blob();
    return URL.createObjectURL(blob);
  }

  async deleteGalleryImage(tripId: string, imageId: string): Promise<void> {
    const response = await this.fetch(`${this.baseUrl}/trip/${tripId}/gallery/${imageId}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete gallery image: ${response.statusText}`);
    }
  }



  async getTripCountByToyId(toyId: string): Promise<number> {
    try {
      const response = await this.fetch(`${this.baseUrl}/trip?toy_id=${toyId}&limit=1000`);
      
      if (!response.ok) {
        console.error(`Failed to fetch trip count for toy ${toyId}`);
        return 0;
      }

      const data: TripListResponse = await response.json();
      return data.total;
    } catch (error) {
      console.error(`Error fetching trip count for toy ${toyId}:`, error);
      return 0;
    }
  }
}

export const tripApiClient = new TripApiClient();
