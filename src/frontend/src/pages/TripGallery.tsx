import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { tripApiClient } from '../services/tripApiClient';
import type { Trip, GalleryImage } from '../types/trip';

function TripGallery() {
  const { tripId } = useParams<{ tripId: string }>();
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [trip, setTrip] = useState<Trip | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [selectedImage, setSelectedImage] = useState<GalleryImage | null>(null);
  const [galleryBlobUrls, setGalleryBlobUrls] = useState<Map<string, string>>(new Map());
  const [loadingImages, setLoadingImages] = useState<Set<string>>(new Set());
  
  // Upload form state
  const [uploadLandmark, setUploadLandmark] = useState('');
  const [uploadCaption, setUploadCaption] = useState('');

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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load trip');
    } finally {
      setLoading(false);
    }
  };

  const loadGalleryImages = async () => {
    if (!trip || !tripId) return;
    
    // Load blob URLs for all gallery images
    const newUrls = new Map<string, string>();
    const loading = new Set<string>();
    
    for (const image of trip.gallery) {
      loading.add(image.image_id);
    }
    setLoadingImages(loading);
    
    for (const image of trip.gallery) {
      try {
        const blobUrl = await tripApiClient.getGalleryImageBlob(tripId, image.image_id);
        newUrls.set(image.image_id, blobUrl);
      } catch (err) {
        console.error(`Failed to load gallery image ${image.image_id}:`, err);
      } finally {
        setLoadingImages(prev => {
          const next = new Set(prev);
          next.delete(image.image_id);
          return next;
        });
      }
    }
    
    setGalleryBlobUrls(newUrls);
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!tripId || !e.target.files || e.target.files.length === 0) return;
    
    const file = e.target.files[0];
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB');
      return;
    }
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('File must be an image');
      return;
    }
    
    try {
      setUploading(true);
      
      const metadata: any = {};
      if (uploadLandmark.trim()) metadata.landmark = uploadLandmark.trim();
      if (uploadCaption.trim()) metadata.caption = uploadCaption.trim();
      
      await tripApiClient.uploadGalleryImage(tripId, file, metadata);
      
      // Reset form
      setUploadLandmark('');
      setUploadCaption('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      
      await loadTrip();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to upload image');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteImage = async (imageId: string) => {
    if (!tripId || !confirm('Are you sure you want to delete this image?')) return;
    
    try {
      await tripApiClient.deleteGalleryImage(tripId, imageId);
      setSelectedImage(null);
      await loadTrip();
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Failed to delete image');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-gray-600">Loading gallery...</div>
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <button
        onClick={() => navigate(`/trip/${tripId}`)}
        className="text-gray-600 hover:text-gray-900 mb-6 flex items-center gap-2"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Back to trip
      </button>

      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Gallery</h1>
        <p className="text-gray-600 mt-1">{trip.title}</p>
      </div>

      {/* Upload Form */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Upload Photo</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Select Image
            </label>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              disabled={uploading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 disabled:opacity-50"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Landmark (Optional)
            </label>
            <input
              type="text"
              value={uploadLandmark}
              onChange={(e) => setUploadLandmark(e.target.value)}
              disabled={uploading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 disabled:opacity-50"
              maxLength={200}
              placeholder="e.g., Eiffel Tower"
            />
          </div>
        </div>
        
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Caption (Optional)
          </label>
          <input
            type="text"
            value={uploadCaption}
            onChange={(e) => setUploadCaption(e.target.value)}
            disabled={uploading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-900 disabled:opacity-50"
            maxLength={500}
            placeholder="Add a caption..."
          />
        </div>
        
        {uploading && (
          <div className="mt-4 text-sm text-gray-600">
            Uploading...
          </div>
        )}
      </div>

      {/* Gallery Grid */}
      {trip.gallery.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No photos yet</h2>
          <p className="text-gray-600">
            Upload the first photo using the form above
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {trip.gallery.map((image) => {
            const blobUrl = galleryBlobUrls.get(image.image_id);
            const isLoading = loadingImages.has(image.image_id);
            
            return (
              <div
                key={image.image_id}
                onClick={() => !isLoading && setSelectedImage(image)}
                className="aspect-square bg-gray-100 rounded-lg overflow-hidden cursor-pointer hover:opacity-90 transition-opacity relative group"
              >
                {isLoading ? (
                  <div className="w-full h-full flex items-center justify-center">
                    <svg className="w-8 h-8 text-gray-400 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </div>
                ) : blobUrl ? (
                  <img
                    src={blobUrl}
                    alt={image.caption || 'Gallery image'}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400">
                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                )}
              
                {/* Overlay with info */}
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all flex items-end p-3">
                  <div className="text-white text-xs opacity-0 group-hover:opacity-100 transition-opacity">
                    {image.landmark && <div className="font-medium">{image.landmark}</div>}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Image Modal */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedImage(null)}
        >
          <button
            onClick={() => setSelectedImage(null)}
            className="absolute top-4 right-4 text-white hover:text-gray-300 z-10"
          >
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <div
            className="max-w-5xl w-full"
            onClick={(e) => e.stopPropagation()}
          >
            {galleryBlobUrls.get(selectedImage.image_id) ? (
              <img
                src={galleryBlobUrls.get(selectedImage.image_id)}
                alt={selectedImage.caption || 'Gallery image'}
                className="w-full h-auto max-h-[80vh] object-contain rounded-lg"
              />
            ) : (
              <div className="w-full h-96 bg-gray-800 rounded-lg flex items-center justify-center">
                <svg className="w-16 h-16 text-gray-400 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
            )}
            
            <div className="bg-white rounded-lg p-6 mt-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  {selectedImage.landmark && (
                    <div className="mb-2">
                      <span className="text-sm font-medium text-gray-700">Landmark:</span>
                      <p className="text-gray-900">{selectedImage.landmark}</p>
                    </div>
                  )}
                  
                  {selectedImage.caption && (
                    <div className="mb-2">
                      <span className="text-sm font-medium text-gray-700">Caption:</span>
                      <p className="text-gray-900">{selectedImage.caption}</p>
                    </div>
                  )}
                  

                </div>
                
                <div className="text-sm text-gray-600">
                  <div className="mb-2">
                    <span className="font-medium">Source:</span> {selectedImage.source}
                  </div>
                  <div className="mb-2">
                    <span className="font-medium">Uploaded:</span> {new Date(selectedImage.uploaded_at).toLocaleString()}
                  </div>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <button
                  onClick={() => handleDeleteImage(selectedImage.image_id)}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
                >
                  Delete Image
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default TripGallery;
