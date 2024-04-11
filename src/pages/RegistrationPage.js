import React from 'react'

const RegistrationPage = () => {
  return (
    <div>
      <header>
        {/* Your logo here */}
        <nav>
          {/* Navigation for login can go here */}
        </nav>
      </header>
      <form>
        {/* Form fields for registration */}
        <input type="text" placeholder="name" />
        <input type="email" placeholder="email" />
        <input type="password" placeholder="password" />
        <input type="password" placeholder="confirm password" />
        <button type="submit">Register</button>
      </form>
    </div>
  )
}

export default RegistrationPage
