import { type ComponentType, useEffect, useMemo, useState } from 'react';
import AppShell from './components/layout/AppShell.tsx';
import Dashboard from './pages/Dashboard.tsx';
import DemoControlsPage from './pages/DemoControlsPage.tsx';
import DigitalTwinPage from './pages/DigitalTwinPage.tsx';
import ImmuneNetPage from './pages/ImmuneNetPage.tsx';
import ParcelsPage from './pages/ParcelsPage.tsx';
import TrustBoardPage from './pages/TrustBoardPage.tsx';
import { useDemoState, type DemoState } from './hooks/useDemoState.ts';

const routePaths = ['/dashboard', '/digital-twin', '/parcels', '/immunenet', '/trust-board', '/demo-controls'] as const;
type RoutePath = (typeof routePaths)[number];

type RoutedPageProps = {
  demo: DemoState;
};

function normalizePath(pathname: string): RoutePath {
  if (pathname === '/') return '/dashboard';
  return routePaths.includes(pathname as RoutePath) ? (pathname as RoutePath) : '/dashboard';
}

export default function App() {
  const demo = useDemoState();
  const [currentPath, setCurrentPath] = useState<RoutePath>(() => normalizePath(window.location.pathname));
  const routes = useMemo<Record<RoutePath, ComponentType<RoutedPageProps>>>(
    () => ({
      '/dashboard': Dashboard,
      '/digital-twin': DigitalTwinPage,
      '/parcels': ParcelsPage,
      '/immunenet': ImmuneNetPage,
      '/trust-board': TrustBoardPage,
      '/demo-controls': DemoControlsPage,
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

  const Page = routes[currentPath];

  return (
    <AppShell currentPath={currentPath} onNavigate={navigate}>
      <Page demo={demo} />
    </AppShell>
  );
}
