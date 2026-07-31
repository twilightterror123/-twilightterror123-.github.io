import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

const Register: React.FC = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await register(email, username, password);
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-twilight-bg">
      <div className="bg-twilight-surface p-8 rounded-lg shadow-xl w-full max-w-md border border-twilight-border">
        <h1 className="text-2xl font-bold mb-6 text-twilight-text">Registrieren</h1>
        <form onSubmit={handleSubmit}>
          <input type="email" placeholder="E-Mail" className="w-full p-2 mb-4 bg-twilight-bg border border-twilight-border rounded text-twilight-text" value={email} onChange={e => setEmail(e.target.value)} required />
          <input type="text" placeholder="Benutzername" className="w-full p-2 mb-4 bg-twilight-bg border border-twilight-border rounded text-twilight-text" value={username} onChange={e => setUsername(e.target.value)} required />
          <input type="password" placeholder="Passwort" className="w-full p-2 mb-4 bg-twilight-bg border border-twilight-border rounded text-twilight-text" value={password} onChange={e => setPassword(e.target.value)} required />
          <button type="submit" className="w-full bg-twilight-accent text-white py-2 rounded hover:bg-purple-600 transition">Registrieren</button>
        </form>
        <p className="mt-4 text-twilight-muted text-sm">Bereits Konto? <Link to="/login" className="text-twilight-accent">Anmelden</Link></p>
      </div>
    </div>
  );
};

export default Register;
