import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import '../styles/homePageStyles.css';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = 'http://127.0.0.1:8001/api/v1'; // Replace with your actual backend API base URL
const API_BASE_URL_2 = 'http://127.0.0.1:8002/api/v1';

const HomePage = () => {
  const [posts, setPosts] = useState([]);
  const [loggedIn, setLoggedIn] = useState(false);
  const [postText, setPostText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const postsElements = useRef([]);
  const navigate = useNavigate();

  useEffect(() => {
    const access_token = localStorage.getItem('access_token');
    if (access_token) {
      setLoggedIn(true);
      fetchPosts(access_token);
    }
  }, []);

  const fetchPosts = (access_token) => {
    axios
      .get(`${API_BASE_URL}/post`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      .then((response) => {
        setPosts(response.data);
      })
      .catch((error) => {
        console.error('Error fetching posts:', error);
      });
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  const handlePostTextChange = (event) => {
    setPostText(event.target.value);
  };

  const handleImageChange = (event) => {
    setSelectedImage(event.target.files[0]);
  };

  const handleSubmitPost = async () => {
    const formData = new FormData();
    formData.append('post_text', postText);
    if (selectedImage) {
      formData.append('image', selectedImage, selectedImage.name);
    }

    const access_token = localStorage.getItem('access_token');

    try {
      await axios.post(`${API_BASE_URL}/post`, formData, {
        headers: {
          Authorization: `Bearer ${access_token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      fetchPosts(access_token);
      setPostText('');
      setSelectedImage(null);
    } catch (error) {
      console.error('Error submitting post:', error.response);
    }
  };

  const scrollToPost = (postId) => {
    const postElement = postsElements.current.find((element) => element.id === `post-${postId}`);
    if (postElement) {
      postElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleFetchNotifications = () => {
    const access_token = localStorage.getItem('access_token');
    axios
      .get(`${API_BASE_URL_2}/notification`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      .then((response) => {
        setNotifications(response.data);
      })
      .catch((error) => {
        console.error('Error fetching notifications:', error);
      });
  };

  return (
    <div className="container">
      {loggedIn ? (
        <div className="content">
          <h2>Welcome to Your Home Page</h2>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
          <div className="new-post">
            <h3>Create a New Post</h3>
            <textarea
              rows={4}
              cols={50}
              value={postText}
              onChange={handlePostTextChange}
              placeholder="Enter your post text"
            />
            <input type="file" onChange={handleImageChange} />
            <button className="submit-button" onClick={handleSubmitPost}>
              Submit Post
            </button>
          </div>
          <div className="posts">
            {posts.length > 0 ? (
              <div>
                <h3>What's New:</h3>
                {posts.map((post) => (
                  <div className="post" id={`post-${post.pid}`} ref={(ref) => postsElements.current.push(ref)} key={post.pid}>
                    <p className="username">{post.username}</p>
                    <p className="post-text">{post.post_text}</p>
                    {post.image_url && <img src={post.image_url} alt="Post" className="post-image" />}
                  </div>
                ))}
              </div>
            ) : (
              <p>No posts available.</p>
            )}
          </div>
          <div className="notifications-container">
            <button className="notification-button" onClick={handleFetchNotifications}>
              Fetch Notifications
            </button>
            {notifications.length > 0 ? (
            <div className="notification-list">
              <h3 className="notifications-heading">Notifications ({notifications.length})</h3>
                <ul className="notification-list-ul">
                {notifications.map((notification, index) => (
                  <li className="notification-item" key={index} onClick={() => scrollToPost(notification.postId)}>
                      <p className="notification-text">{notification.notification_text}</p>
                      <p className="notification-datetime">{notification.notification_datetime}</p>
                  </li>
              ))}
                </ul>
            </div>
            ) : (
                <p className="no-notifications">No new notifications available</p>
            )}
          </div>
        </div>
      ) : (
        <p>Please log in to view this page.</p>
      )}
    </div>
  );
};

export default HomePage;
