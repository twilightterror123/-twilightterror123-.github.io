import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { logout } = useAuth();
  return (
    <div className="flex h-screen bg-twilight-bg">
      <aside className="w-64 bg-twilight-surface border-r border-twilight-border p-4 flex flex-col">
        <h1 className="text-2xl font-bold text-twilight-accent mb-6">✦ Twilight AI</h1>
        <button className="bg-twilight-accent text-white px-4 py-2 rounded mb-4 hover:bg-purple-600 transition">+ Neuer Chat</button>
        <div className="flex-1 overflow-y-auto text-twilight-muted text-sm">
          <p>Chat-Verlauf (Platzhalter)</p>
        </div>
        <button onClick={logout} className="mt-auto text-twilight-muted hover:text-twilight-text transition">Abmelden</button>
      </aside>
      <main className="flex-1 flex flex-col">
        {children}
      </main>
    </div>
  );
};

export default Layout;
