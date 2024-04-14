import '../stylesheets/UserProfilePage.css';
import React, {useState, useEffect} from 'react';

export default function ProfilePage() {
    const username = localStorage.getItem('username')
    const [userInfo, setUserInfo] = useState({
        name: 'Name',
        email: 'Email',
    })
    const [articles, setArticles] = useState([
        { "title": 'Article Title 1', "subtitle": 'Sub-title 1', "timestamp": "2024-04-11 19:45:50" },
        { "title": 'Article Title 2', "subtitle": 'Sub-title 2', "timestamp": "2024-04-11 19:45:50" },
        { "title": 'Article Title 3', "subtitle": 'Sub-title 3', "timestamp": "2024-04-11 19:45:50" },
        { "title": 'Article Title 4', "subtitle": 'Sub-title 4', "timestamp": "2024-04-11 19:45:50" },
        { "title": 'Article Title 5', "subtitle": 'Sub-title 5', "timestamp": "2024-04-11 19:45:50" },
    ])
    const [preferences, setPreferences] = useState({
        History: 0.5,
        Art: 0.2,
        Cybersecurity: 0.3,
        Technology: 1,
        Politics: 0.1,
        International: 0.4,
    })

    const getUserData = async () => {
        try {
            // Send a POST request to the backend login endpoint
            const response = await fetch(`http://127.0.0.1:8000/users/user/profile?username=${encodeURIComponent(username)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            })
            const data = await response.json();
            console.log("User data Successfully retrieved from the backend");
            setUserInfo({
                name: data["username"],
                email: data["email"],
            });
            setPreferences(data["preferList"]);
            setArticles(data["recentNewsLogs"])
        } catch {
            alert("There was a problem while contacting the backend to get the user data")
        }
    }

    const clearHistory = () => {
        setArticles([])
    }

    const handlePreferenceChange = (category, value) => {
        setPreferences((prevPreferences) => ({
        ...prevPreferences,
        [category]: value,
        }))
    }

    useEffect(() => {
        getUserData()
    }, [])

    return (
        <div className="profile-page">
            <div className="page-taskbar">
                <div id="logo">Logo</div>
                <div className="page-title">User Profile</div>
            </div>
            <div id="user-info">
                <div id="userName">{userInfo.name}</div>
                <div id="userEmail">{userInfo.email}</div>
            </div>
            <div id="user-details">
                <div id="article-history">
                    <div className="section-heading">
                        <h2>Article Read History</h2>
                        <button onClick={clearHistory}>Clear</button>
                    </div>
                    {articles.map((article, index) => (
                    <div key={index} className="articleItem">
                        <div className="articleTitle">{article.title}</div>
                        <div className="articleTimestamp">{Date(article.timestamp).toLocaleString()}</div>
                    </div>
                    ))}
                </div>
                <div id="category-pref">
                    <div className="section-heading">
                        <h2>Category Preferences</h2>
                    </div>
                    {Object.keys(preferences).map((pref) => (
                    <div key={pref} className="preferenceSlider">
                        <label>{pref}</label>
                        <input
                        type="range"
                        min="0"
                        max="10"
                        value={preferences[pref]*10}
                        onChange={(e) => handlePreferenceChange(pref, e.target.value)}
                        />
                    </div>
                    ))}
                </div>
            </div>
        </div>
    );
}