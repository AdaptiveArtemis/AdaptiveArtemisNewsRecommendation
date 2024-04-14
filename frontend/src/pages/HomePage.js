import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useLocation } from 'react-router-dom'

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
    console.log('Sending the following data to the backend:', JSON.stringify(dataToSend))
    try {
      // 执行POST请求
      const response = await fetch('http://127.0.0.1:8000/users/user/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prefer_list: selectedPreferences,
          isFirstLogin: false, // 用户已经设置了偏好
        }),
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
  //这里需要改 用户的初始状态是根据token来定的
  const location = useLocation()  // 从 React Router 钩子中获取 location 对象
  const [isFirstLogin, setIsFirstLogin] = useState(
    location.state?.isFirstLogin || true  // 使用 location.state 中的 isFirstLogin 或默认为 true
  )
  const [preferences, setPreferences] = useState([])
  const [recommendations, setRecommendations] = useState([])

  useEffect(() => {
    const fetchUserStatus = async () => {
      if (isFirstLogin) {
        const response = await fakeApiCall()
        setIsFirstLogin(false) // 假设用户完成了首次登录流程，更新状态为 false
        setPreferences(response.preferences)

      }
      fetchRecommendations()  // 获取推荐信息
    }

    fetchUserStatus()
  }, [])

  const fetchRecommendations = async () => {
    try {
      // 执行GET请求
      const response = await fetch('http://127.0.0.1:8000/recommendations', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      if (response.ok) {
        const data = await response.json()  // 解析JSON数据
        setRecommendations(data.recommendations)  // 更新推荐列表状态
      } else {
        console.error('Failed to fetch recommendations:', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    }
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


const fakeApiCall = () => {
  return Promise.resolve({
    //在这里改成token获得的isFirstLogin
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
      { id: 11, name: 'Newsletter' },
      { id: 12, name: 'Innovation for Good' },
      { id: 13, name: 'Education' },
      { id: 14, name: 'Energy' },
      { id: 15, name: 'Health & Medicine' },
      { id: 16, name: 'Sustainability' },
      { id: 17, name: 'Technology' },
      { id: 18, name: 'Video' },
      { id: 19, name: 'Africa & the Middle East' },
      { id: 20, name: 'Asia Pacific' },
      { id: 21, name: 'Europe' },
      { id: 22, name: 'Central and South America' },
      { id: 23, name: 'U.S. & Canada' },
      { id: 24, name: 'Journeys' },
      { id: 25, name: 'Photo Contest' },
      { id: 26, name: 'Instagram' },
    ],
  })
}

export default HomePage
