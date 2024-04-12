import '../stylesheets/UserProfilePage.css';
import React, {useState} from 'react';

export default function ProfilePage() {
    
    const [userInfo, setUserInfo] = useState({
        name: 'Name',
        email: 'Email',
    })
    const [articles, setArticles] = useState([
        { title: 'Article Title 1', subtitle: 'Sub-title 1' },
        { title: 'Article Title 2', subtitle: 'Sub-title 2' },
        { title: 'Article Title 3', subtitle: 'Sub-title 3' },
        { title: 'Article Title 4', subtitle: 'Sub-title 4' },
        { title: 'Article Title 5', subtitle: 'Sub-title 5' },
    ])

    const [preferences, setPreferences] = useState({
        History: 5,
        Art: 2,
        Cybersecurity: 3,
        Technology: 10,
        Politics: 1,
        International: 4,
    })

    const clearHistory = () => {
        setArticles([])
    }

    const handlePreferenceChange = (category, value) => {
        setPreferences((prevPreferences) => ({
        ...prevPreferences,
        [category]: value,
        }))
    }

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
                        <div className="articleSubTitle">{article.subtitle}</div>
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
                        value={preferences[pref]}
                        onChange={(e) => handlePreferenceChange(pref, e.target.value)}
                        />
                    </div>
                    ))}
                </div>
            </div>
        </div>
    );
}