import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

// Preferences Modal Component
const PreferencesModal = ({ preferences, onSave }) => {
  const [selectedPreferences, setSelectedPreferences] = useState([])

  const handleSave = async () => {
    // 构建要发送的数据
    const dataToSend = {
      prefer_list: selectedPreferences.map(id =>
          preferences.find(preference => preference.id === id).name
      )
    }

    try {
      // 执行POST请求
      const response = await fetch('http://127.0.0.1:8000/users/user/update/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend)
      })

      if (response.ok) {
        const responseData = await response.json()
        console.log('Preferences saved:', responseData)
        onSave(selectedPreferences)
      } else {
        console.error('Failed to save preferences:', response.statusText)
      }
    } catch (error) {
      console.error('Error saving preferences:', error)
    }
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

// Recommendations List Component
const RecommendationsList = ({ articles }) => {
  return (
      <div>
        <h2>Recommended Articles</h2>
        {articles.length > 0 ? (
            <ul>
              {articles.map(article => (
                  <li key={article.title}>
                    <a href={article.link} target="_blank" rel="noopener noreferrer">
                      <h3>{article.title}</h3>
                      <p>{article.subtitle}</p>
                    </a>
                  </li>
              ))}
            </ul>
        ) : (
            <p>No recommendations available.</p>
        )}
      </div>
  )
}

// Home Page Component
const HomePage = () => {
  const [isFirstLogin, setIsFirstLogin] = useState(true)
  const [preferences, setPreferences] = useState([])
  const [recommendations, setRecommendations] = useState([])

  useEffect(() => {
    const fetchUserStatus = async () => {
      const response = await fakeApiCall()
      setIsFirstLogin(response.isFirstLogin)
      setPreferences(response.preferences)
      fetchRecommendations()  // Fetch recommendations on user login
    }

    fetchUserStatus()
  }, [])

  const fetchRecommendations = async () => {
    // 使用静态数据模拟API调用
    const data = {
      recommendations: [
        { title: "The Real Science Behind the Megalodon", subtitle: "As The Meg hits theaters, dive into what we really know about this chompy predator", link: "https://www.smithsonianmag.com/articles/real-science-megalodon-180969860/", relevant_keyword: null },
        { title: "The Forgotten Sisters Behind 'Happy Birthday to You'", subtitle: "Mildred and Patty Hill wrote the popular song's melody, but their contributions to American culture have long been overlooked", link: "https://www.smithsonianmag.com/history/the-forgotten-sisters-behind-happy-birthday-to-you-180983885/", relevant_keyword: null },
        // More articles
      ]
    }
    setRecommendations(data.recommendations)
  }


  const savePreferences = (userPreferences) => {
    console.log('Saving user preferences:', userPreferences)
    setIsFirstLogin(false)
  }

  if (isFirstLogin === null) {
    return <div>Loading...</div>
  }

  return (
      <div className="homepage">
        <div className="profile-link">
          <Link to="/profile">Profile Settings</Link>
        </div>
        {isFirstLogin === null ? (
            <div>Loading...</div>
        ) : isFirstLogin ? (
            <PreferencesModal preferences={preferences} onSave={savePreferences} />
        ) : (
            <RecommendationsList articles={recommendations} />
        )}
      </div>
  )
}

// Assumed API call function
const fakeApiCall = () => {
  return Promise.resolve({
    isFirstLogin: true,  // Assume this dynamically changes based on actual user status
    preferences: [
      { id: 1, name: 'History' },
      { id: 2, name: 'Science' },
      { id: 3, name: 'Innovation' },
      { id: 4, name: 'Arts & Culture' },
      { id: 5, name: 'Travel' },
      { id: 6, name: 'Human Behavior' },
      { id: 7, name: 'Mind & Body' },
      { id: 8, name: 'Our Planet' },
      { id: 9, name: 'Space' },
      { id: 10, name: 'Wildlife' },
      { id: 11, name: 'Newsletter' }, // You might want to consider if 'Newsletter' is a preference category like the others
      { id: 12, name: 'Innovation for Good' },
      { id: 13, name: 'Education' },
      { id: 14, name: 'Energy' },
      { id: 15, name: 'Health & Medicine' },
      { id: 16, name: 'Sustainability' },
      { id: 17, name: 'Technology' }, // This is repeated since 'Technology' is also mentioned earlier in your list
      { id: 18, name: 'Video' },
      // Assuming 'Newsletter' here is the same as the one above, you may not need to repeat it
      { id: 19, name: 'Africa & the Middle East' },
      { id: 20, name: 'Asia Pacific' },
      { id: 21, name: 'Europe' },
      { id: 22, name: 'Central and South America' },
      { id: 23, name: 'U.S. & Canada' },
      { id: 24, name: 'Journeys' },
      // 'Newsletter' would be repeated here again if it's considered a separate category
      { id: 25, name: 'Photo Contest' },
      { id: 26, name: 'Instagram' }, // 'Instagram' might be a link to a social media page rather than a content category
      // More preferences
    ],

  })
}

export default HomePage
