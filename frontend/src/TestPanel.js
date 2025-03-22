import React, { useState } from "react";
import { getToken } from "./firebase";

const TestPanel = () => {
  const [response, setResponse] = useState("");

  const handlePost = async () => {
    const token = await getToken();
    const res = await fetch("http://localhost:8001/air-quality/TestCity", {
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
    const res = await fetch("http://localhost:8001/air-quality/TestCity", {
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
      <h2>🔐 Test Protected Endpoints</h2>
      <button onClick={handlePost}>POST air quality</button>
      <button onClick={handleDelete}>DELETE air quality</button>
      <pre>{response}</pre>
    </div>
  );
};

export default TestPanel;
