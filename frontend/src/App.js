import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import RegistrationPage from './pages/RegistrationPage'
import LoginPage from './pages/LoginPage'
import HomePage from './pages/HomePage'
import UserProfilePage from './pages/UserProfilePage'

function App () {
  return (
    <Router>
      <div>
        <nav>
        </nav>
        <Routes>
          <Route path="/register" element={<RegistrationPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<LoginPage />} />
          <Route path="/HomePage" element={<HomePage />} />
          <Route path="/profile" element={<UserProfilePage />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
