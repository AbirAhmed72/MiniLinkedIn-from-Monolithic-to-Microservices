import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/navbarStyles.css';

const Navbar = ({ handleLogout, notifications }) => {
  const [showNotifications, setShowNotifications] = useState(false);

  const toggleNotifications = () => {
    setShowNotifications(!showNotifications);
  };

  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <button onClick={handleLogout}>Logout</button>
          </li>
          <li onClick={toggleNotifications}>
            <span className="notification-icon">🔔</span>
            Notifications ({notifications.length})
            {showNotifications && (
              <div className="notifications-dropdown">
                {notifications.map((notification, index) => (
                  <div key={index} className="notification-item">
                    <p>{notification.notification_text}</p>
                    <p>{notification.notification_datetime}</p>
                  </div>
                ))}
              </div>
            )}
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Navbar;
