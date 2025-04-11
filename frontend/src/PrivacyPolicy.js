import React from 'react';

const PrivacyPolicy = ({ onAccept }) => {
  return (
    <div className="privacy-notice">
      <h3>🔒 Privacy Notice</h3>
      <p>This is a development version of the application. We collect:</p>
      <ul>
        <li>Email addresses for authentication</li>
        <li>Location data for air quality measurements</li>
        <li>Usage data for improving the service</li>
      </ul>
      <button onClick={onAccept}>Accept & Continue</button>
    </div>
  );
};

export default PrivacyPolicy;