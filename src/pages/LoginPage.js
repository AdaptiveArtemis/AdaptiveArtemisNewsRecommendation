import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

export default function LoginPage () {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      // Replace with your actual login API here
      const response = await fakeLoginAPI(username, password)
      if (response.success) {
        // Login successful, redirect to the user interface
        navigate('/HomePage')
      } else {
        // Login failed, display error message
        alert('Login failed: ' + response.message)
      }
    } catch (error) {
      // Handle request error
      alert('Login request failed')
    }
  }

  // Mock login API function
  const fakeLoginAPI = (username, password) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (username === '1' && password === '1') {
          resolve({ success: true })
        } else {
          resolve({ success: false, message: 'Incorrect username or password' })
        }
      }, 1000)
    })
  }

  return (
    <div className="login-page">
      <div className="login-form">
        <h2>Login</h2>
        <div className="form-group">
          <label htmlFor="username">Username or Email:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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
