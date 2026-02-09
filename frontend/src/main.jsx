import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import "./reusableComponents/root.css";


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

//This was auto created by react when setting up project - it boostraps jsx into the index.html, I don't think we need to change it