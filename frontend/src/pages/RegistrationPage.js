import React, { useState } from 'react';
// import 'bootstrap/dist/css/bootstrap.min.css';

const RegistrationPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords don't match!")
      return
    }
    try {
      const response = await fetch('http://localhost:8000/users/api/register/', {
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
      alert(data.message)
      // Redirect to the login page
      window.location.href = '/login'
    } catch (error) {
      alert("An error occurred while registering the user.")
    }
  }

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-12 col-md-8 col-lg-6">
          <form className="my-5" onSubmit={handleSubmit}>
          <h4 className="mb-3 fw-normal">Welcome to the Daily SciSync! To continue, please register.</h4>
            <div className="form-floating mb-3">
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                className="form-control"
                placeholder="Enter your name"
              />
              <label htmlFor="username">Name</label>
            </div>

            <div className="form-floating mb-3">
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="form-control"
                placeholder="Enter your email"
              />
              <label htmlFor="email">Email address</label>
            </div>

            <div className="form-floating mb-3">
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="form-control"
                placeholder="Create a password"
              />
              <label htmlFor="password">Password</label>
            </div>

            <div className="form-floating mb-3">
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="form-control"
                placeholder="Confirm your password"
              />
              <label htmlFor="confirmPassword">Confirm Password</label>
            </div>

            <button className="w-100 btn btn-lg btn-primary" type="submit">Register</button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default RegistrationPage