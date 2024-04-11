import React, { useState } from 'react'

const RegistrationPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })

  // Update the state on input change
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: value
    }))
  }

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords don't match!")
      return
    }
    try {
      const response = await fetch('YOUR_BACKEND_API_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password
        }),
      })
      const data = await response.json()
      alert(data.message) // Or handle the response accordingly
    } catch (error) {
      alert("An error occurred while registering the user.")
    }
  }

  return (
    <div className="registration-page">
      <header>
        {/* Your logo here */}
        <nav>
          {/* Navigation for login can go here */}
        </nav>
      </header>
      <form className="registration-form" onSubmit={handleSubmit}>
        <label htmlFor="username">Name:</label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="Enter your name"
        />

        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Enter your email"
        />

        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Create a password"
        />

        <label htmlFor="confirmPassword">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          placeholder="Confirm your password"
        />

        <button type="submit">Register</button>
      </form>
    </div>
  )
}

export default RegistrationPage
