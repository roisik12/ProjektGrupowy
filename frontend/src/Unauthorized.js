import React from "react";

const Unauthorized = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 animate-fade-in text-center">
      <h1 className="text-3xl sm:text-4xl font-bold text-highlight mb-4">403 Forbidden</h1>
      <p className="text-white text-sm sm:text-lg">Nie masz uprawnień do wyświetlenia tej strony.</p>
    </div>
  );
};

export default Unauthorized;
