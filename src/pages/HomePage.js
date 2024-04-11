import React, { useState, useEffect } from 'react'
import ArticleList from './ArticleList'
import { Link } from 'react-router-dom'

// Assumed modal component
const PreferencesModal = ({ preferences, onSave }) => {
  const [selectedPreferences, setSelectedPreferences] = useState([])

  const handleSave = () => {
    onSave(selectedPreferences)
    // Logic to close modal (if your modal component isn't auto-closing)
  }

  return (
    <div className="modal">
      <h2>Choose your preferences</h2>
      <ul>
        {preferences.map((preference) => (
          <li key={preference.id}>
            <input
              type="checkbox"
              checked={selectedPreferences.includes(preference.id)}
              onChange={() => {
                setSelectedPreferences((currentPreferences) =>
                  currentPreferences.includes(preference.id)
                    ? currentPreferences.filter((id) => id !== preference.id)
                    : [...currentPreferences, preference.id]
                )
              }}
            />
            {preference.name}
          </li>
        ))}
      </ul>
      <button onClick={handleSave}>Save Preferences</button>
    </div>
  )
}

const HomePage = () => {
  const [isFirstLogin, setIsFirstLogin] = useState(null) // Null indicates we don't know yet
  const [preferences, setPreferences] = useState([])

  // Simulate fetching user's first login status and preferences list from backend
  useEffect(() => {
    // Assume fetchUserStatus returns { isFirstLogin: boolean, preferences: array }
    const fetchUserStatus = async () => {
      const response = await fakeApiCall()
      setIsFirstLogin(response.isFirstLogin)
      setPreferences(response.preferences)
    }

    fetchUserStatus()
  }, [])

  const savePreferences = (userPreferences) => {
    // Logic to save user preferences
    console.log('Saving user preferences:', userPreferences)
    setIsFirstLogin(false) // Assume the user is no longer first-time login after saving
  }

  // If still loading user information
  if (isFirstLogin === null) {
    return <div>Loading...</div>
  }

  return (
    <div className="homepage">
      <div className="profile-link">
        <Link to="/profile">Profile Settings</Link>
      </div>
      {isFirstLogin ? (
        <PreferencesModal preferences={preferences} onSave={savePreferences} />
      ) : (
        <ArticleList />
      )}
    </div>
  )
}

export default HomePage

// Assumed API call function
const fakeApiCall = () => {
  return Promise.resolve({
    isFirstLogin: true, // Assume user is first-time login
    preferences: [
      { id: 1, name: 'Technology' },
      { id: 2, name: 'Science' },
      // More preferences
    ],
  })
}
