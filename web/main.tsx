import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { AgentApp } from './agent/AgentApp';
import './base.css';

createRoot(document.getElementById('root')!).render(<StrictMode><AgentApp /></StrictMode>);
