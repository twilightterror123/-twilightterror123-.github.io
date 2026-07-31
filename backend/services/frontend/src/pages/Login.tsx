import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-twilight-bg">
      <div className="bg-twilight-surface p-8 rounded-lg shadow-xl w-full max-w-md border border-twilight-border">
        <h1 className="text-2xl font-bold mb-6 text-twilight-text">Anmelden</h1>
        <form onSubmit={handleSubmit}>
          <input type="email" placeholder="E-Mail" className="w-full p-2 mb-4 bg-twilight-bg border border-twilight-border rounded text-twilight-text" value={email} onChange={e => setEmail(e.target.value)} required />
          <input type="password" placeholder="Passwort" className="w-full p-2 mb-4 bg-twilight-bg border border-twilight-border rounded text-twilight-text" value={password} onChange={e => setPassword(e.target.value)} required />
          <button type="submit" className="w-full bg-twilight-accent text-white py-2 rounded hover:bg-purple-600 transition">Anmelden</button>
        </form>
        <p className="mt-4 text-twilight-muted text-sm">Noch kein Konto? <Link to="/register" className="text-twilight-accent">Registrieren</Link></p>
      </div>
    </div>
  );
};

export default Login;
