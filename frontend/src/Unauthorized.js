import React from "react";

const Unauthorized = () => {
  return (
    <div className="container fade-in" style={{ marginTop: '5rem', textAlign: 'center' }}>
      <h1 className="section-header">403 Forbidden</h1>
      <p>Nie masz uprawnień do wyświetlenia tej strony.</p>
    </div>
  );
};

export default Unauthorized;