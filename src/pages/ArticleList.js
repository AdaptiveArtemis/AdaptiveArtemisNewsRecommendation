import React from 'react'

// 静态数据，用于展示
const articles = [
  {
    id: 1,
    title: 'Exploring the React Ecosystem',
    author: 'John Doe',
    excerpt: 'React offers a vast ecosystem to work with. From state management with Redux to styling with Styled-Components, learn how to navigate the sea of options.'
  },
  {
    id: 2,
    title: 'Understanding Functional Components',
    author: 'Jane Smith',
    excerpt: 'Functional components have become the standard for modern React development. Discover the advantages they offer and how to use them effectively.'
  },
  {
    id: 3,
    title: 'Type Safety in React with TypeScript',
    author: 'Emily Johnson',
    excerpt: 'TypeScript brings type safety to JavaScript, reducing bugs and improving the development experience. Learn how to integrate TypeScript in your React projects.'
  },
]

const ArticleList = () => {
  return (
    <div className="article-list">
      {articles.map((article) => (
        <div key={article.id} className="article-summary">
          <h2>{article.title}</h2>
          <p className="author">By {article.author}</p>
          <p>{article.excerpt}</p>
        </div>
      ))}
    </div>
  )
}

export default ArticleList
