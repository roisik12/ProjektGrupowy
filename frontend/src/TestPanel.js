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
    setResponse(JSON.stringify(data, null, 2));
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
    setResponse(JSON.stringify(data, null, 2));
  };

  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl sm:text-3xl font-semibold text-highlight mb-4">
        🔐 Test Protected Endpoints
      </h2>
      <div className="flex flex-col sm:flex-row gap-4">
        <button
          className="text-sm sm:text-base bg-accent hover:bg-blue-600 text-white py-2 px-4 rounded-lg transition duration-300"
          onClick={handlePost}
        >
          POST air quality
        </button>
        <button
          className="text-sm sm:text-base bg-danger hover:bg-red-700 text-white py-2 px-4 rounded-lg transition duration-300"
          onClick={handleDelete}
        >
          DELETE air quality
        </button>
      </div>
      {response && (
        <pre className="bg-primary text-cyan-100 p-4 rounded-lg mt-4 overflow-x-auto text-sm sm:text-base">
          {response}
        </pre>
      )}
    </div>
  );
};

export default TestPanel;
