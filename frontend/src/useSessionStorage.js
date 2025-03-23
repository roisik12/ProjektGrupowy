import { useState, useEffect } from 'react';

function useSessionStorage(key, defaultValue) {
  const [value, setValue] = useState(() => {
    const storedValue = sessionStorage.getItem(key);
    return storedValue === null ? defaultValue : storedValue;
  });

  useEffect(() => {
    const handleStorageChange = () => {
      const storedValue = sessionStorage.getItem(key);
      setValue(storedValue === null ? defaultValue : storedValue);
    };

    window.addEventListener('storage', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [key, defaultValue]);

  const setSessionStorageValue = (newValue) => {
    sessionStorage.setItem(key, newValue);
    setValue(newValue);
  };

  return [value, setSessionStorageValue];
}

export default useSessionStorage;