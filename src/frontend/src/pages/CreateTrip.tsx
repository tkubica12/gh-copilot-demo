import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { tripApiClient } from '../services/tripApiClient';
import { toyApiClient } from '../services/toyApiClient';
import type { TripCreate } from '../types/trip';
import type { Toy } from '../types/toy';

function CreateTrip() {
  const { toyId } = useParams<{ toyId: string }>();
  const navigate = useNavigate();
  
  const [toy, setToy] = useState<Toy | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Form fields
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [locationName, setLocationName] = useState('');
  const [countryCode, setCountryCode] = useState('');
  const [publicTracking, setPublicTracking] = useState(false);

  useEffect(() => {
    if (toyId) {
      loadToy();
    }
  }, [toyId]);

  const loadToy = async () => {
    if (!toyId) return;
    
    try {
      setLoading(true);
      const data = await toyApiClient.getToy(toyId);
      setToy(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load toy');
    } finally {
      setLoading(false);
    }
  };



  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!toyId) return;
    
    // Validation
    if (!title.trim()) {
      alert('Please enter a trip title');
      return;
    }
    
    if (!locationName.trim()) {
      alert('Please enter a destination');
      return;
    }
    
    if (!countryCode.trim() || countryCode.length !== 2) {
      alert('Please enter a valid 2-letter country code (e.g., US, GB, JP)');
      return;
    }
    
    try {
      setSubmitting(true);
      setError(null);
      
      const tripData: TripCreate = {
        toy_id: toyId,
        title: title.trim(),
        description: description.trim() || undefined,
        location_name: locationName.trim(),
        country_code: countryCode.trim().toUpperCase(),
        public_tracking_enabled: publicTracking,
      };
      
      const newTrip = await tripApiClient.createTrip(tripData);
      
      // Navigate to the new trip
      navigate(`/trip/${newTrip.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create trip');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  if (error && !toy) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] gap-4">
        <div className="text-red-600">{error}</div>
        <button
          onClick={() => navigate('/')}
          className="text-blue-600 hover:text-blue-700"
        >
          Back to catalog
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <button
        onClick={() => navigate(`/toy/${toyId}/trips`)}
        className="text-gray-600 hover:text-gray-900 mb-6 flex items-center gap-2"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to trips
      </button>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          Create New Trip for {toy?.name}
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Info */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Trip Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900"
              maxLength={200}
              placeholder="e.g., Summer Adventure in Tokyo"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 min-h-[100px]"
              maxLength={1000}
              placeholder="Describe this trip..."
            />
            <div className="text-xs text-gray-500 mt-1">
              {description.length}/1000 characters
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Destination *
              </label>
              <input
                type="text"
                value={locationName}
                onChange={(e) => setLocationName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900"
                maxLength={200}
                placeholder="e.g., Tokyo"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Country Code *
              </label>
              <input
                type="text"
                value={countryCode}
                onChange={(e) => setCountryCode(e.target.value.toUpperCase())}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900"
                maxLength={2}
                placeholder="e.g., JP"
                required
              />
              <div className="text-xs text-gray-500 mt-1">
                ISO 3166-1 alpha-2 code
              </div>
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="publicTracking"
              checked={publicTracking}
              onChange={(e) => setPublicTracking(e.target.checked)}
              className="h-4 w-4 text-gray-900 focus:ring-gray-900 border-gray-300 rounded"
            />
            <label htmlFor="publicTracking" className="ml-2 block text-sm text-gray-700">
              Enable public location tracking
            </label>
          </div>



          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              {error}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 bg-gray-900 text-white px-6 py-3 rounded-md hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {submitting ? 'Creating Trip...' : 'Create Trip'}
            </button>
            
            <button
              type="button"
              onClick={() => navigate(`/toy/${toyId}/trips`)}
              disabled={submitting}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateTrip;
