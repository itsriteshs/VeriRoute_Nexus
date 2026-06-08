import { type ComponentType, useEffect, useMemo, useState } from 'react';
import AppShell from './components/layout/AppShell.tsx';
import Dashboard from './pages/Dashboard.tsx';
import DemoControlsPage from './pages/DemoControlsPage.tsx';
import DigitalTwinPage from './pages/DigitalTwinPage.tsx';
import ImmuneNetPage from './pages/ImmuneNetPage.tsx';
import LedgerPage from './pages/LedgerPage.tsx';
import ParcelDetails from './pages/ParcelDetails.tsx';
import ParcelsPage from './pages/ParcelsPage.tsx';
import ScanPage from './pages/ScanPage.tsx';
import TrustBoardPage from './pages/TrustBoardPage.tsx';
import { usePacketFlowLiveState, type LiveDemoState } from './hooks/usePacketFlowLiveState.ts';

const routePaths = ['/dashboard', '/digital-twin', '/parcels', '/immunenet', '/trust-board', '/demo-controls', '/ledger'] as const;
type RoutePath = (typeof routePaths)[number];

type RoutedPageProps = {
  demo: LiveDemoState;
};

function normalizePath(pathname: string): string {
  if (pathname === '/') return '/dashboard';
  if (pathname.startsWith('/scan/')) return pathname;
  if (pathname.startsWith('/parcels/')) return pathname;
  return routePaths.includes(pathname as RoutePath) ? pathname : '/dashboard';
}

export default function App() {
  const demo = usePacketFlowLiveState();
  const [currentPath, setCurrentPath] = useState<string>(() => normalizePath(window.location.pathname));
  const routes = useMemo<Record<RoutePath, ComponentType<any>>>(
    () => ({
      '/dashboard': Dashboard,
      '/digital-twin': DigitalTwinPage,
      '/parcels': ParcelsPage,
      '/immunenet': ImmuneNetPage,
      '/trust-board': TrustBoardPage,
      '/demo-controls': DemoControlsPage,
      '/ledger': LedgerPage,
    }),
    [],
  );

  useEffect(() => {
    const onPopState = () => setCurrentPath(normalizePath(window.location.pathname));
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  function navigate(path: string) {
    const nextPath = normalizePath(path);
    if (nextPath !== currentPath) {
      window.history.pushState({}, '', nextPath);
      setCurrentPath(nextPath);
    }
  }

  const Page = routes[currentPath as RoutePath];
  const pathParts = currentPath.split('/').filter(Boolean);

  let content = Page ? <Page demo={demo} /> : <Dashboard demo={demo} />;
  if (currentPath.startsWith('/scan/')) {
    content = <ScanPage hubId={pathParts[1]} />;
  } else if (currentPath.startsWith('/parcels/')) {
    content = <ParcelDetails parcelId={pathParts[1]} />;
  }

  return (
    <AppShell currentPath={currentPath} onNavigate={navigate} demo={demo}>
      {content}
    </AppShell>
  );
}
