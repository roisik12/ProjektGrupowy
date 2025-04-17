// CityBackground.js
import React, { useEffect, useState } from "react";
import "./cityBackground.css";

/** 
 * Komponent tła:
 * 1) .city-background -> pełny ekran w tle (gradient nieba).
 * 2) .buildings -> kilka budynków, w building: okna (window).
 * 3) Losowo zapala/gasi okna co 5s.
 * 4) .wind -> animowany pas wiatru nad budynkami.
 */
function CityBackground() {
  // Zdefiniuj sobie liczbę budynków i liczbę okien w każdym:
  // Na przykład 3 budynki, o 15, 20 i 10 oknach:
  const windowsPerBuilding = [15, 20, 10];

  // Stan: litWindows[i][j] => czy w budynku i okno j jest zapalone
  const [litWindows, setLitWindows] = useState(
    windowsPerBuilding.map(num => Array(num).fill(false))
  );

  useEffect(() => {
    // Co 5 sek. losowo toggluj parę okien
    const interval = setInterval(() => {
      setLitWindows(current => {
        // Kopiujemy tablicę
        const newState = current.map(arr => [...arr]);

        newState.forEach((buildingArr, buildingIndex) => {
          // Ile okien togglujemy? 1/4 okien w tym budynku
          const howMany = Math.floor(buildingArr.length / 4);
          for (let i = 0; i < howMany; i++) {
            const randIndex = Math.floor(Math.random() * buildingArr.length);
            newState[buildingIndex][randIndex] = !newState[buildingIndex][randIndex];
          }
        });

        return newState;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="city-background">
      {/* Budynki */}
      <div className="buildings">
        {litWindows.map((buildingWindows, buildingIndex) => (
          <div key={buildingIndex} className="building">
            {buildingWindows.map((isLit, windowIndex) => (
              <div 
                key={windowIndex} 
                className={`window ${isLit ? 'lit' : ''}`} 
              />
            ))}
          </div>
        ))}
      </div>

      {/* Wiatr ponad budynkami */}
      <div className="wind"></div>
    </div>
  );
}

export default CityBackground;
