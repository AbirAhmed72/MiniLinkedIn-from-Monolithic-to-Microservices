import React from 'react';
import '../styles/notificationStyles.css';

const Notification = ({ notifications }) => {
  const notificationList = Array.isArray(notifications) ? notifications : [];

  const scrollToPost = (postId) => {
    const postElement = document.getElementById(`post-${postId}`);
    if (postElement) {
      postElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="notifications-container">
      <h3 className="notifications-heading">Notifications:</h3>
      {notificationList.length > 0 ? (
        <ul className="notification-list">
          {notificationList.map((notification, index) => (
            <li className="notification-item" key={index} onClick={() => scrollToPost(notification.postId)}>
              <p className="notification-text">{notification.notification_text}</p>
              <p className="notification-datetime">{notification.notification_datetime}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="no-notifications">No new notifications.</p>
      )}
    </div>
  );
};

export default Notification;
