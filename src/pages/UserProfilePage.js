import React, { useState } from 'react'
import '../ProfilePage.css'

const ProfilePage = () => {
  // State for user info
  const [userInfo, setUserInfo] = useState({
    name: 'Name',
    email: 'Email',
  })

  // Handling user info changes
  const handleUserInfoChange = (field, value) => {
    setUserInfo(prevState => ({
      ...prevState,
      [field]: value,
    }))
  }

  // State for articles and preferences
  const [articles, setArticles] = useState([
    // Initial articles data
  ])
  const [preferences, setPreferences] = useState({
    // Initial preferences data
  })

  // Functions to modify articles and preferences
  const clearHistory = () => setArticles([])
  const handlePreferenceChange = (category, value) => {
    setPreferences(prevPreferences => ({
      ...prevPreferences,
      [category]: parseInt(value, 10),
    }))
  }

  return (
    <div className="profile-page">
      <div className="page-taskbar">
        {/* Logo and Page Title */}
      </div>
      <div id="user-info">
        {/* Display and edit user info */}
        <input
          type="text"
          value={userInfo.name}
          onChange={(e) => handleUserInfoChange('name', e.target.value)}
          placeholder="Name"
        />
        <input
          type="email"
          value={userInfo.email}
          onChange={(e) => handleUserInfoChange('email', e.target.value)}
          placeholder="Email"
        />
      </div>
      <div id="user-details">
        {/* Articles and Preferences */}
        <div id="article-history">
          {/* Article history section */}
          {articles.map((article, index) => (
            <div key={index} className="articleItem">
              {/* Article item */}
            </div>
          ))}
          <button onClick={clearHistory}>Clear History</button>
        </div>
        <div id="category-pref">
          {/* Preferences section */}
          {Object.keys(preferences).map((pref) => (
            <div key={pref} className="preferenceSlider">
              <label>{pref}</label>
              <input
                type="range"
                min="0"
                max="10"
                value={preferences[pref]}
                onChange={(e) => handlePreferenceChange(pref, e.target.value)}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
