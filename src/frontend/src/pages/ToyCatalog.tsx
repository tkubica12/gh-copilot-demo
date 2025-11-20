import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { toyApiClient } from '../services/toyApiClient';
import { tripApiClient } from '../services/tripApiClient';
import type { Toy } from '../types/toy';
import DemoDataPanel from '../components/admin/DemoDataPanel';

function ToyCatalog() {
  const [toys, setToys] = useState<Toy[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [avatarUrls, setAvatarUrls] = useState<Map<string, string>>(new Map());
  const [loadingAvatars, setLoadingAvatars] = useState<Set<string>>(new Set());
  const [loadingTripCounts, setLoadingTripCounts] = useState<Set<string>>(new Set());
  const navigate = useNavigate();
  const observerRef = useRef<IntersectionObserver | null>(null);
  const toysRef = useRef<Toy[]>([]);
  const avatarUrlsRef = useRef<Map<string, string>>(new Map());
  const loadingAvatarsRef = useRef<Set<string>>(new Set());

  // Keep refs in sync with state
  useEffect(() => {
    toysRef.current = toys;
  }, [toys]);

  useEffect(() => {
    avatarUrlsRef.current = avatarUrls;
  }, [avatarUrls]);

  useEffect(() => {
    loadingAvatarsRef.current = loadingAvatars;
  }, [loadingAvatars]);

  const loadAvatar = async (toyId: string) => {
    // Skip if already loaded or loading - use refs for current values
    if (avatarUrlsRef.current.has(toyId) || loadingAvatarsRef.current.has(toyId)) {
      return;
    }

    // Find the toy to check if it has an avatar
    const toy = toysRef.current.find(t => t.id === toyId);
    if (!toy?.avatar_blob_name) {
      return;
    }

    // Mark as loading
    setLoadingAvatars(prev => new Set(prev).add(toyId));

    try {
      const blobUrl = await toyApiClient.getAvatarBlob(toyId);
      setAvatarUrls(prev => new Map(prev).set(toyId, blobUrl));
    } catch (err) {
      console.error(`Failed to load avatar for toy ${toyId}:`, err);
    } finally {
      setLoadingAvatars(prev => {
        const next = new Set(prev);
        next.delete(toyId);
        return next;
      });
    }
  };

  const loadTripCount = async (toyId: string) => {
    // Skip if already loading
    if (loadingTripCounts.has(toyId)) {
      return;
    }

    setLoadingTripCounts(prev => new Set(prev).add(toyId));

    try {
      const count = await tripApiClient.getTripCountByToyId(toyId);
      setToys(prev => {
        // Check if already loaded to avoid race conditions
        const existingToy = prev.find(t => t.id === toyId);
        if (existingToy?.tripCount !== undefined) {
          return prev;
        }
        return prev.map(t => 
          t.id === toyId ? { ...t, tripCount: count } : t
        );
      });
    } catch (err) {
      console.error(`Failed to load trip count for toy ${toyId}:`, err);
      // Set to 0 on error so we don't keep retrying
      setToys(prev => prev.map(t => 
        t.id === toyId ? { ...t, tripCount: 0 } : t
      ));
    } finally {
      setLoadingTripCounts(prev => {
        const next = new Set(prev);
        next.delete(toyId);
        return next;
      });
    }
  };

  const loadToys = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await toyApiClient.getAllToys();
      
      setToys(data);

      // Load trip counts in parallel (non-blocking)
      // Using Promise.allSettled to handle failures gracefully
      const tripCountPromises = data.map(toy => loadTripCount(toy.id));
      Promise.allSettled(tripCountPromises).catch(err => {
        console.error('Error loading trip counts:', err);
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load toys');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadToys();
  }, []);

  // Setup Intersection Observer once
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const toyId = entry.target.getAttribute('data-toy-id');
            if (toyId) {
              loadAvatar(toyId);
              // Stop observing once we've triggered the load
              observer.unobserve(entry.target);
            }
          }
        });
      },
      {
        rootMargin: '50px', // Start loading slightly before entering viewport
        threshold: 0.01,
      }
    );

    observerRef.current = observer;
    
    // Cleanup
    return () => {
      observer.disconnect();
      avatarUrls.forEach(url => URL.revokeObjectURL(url));
    };
  }, []);

  const attachObserver = useCallback((element: HTMLDivElement | null) => {
    if (element && observerRef.current) {
      observerRef.current.observe(element);
    }
  }, []);

  const truncateDescription = (text: string | undefined, maxLength: number = 80) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-gray-600">Loading toys...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900">Toy Catalog</h2>
        <p className="mt-1 text-sm text-gray-600">Browse all available toys</p>
      </div>

      {toys.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">No toys found. You can import the default dataset to get started.</p>
          <DemoDataPanel />
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {toys.map((toy) => {
            const hasAvatar = avatarUrls.has(toy.id);
            const isLoadingAvatar = loadingAvatars.has(toy.id);
            
            return (
              <div
                key={toy.id}
                onClick={() => navigate(`/toy/${toy.id}`)}
                className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer overflow-hidden border border-gray-200"
              >
                <div 
                  ref={attachObserver}
                  data-toy-id={toy.id}
                  className="relative aspect-square bg-gray-100"
                >
                  <div className="absolute top-2 right-2 flex flex-col gap-1 items-end">
                    {toy.tripCount !== undefined ? (
                      <div className="bg-gray-700 text-white text-xs px-2 py-1 rounded-full font-medium shadow-sm flex items-center gap-1">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {toy.tripCount}
                      </div>
                    ) : loadingTripCounts.has(toy.id) ? (
                      <div className="bg-gray-600 text-white text-xs px-2 py-1 rounded-full font-medium shadow-sm animate-pulse">
                        ...
                      </div>
                    ) : null}
                  </div>
                  {hasAvatar ? (
                    <img
                      src={avatarUrls.get(toy.id)}
                      alt={toy.name}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.currentTarget.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="256" height="256"%3E%3Crect width="256" height="256" fill="%23e5e7eb"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="48" fill="%239ca3af"%3E' + toy.name.charAt(0).toUpperCase() + '%3C/text%3E%3C/svg%3E';
                      }}
                    />
                  ) : isLoadingAvatar ? (
                    <div className="w-full h-full flex items-center justify-center">
                      <div className="animate-pulse">
                        <span className="text-sm text-gray-400">Loading...</span>
                      </div>
                    </div>
                  ) : toy.avatar_blob_name ? (
                    <div className="w-full h-full flex items-center justify-center bg-gray-50">
                      <span className="text-6xl text-gray-300 font-medium">
                        {toy.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <span className="text-6xl text-gray-400 font-medium">
                        {toy.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-2 truncate">{toy.name}</h3>
                  <p className="text-sm text-gray-600 line-clamp-2 min-h-[2.5rem]">
                    {truncateDescription(toy.description)}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
      </div>
    </>
  );
}

export default ToyCatalog;
