import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { tripApiClient } from '../services/tripApiClient';
import { toyApiClient } from '../services/toyApiClient';
import type { Trip, TripStatus } from '../types/trip';
import type { Toy } from '../types/toy';

function TripList() {
  const { toyId } = useParams<{ toyId: string }>();
  const navigate = useNavigate();
  
  const [trips, setTrips] = useState<Trip[]>([]);
  const [toy, setToy] = useState<Toy | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (toyId) {
      loadData();
    }
  }, [toyId]);

  const loadData = async () => {
    if (!toyId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      // Load toy and trips in parallel
      const [toyData, tripsData] = await Promise.all([
        toyApiClient.getToy(toyId),
        tripApiClient.listTrips({ toy_id: toyId, limit: 100 }),
      ]);
      
      setToy(toyData);
      setTrips(tripsData.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load trips');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: TripStatus) => {
    const badges = {
      planned: 'bg-blue-100 text-blue-800',
      in_progress: 'bg-green-100 text-green-800',
      completed: 'bg-gray-100 text-gray-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    
    const labels = {
      planned: 'Planned',
      in_progress: 'In Progress',
      completed: 'Completed',
      cancelled: 'Cancelled',
    };
    
    return (
      <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${badges[status]}`}>
        {labels[status]}
      </span>
    );
  };

  const getCountryFlag = (countryCode: string) => {
    // Convert country code to flag emoji
    const codePoints = countryCode
      .toUpperCase()
      .split('')
      .map((char) => 127397 + char.charCodeAt(0));
    return String.fromCodePoint(...codePoints);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-gray-600">Loading trips...</div>
      </div>
    );
  }

  if (error || !toy) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] gap-4">
        <div className="text-red-600">{error || 'Toy not found'}</div>
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
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate(`/toy/${toyId}`)}
          className="text-gray-600 hover:text-gray-900 mb-4 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to {toy.name}
        </button>

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Trips</h1>
            <p className="text-gray-600 mt-1">Adventures for {toy.name}</p>
          </div>
          
          <button
            onClick={() => navigate(`/toy/${toyId}/trip/create`)}
            className="bg-gray-900 text-white px-4 py-2 rounded-lg hover:bg-gray-800 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Trip
          </button>
        </div>
      </div>

      {/* Trips List */}
      {trips.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No trips yet</h2>
          <p className="text-gray-600 mb-6">
            Create the first trip for your toy's adventure!
          </p>
          <button
            onClick={() => navigate(`/toy/${toyId}/trip/create`)}
            className="bg-gray-900 text-white px-6 py-3 rounded-lg hover:bg-gray-800"
          >
            Create First Trip
          </button>
        </div>
      ) : (
        <div className="grid gap-4">
          {trips.map((trip) => (
            <div
              key={trip.id}
              onClick={() => navigate(`/trip/${trip.id}`)}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <h2 className="text-xl font-semibold text-gray-900 truncate">
                      {trip.title}
                    </h2>
                    {getStatusBadge(trip.status)}
                  </div>
                  
                  <div className="flex items-center gap-2 text-gray-600 mb-3">
                    <span className="text-2xl">{getCountryFlag(trip.country_code)}</span>
                    <span className="font-medium">{trip.location_name}</span>
                  </div>
                  
                  {trip.description && (
                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                      {trip.description}
                    </p>
                  )}

                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    
                    {trip.gallery.length > 0 && (
                      <div className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span>{trip.gallery.length} photo{trip.gallery.length !== 1 ? 's' : ''}</span>
                      </div>
                    )}
                    
                    <div className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span>{new Date(trip.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>

                <svg className="w-6 h-6 text-gray-400 flex-shrink-0 ml-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TripList;
