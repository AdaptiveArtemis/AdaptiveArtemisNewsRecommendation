import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css'

export default function LoginPage () {
  const [email, setEmail] = useState('') // State for storing email
  const [password, setPassword] = useState('') // State for storing password
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      // Send a POST request to the backend login endpoint
      const response = await fetch('http://127.0.0.1:8000/users/api/login/', {
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
        localStorage.setItem('username', data.username)
        navigate('/HomePage')
        // Navigate to the homepage
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
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-12 col-md-8 col-lg-6">
          <form className="my-5" onSubmit={handleLogin}>
            <h4 className="mb-3 fw-normal">Welcome to the Daily SciSync! To continue, please sign in.</h4>
            <div className="form-floating mb-3">
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-control"
                placeholder="Enter your email"
              />
              <label htmlFor="email">Email address</label>
            </div>

            <div className="form-floating mb-3">
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-control"
                placeholder="Enter your password"
              />
              <label htmlFor="password">Password</label>
            </div>

            <button className="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
            <p className="mt-3 text-center">
              Don't have an account? <Link to="/register">Register</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  )
}