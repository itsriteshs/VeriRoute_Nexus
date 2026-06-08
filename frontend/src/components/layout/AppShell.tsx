import type { ReactNode } from 'react';
import Sidebar from './Sidebar';
import TopBar from './TopBar';

type AppShellProps = {
  children: ReactNode;
  currentPath: string;
  onNavigate: (path: string) => void;
  demo?: any;
};

export default function AppShell({ children, currentPath, onNavigate, demo }: AppShellProps) {
  return (
    <div className="page-canvas">
      <div className="app-shell">
        <Sidebar currentPath={currentPath} onNavigate={onNavigate} />
        <div className="app-shell__main">
          <TopBar demo={demo} />
          {children}
        </div>
      </div>
    </div>
  );
}
