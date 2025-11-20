import { useState } from 'react';
import { API_CONFIG } from '../../config/apiConfig';

type OperationSummary = {
  toys_processed: number;
  toy_failures: number;
  toy_avatars_uploaded: number;
  trips_processed: number;
  trip_failures: number;
  images_uploaded: number;
};

type ImportResponse = {
  include_toys: boolean;
  include_trips: boolean;
  summary: OperationSummary;
  duration_ms: number;
};

function DemoDataPanel() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ImportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [includeToys, setIncludeToys] = useState(true);
  const [includeTrips, setIncludeTrips] = useState(true);

  const triggerImport = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch(`${API_CONFIG.DEMO_DATA_API_URL}/demo-data/import`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ include_toys: includeToys, include_trips: includeTrips }),
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }
      const data: ImportResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to trigger import');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Demo Data Import</h2>
            <p className="text-sm text-gray-500">Admin-only tooling for reseeding toy & trip data</p>
          </div>
          <div className="flex gap-3 items-center">
            <label className="inline-flex items-center text-sm text-gray-700">
              <input
                type="checkbox"
                className="mr-2"
                checked={includeToys}
                onChange={(e) => setIncludeToys(e.target.checked)}
              />
              Toys
            </label>
            <label className="inline-flex items-center text-sm text-gray-700">
              <input
                type="checkbox"
                className="mr-2"
                checked={includeTrips}
                onChange={(e) => setIncludeTrips(e.target.checked)}
              />
              Trips
            </label>
            <button
              onClick={triggerImport}
              disabled={isLoading || (!includeToys && !includeTrips)}
              className="bg-gray-900 hover:bg-gray-800 text-white px-4 py-2 rounded-lg text-sm font-medium disabled:opacity-50"
            >
              {isLoading ? 'Starting…' : 'Run Import'}
            </button>
          </div>
        </div>

        {error && (
          <div className="mb-4 rounded-lg bg-red-50 text-red-700 px-4 py-3 text-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="border rounded-lg p-4 mt-4">
            <p className="text-sm text-gray-500 mb-2">Last run summary</p>
            <ul className="text-sm text-gray-700 grid gap-1 sm:grid-cols-2">
              <li>Toys processed: {result.summary.toys_processed}</li>
              <li>Trips processed: {result.summary.trips_processed}</li>
              <li>Toy avatars uploaded: {result.summary.toy_avatars_uploaded}</li>
              <li>Gallery images uploaded: {result.summary.images_uploaded}</li>
              <li>Errors (toys): {result.summary.toy_failures}</li>
              <li>Errors (trips): {result.summary.trip_failures}</li>
            </ul>
            <p className="text-xs text-gray-500 mt-3">
              Ran in {(result.duration_ms / 1000).toFixed(1)}s using {result.include_toys ? 'toys' : ''}
              {result.include_toys && result.include_trips ? ' + ' : ''}
              {result.include_trips ? 'trips' : ''} dataset(s)
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

export default DemoDataPanel;
