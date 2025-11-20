import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from '../components/Layout';
import ToyCatalog from '../pages/ToyCatalog';
import ToyDetail from '../pages/ToyDetail';
import TripList from '../pages/TripList';
import CreateTrip from '../pages/CreateTrip';
import TripDetail from '../pages/TripDetail';
import TripGallery from '../pages/TripGallery';

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<ToyCatalog />} />
        <Route path="toy/:id" element={<ToyDetail />} />
        <Route path="toy/:toyId/trips" element={<TripList />} />
        <Route path="toy/:toyId/trip/create" element={<CreateTrip />} />
        <Route path="trip/:tripId" element={<TripDetail />} />
        <Route path="trip/:tripId/gallery" element={<TripGallery />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
