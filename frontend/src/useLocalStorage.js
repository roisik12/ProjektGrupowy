import { useState, useEffect } from 'react';

function useLocalStorage(key, defaultValue) {
  const [value, setValue] = useState(() => {
    const storedValue = localStorage.getItem(key);
    return storedValue === null ? defaultValue : storedValue;
  });

  useEffect(() => {
    const handleStorageChange = () => {
      const storedValue = localStorage.getItem(key);
      setValue(storedValue === null ? defaultValue : storedValue);
    };

    // Add event listener for 'storage' event
    window.addEventListener('storage', handleStorageChange);

    return () => {
      // Remove event listener on cleanup
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key, defaultValue]);

  const setLocalStorageValue = (newValue) => {
    localStorage.setItem(key, newValue);
    setValue(newValue);
  };

  return [value, setLocalStorageValue];
}

export default useLocalStorage;