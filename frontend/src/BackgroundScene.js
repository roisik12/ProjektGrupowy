import React, { useState, useEffect } from "react";

const BackgroundScene = () => {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const generateBuildings = () => {
    const buildingCount = windowWidth < 640 ? 15 : windowWidth < 1024 ? 25 : 30;
    return (
      <div className="flex items-end justify-around h-full">
        {Array.from({ length: buildingCount }).map((_, i) => (
          <div
            key={i}
            className="bg-secondary mx-1 rounded-sm"
            style={{
              width: `${25 + Math.random() * 35}px`,
              height: `${30 + Math.random() * 70}%`,
              opacity: 0.8,
            }}
          ></div>
        ))}
      </div>
    );
  };

  const generateSmog = () => (
    <div className="flex">
      {Array.from({ length: 20 }).map((_, i) => (
        <div
          key={i}
          className="bg-gray-300/20 rounded-full"
          style={{
            position: "absolute",
            top: `${40 + Math.random() * 40}%`,
            left: `${Math.random() * 100}%`,
            width: `${windowWidth < 640 ? 100 + Math.random() * 100 : 150 + Math.random() * 250}px`,
            height: `${4 + Math.random() * 10}px`,
          }}
        ></div>
      ))}
    </div>
  );

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      
      {/* Budynki */}
      <div className={`absolute bottom-0 left-0 flex w-[100vw] ${windowWidth < 640 ? 'h-24' : windowWidth < 1024 ? 'h-36' : 'h-48'}`}>
        <div className="animate-move-buildings w-full h-full absolute">{generateBuildings()}</div>
        <div className="animate-move-buildings w-full h-full absolute right-[-100%]">{generateBuildings()}</div>
      </div>

      {/* Smugi smogu */}
      <div className="absolute bottom-0 left-0 flex w-[100vw] h-full pointer-events-none overflow-hidden">
        <div className="animate-move-smog w-full h-full absolute">{generateSmog()}</div>
        <div className="animate-move-smog w-full h-full absolute right-[-100%]">{generateSmog()}</div>
      </div>

    </div>
  );
};

export default BackgroundScene;
