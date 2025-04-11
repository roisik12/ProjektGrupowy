import React, { useState } from "react";
import { getToken } from "./firebase";

const TestPanel = () => {
  const [response, setResponse] = useState("");

  const handlePost = async () => {
    const token = await getToken();
    const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/air-quality/TestCity`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        AQI: 123,
        last_update: new Date().toISOString(),
      }),
    });
    const data = await res.json();
    setResponse(JSON.stringify(data));
  };

  const handleDelete = async () => {
    const token = await getToken();
    const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/air-quality/TestCity`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await res.json();
    setResponse(JSON.stringify(data));
  };

  return (
    <div>
      <h2 className="section-header">🔐 Test Protected Endpoints</h2>
      <button className="btn" onClick={handlePost}>POST air quality</button>
      <button className="btn btn-danger" onClick={handleDelete}>DELETE air quality</button>
      <pre>{response}</pre>
    </div>
  );
};

export default TestPanel;
