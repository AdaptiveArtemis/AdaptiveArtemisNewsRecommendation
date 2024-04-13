import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

export default function LoginPage () {
  const [email, setEmail] = useState('') // State for storing email
  const [password, setPassword] = useState('') // State for storing password
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      // Send a POST request to the backend login endpoint
      const response = await fetch('http://127.0.0.1:8000/users/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email, // Use the user-entered email
          password: password // Use the user-entered password
        })
      })

      const data = await response.json()
      if (data.message === "Login successful") {
        // Login successful, take actions based on the backend response
        navigate('/HomePage') // Navigate to the homepage
      } else {
        // Login failed, display an error message
        alert('Login failed: ' + data.message)
      }
    } catch (error) {
      // Request error, display an error message
      alert('Login request failed: ' + error.message)
    }
  }

  return (
    <div className="login-page">
      <div className="login-form">
        <h2>Login</h2>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button onClick={handleLogin}>Login</button>
        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  )
}
