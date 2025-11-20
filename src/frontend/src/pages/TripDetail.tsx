import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { tripApiClient } from '../services/tripApiClient';
import { TripStatus } from '../types/trip';
import type { Trip } from '../types/trip';

function TripDetail() {
  const { tripId } = useParams<{ tripId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  
  const [trip, setTrip] = useState<Trip | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [galleryBlobUrls, setGalleryBlobUrls] = useState<Map<string, string>>(new Map());

  useEffect(() => {
    if (tripId) {
      loadTrip();
    }
  }, [tripId]);

  useEffect(() => {
    // Load gallery image blobs when trip changes
    if (trip && tripId) {
      loadGalleryImages();
    }
    
    // Cleanup blob URLs on unmount or when trip changes
    return () => {
      galleryBlobUrls.forEach(url => URL.revokeObjectURL(url));
    };
  }, [trip?.id]);

  const loadTrip = async () => {
    if (!tripId) return;
    
    try {
      setLoading(true);
      setError(null);
      const data = await tripApiClient.getTrip(tripId);
      setTrip(data);
      setEditTitle(data.title);
      setEditDescription(data.description || '');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load trip');
    } finally {
      setLoading(false);
    }
  };

  const loadGalleryImages = async () => {
    if (!trip || !tripId) return;
    
    // Load blob URLs for gallery images (limited to preview, first 6)
    const imagesToLoad = trip.gallery.slice(0, 6);
    const newUrls = new Map<string, string>();
    
    for (const image of imagesToLoad) {
      try {
        const blobUrl = await tripApiClient.getGalleryImageBlob(tripId, image.image_id);
        newUrls.set(image.image_id, blobUrl);
      } catch (err) {
        console.error(`Failed to load gallery image ${image.image_id}:`, err);
      }
    }
    
    setGalleryBlobUrls(newUrls);
  };

  const handleSave = async () => {
    if (!tripId || !trip) return;
    
    try {
      setIsSaving(true);
      await tripApiClient.updateTrip(tripId, {
        title: editTitle,
        description: editDescription || undefined,
      });
      await loadTrip();
      setIsEditing(false);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update trip');
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!tripId || !confirm('Are you sure you want to delete this trip? This will also delete all gallery images.')) return;
    
    try {
      setIsDeleting(true);
      await tripApiClient.deleteTrip(tripId);
      navigate(`/toy/${trip?.toy_id}/trips`);
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete trip');
      setIsDeleting(false);
    }
  };

  const handleStatusChange = async (newStatus: TripStatus) => {
    if (!tripId || !trip) return;
    
    try {
      await tripApiClient.updateTrip(tripId, { status: newStatus });
      await loadTrip();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to update trip status');
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
      <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${badges[status]}`}>
        {labels[status]}
      </span>
    );
  };



  const getCountryFlag = (countryCode: string) => {
    const codePoints = countryCode
      .toUpperCase()
      .split('')
      .map((char) => 127397 + char.charCodeAt(0));
    return String.fromCodePoint(...codePoints);
  };

  // Determine back button destination based on navigation context
  const getBackDestination = () => {
    const searchParams = new URLSearchParams(location.search);
    const fromToy = searchParams.get('from') === 'toy';
    
    if (fromToy && trip) {
      return `/toy/${trip.toy_id}`;
    }
    
    return trip ? `/toy/${trip.toy_id}/trips` : '/';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-gray-600">Loading trip...</div>
      </div>
    );
  }

  if (error || !trip) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] gap-4">
        <div className="text-red-600">{error || 'Trip not found'}</div>
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
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <button
        onClick={() => navigate(getBackDestination())}
        className="text-gray-600 hover:text-gray-900 mb-6 flex items-center gap-2"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to trips
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Trip Header */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            {isEditing ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900"
                    maxLength={200}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={editDescription}
                    onChange={(e) => setEditDescription(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 min-h-[100px]"
                    maxLength={1000}
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={handleSave}
                    disabled={isSaving || !editTitle.trim()}
                    className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-800 disabled:opacity-50"
                  >
                    {isSaving ? 'Saving...' : 'Save'}
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      setEditTitle(trip.title);
                      setEditDescription(trip.description || '');
                    }}
                    disabled={isSaving}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">{trip.title}</h1>
                    <div className="flex items-center gap-3 text-lg text-gray-600">
                      <span className="text-3xl">{getCountryFlag(trip.country_code)}</span>
                      <span>{trip.location_name}</span>
                    </div>
                  </div>
                  {getStatusBadge(trip.status)}
                </div>
                
                {trip.description && (
                  <p className="text-gray-700 whitespace-pre-wrap mb-4">{trip.description}</p>
                )}

                <div className="flex gap-2 pt-4 border-t border-gray-200">
                  <button
                    onClick={() => setIsEditing(true)}
                    className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-800 text-sm"
                  >
                    Edit
                  </button>
                  <button
                    onClick={handleDelete}
                    disabled={isDeleting}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 text-sm disabled:opacity-50"
                  >
                    {isDeleting ? 'Deleting...' : 'Delete Trip'}
                  </button>
                </div>
              </div>
            )}
          </div>



          {/* Gallery Preview */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                Gallery ({trip.gallery.length})
              </h2>
              <button
                onClick={() => navigate(`/trip/${tripId}/gallery`)}
                className="text-gray-600 hover:text-gray-900 text-sm flex items-center gap-1"
              >
                View All
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            {trip.gallery.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <svg className="w-12 h-12 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p>No photos yet</p>
                <button
                  onClick={() => navigate(`/trip/${tripId}/gallery`)}
                  className="mt-3 text-gray-900 hover:text-gray-700 text-sm font-medium"
                >
                  Upload Photos
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {trip.gallery.slice(0, 6).map((image) => {
                  const blobUrl = galleryBlobUrls.get(image.image_id);
                  return (
                    <div
                      key={image.image_id}
                      onClick={() => navigate(`/trip/${tripId}/gallery`)}
                      className="aspect-square bg-gray-100 rounded-lg overflow-hidden cursor-pointer hover:opacity-90 transition-opacity"
                    >
                      {blobUrl ? (
                        <img
                          src={blobUrl}
                          alt={image.caption || 'Gallery image'}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center">
                          <svg className="w-8 h-8 text-gray-400 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                          </svg>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Trip Status */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-3">Trip Status</h3>
            <select
              value={trip.status}
              onChange={(e) => handleStatusChange(e.target.value as TripStatus)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900"
            >
              <option value={TripStatus.PLANNED}>Planned</option>
              <option value={TripStatus.IN_PROGRESS}>In Progress</option>
              <option value={TripStatus.COMPLETED}>Completed</option>
              <option value={TripStatus.CANCELLED}>Cancelled</option>
            </select>
          </div>

          {/* Trip Info */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-3">Trip Info</h3>
            <div className="space-y-3 text-sm">

              <div>
                <span className="text-gray-500">Photos:</span>
                <span className="ml-2 font-medium">{trip.gallery.length}</span>
              </div>
              <div>
                <span className="text-gray-500">Public Tracking:</span>
                <span className="ml-2 font-medium">{trip.public_tracking_enabled ? 'Enabled' : 'Disabled'}</span>
              </div>
              <div>
                <span className="text-gray-500">Created:</span>
                <span className="ml-2">{new Date(trip.created_at).toLocaleDateString()}</span>
              </div>
              <div>
                <span className="text-gray-500">Updated:</span>
                <span className="ml-2">{new Date(trip.updated_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-3">Quick Actions</h3>
            <div className="space-y-2">
              <button
                onClick={() => navigate(`/trip/${tripId}/gallery`)}
                className="w-full px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-800 text-sm"
              >
                View Gallery
              </button>
              <button
                onClick={() => navigate(`/toy/${trip.toy_id}`)}
                className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 text-sm"
              >
                View Toy
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TripDetail;
